from src.state_machine.state_tree import StateTree
from src.state_machine.state import State, StateBundle
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random
import enum
from typing import TypeVar
from abc import abstractmethod
import re

from src.keyboards import reply
from src.containers.fixeds_list import FixedSizeList
from src.activities.activities_hub import *


StateT = TypeVar('StateT', bound=State)
T = TypeVar('T')


class QuizMenuState(State):
    def __init__(self, tree: StateTree, enable_msg: str, return_to: StateT, action: StateT, activity: T):
        super().__init__(tree)
        self.enable_msg: str = enable_msg
        self.return_to: StateT = return_to
        self.action: StateT = action
        self.activity: T = activity

    async def enable(self, bundle = None):
        await super().get_bot().send_message(
            chat_id=super().get_id(),
            text=self.enable_msg,
            reply_markup=reply.action_menu_kb
        )

    async def disable(self):
        ...

    @abstractmethod
    def get_weights(self) -> list[int]:
        ...

    def rest_weights(self) -> None:
        ...

    @abstractmethod
    def get_score(self) -> int:
        ...

    async def process_message(self, message):
        text: str = message.text.lower()

        if text == 'начать (рандом)':
            bundle = StateBundle()
            bundle.integer = int(QuizActionState.Mode.Random)
            await self.tree.set_state_by_type(self.action, bundle)

        elif text == 'начать (отработка)':
            bundle = StateBundle()
            bundle.integer = int(QuizActionState.Mode.Errors)
            await self.tree.set_state_by_type(self.action, bundle)

        elif text == 'рекорд':
            await message.answer(
                text=f'Ваш рекорд: <b>{self.get_score()}</b>',
                reply_markup=reply.action_menu_kb,
                parse_mode='HTML'
            )
        
        elif text == 'топ ошибок':
            stats_d = {index: value for index, value 
                       in enumerate(self.get_weights()) if value > 0}
            
            if stats_d:
                stats_d = sorted(stats_d.items(), key=lambda x: x[1], reverse=True)
                errors: str = ''
                act = ActivitiesHub.get(self.activity)
                for index, value in stats_d:
                    errors += f'{value} - {QuizActionState.wrap_uppercase(act.get_answer(index))}\n'
                errors = errors.strip()

                await message.answer(
                    text=errors,
                    reply_markup=reply.action_menu_kb,
                    parse_mode='HTML'
                )

            else:
                await message.answer(
                    text='Ошибок нет!',
                    reply_markup=reply.action_menu_kb
                )

        elif text == 'сбросить статистику':
            self.rest_weights()
            await message.answer(
                text=f'Статистика ошибок сброшена',
                reply_markup=reply.action_menu_kb
            )

        elif text == 'назад':
            await self.tree.set_state_by_type(self.return_to)

        else:
            await super().get_bot().send_message(
                chat_id=super().get_id(),
                text='Неизвестная команда',
                reply_markup=reply.action_menu_kb
            )


class QuizActionState(State):
    class Mode(enum.IntEnum):
        Random=0,
        Errors=1

    def __init__(self, tree, question_msg: str, return_to: StateT, activity: T):
        super().__init__(tree)
        self.memory: FixedSizeList = FixedSizeList(10)
        self.question_msg: str = question_msg
        self.return_to: StateT = return_to
        self.activity: T = activity
    
    @abstractmethod
    def get_weights(self) -> list[int]:
        pass
    
    @abstractmethod
    def add_weight(self, idx: int, val: int) -> None:
        pass
    
    @abstractmethod
    def get_score(self) -> int:
        pass

    @abstractmethod
    def set_score(self, value: int) -> None:
        pass


    async def enable(self, bundle = None):
        self.mode: QuizActionState.Mode = bundle.integer
        self.score = 0
        await self.get_bot().send_message(
            chat_id=self.get_id(),
            text=self.question_msg,
            reply_markup=self.generate_keyboard()
        )

    async def congratulate(self):
        self.score += 1
        await self.get_bot().send_message(
                chat_id=self.get_id(),
                text='✅Правильно!',
                reply_markup=self.generate_keyboard()
            )

    async def check_score(self):
            if self.get_score() >= self.score:
                await self.get_bot().send_message(
                    chat_id=self.get_id(),
                    text=f'❌Ошибка! Счёт: {self.score}'
                )
            else:
                await self.get_bot().send_message(
                    chat_id=self.get_id(),
                    text=f'❌Ошибка! 🎉Новый рекорд: {self.score}'
                )
                self.set_score(self.score)
    
    async def send_correct_answer_and_return(self, message, answer: str):
            await message.reply(
                text=f'Правильный ответ: { QuizActionState.wrap_uppercase(answer)}',
                parse_mode='HTML'
            )
            self.score=0
            await self.tree.set_state_by_type(self.return_to)

    @abstractmethod
    async def process_message(self, message: Message):
        pass

    @abstractmethod
    def generate_keyboard(self) -> ReplyKeyboardMarkup:
        pass

    @abstractmethod
    def get_random_not_in_memoty_id(self) -> int:
        pass
    
    def get_random_id(self) -> int:
        match self.mode:
            case QuizActionState.Mode.Random:
                return self.get_random_not_in_memoty_id()
            
            case QuizActionState.Mode.Errors:
                weights = self.get_weights()
                idxs = [i for i in range(len(weights)) if weights[i] > 0]
                weights = [w for w in weights if w > 0]

                if not sum(weights) == 0:
                    rarr = random.choices(idxs, weights=weights, k=sum(weights))
                    for idx in rarr:
                        if idx not in self.memory:
                            return(idx)

                return self.get_random_not_in_memoty_id()
        raise NotImplementedError()

    def wrap_uppercase(text) -> str:
        return re.sub(r'([A-ZА-ЯЁ])', r'<b>\1</b>', text)
