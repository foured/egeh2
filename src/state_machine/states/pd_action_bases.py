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
from src.activities.activities_hub import *
from src.containers.fixeds_list import FixedSizeList
from src.activities.pair_dep_activity import PairDependendActivity

StateT = TypeVar('StateT', bound=State)
T = TypeVar('T')

class PDActioMenuStateBase(State):
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
            bundle.integer = int(PDActionStateBase.Mode.Random)
            await self.tree.set_state_by_type(self.action, bundle)

        elif text == 'начать (отработка)':
            bundle = StateBundle()
            bundle.integer = int(PDActionStateBase.Mode.Errors)
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
                    errors += f'{value} - {act.get_pair(index)[0]}\n'
                errors = errors.strip()

                await message.answer(
                    text=errors,
                    reply_markup=reply.action_menu_kb
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















class PDActionStateBase(State):
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
        self.mode: PDActionStateBase.Mode = bundle.integer
        self.score = 0
        await self.get_bot().send_message(
            chat_id=self.get_id(),
            text=self.question_msg,
            reply_markup=self.generate_keyboard()
        )

    async def process_message(self, message):
        text: str = message.text

        res: bool = ActivitiesHub.get(self.activity).is_word_correct(text)
        word_id: int = ActivitiesHub.get(self.activity).get_word_id(text)

        if word_id != -1:
            self.add_weight(word_id, -1 if res else 1)
            self.memory.add(word_id)            

        if res:
            self.score += 1
            await self.get_bot().send_message(
                chat_id=self.get_id(),
                text='✅Правильно!',
                reply_markup=self.generate_keyboard()
            )

        else:
            correct_answer: str = ActivitiesHub.get(self.activity).get_correct_word(text)

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

            await message.reply(
                text=f'Правильный ответ: { PDActionStateBase.wrap_uppercase(correct_answer)}',
                parse_mode='HTML'
            )
            self.score=0
            await self.tree.set_state_by_type(self.return_to)


    def get_random_not_in_memoty_id(self) -> int:
        act: PairDependendActivity = ActivitiesHub.get(self.activity)
        w_idx: int = act.get_random_id()
        while w_idx in self.memory:
            w_idx = act.get_random_id()
        return w_idx

    def get_random_word_id(self) -> int:
        match self.mode:
            case PDActionStateBase.Mode.Random:
                return self.get_random_not_in_memoty_id()
            
            case PDActionStateBase.Mode.Errors:
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

    def generate_keyboard(self) -> ReplyKeyboardMarkup:
        words: list[str] = list(ActivitiesHub.get(self.activity)
                                .get_pair(self.get_random_word_id()))
        random.shuffle(words)
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text = words[0])
                ],
                [
                    KeyboardButton(text = words[1])
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )
    
    def wrap_uppercase(text) -> str:
        return re.sub(r'([A-ZА-ЯЁ])', r'<b>\1</b>', text)