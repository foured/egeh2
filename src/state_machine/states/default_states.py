from src.state_machine.state_tree import StateTree
from src.state_machine.state import State, StateBundle
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random
import enum

from src.keyboards import reply
from src.activities.activities_hub import *
from src.containers.fixeds_list import FixedSizeList
from src.state_machine.states.pd_action_bases import PDActioMenuStateBase, PDActionStateBase

class MainMenuState(State):
    def __init__(self, tree: StateTree) -> None:
        super().__init__(tree)

    async def enable(self, bundle = None):
        await super().get_bot().send_message(
            chat_id=self.tree.user.id,
            text='Главное меню.',
            reply_markup=reply.main_menu_kb
        )
    
    async def disable(self):
        pass

    async def process_message(self, message):
        text : str = message.text.lower()

        if text == 'ударения':
            await self.tree.set_state_by_type(AccentsMenuState_2)
        else:
            await super().get_bot().send_message(
                chat_id=self.tree.user.id,
                text='Неизвестная команда',
                reply_markup=reply.main_menu_kb
            )





class AccentsMenuState_2(PDActioMenuStateBase):
    def __init__(self, tree):
        super().__init__(tree, 'Меню ударений. Выберите действие', MainMenuState,
                          AccentsActionState_2, RussianNumber_4)
        
    def get_weights(self):
        return self.tree.user.data.rus_n4_stats
    
    def get_score(self):
        return self.tree.user.data.rus_n4_score




class AccentsActionState_2(PDActionStateBase):
    def __init__(self, tree):
        super().__init__(tree, 'Выберите слово с правильным ударением.', 
                         AccentsMenuState_2, RussianNumber_4)

    def get_weights(self):
        return self.tree.user.data.rus_n4_stats
    
    def add_weight(self, idx, val):
        self.tree.user.data.rus_n4_stats[idx] += val

    def get_score(self):
        return self.tree.user.data.rus_n4_score
    
    def set_score(self, value):
        self.tree.user.data.rus_n4_score = value


class AccentsMenuState(State):
    def __init__(self, tree: StateTree) -> None:
        super().__init__(tree)

    async def enable(self, bundle = None):
        await super().get_bot().send_message(
            chat_id=super().get_id(),
            text='Меню ударений. Выберите действие',
            reply_markup=reply.action_menu_kb
        )
        
    async def disable(self):
        ...

    async def process_message(self, message):
        text : str = message.text.lower()

        if text == 'начать (рандом)':
            bundle = StateBundle()
            bundle.integer = int(AccentsActionState.Mode.Random)
            await self.tree.set_state_by_type(AccentsActionState, bundle)

        elif text == 'начать (отработка)':
            bundle = StateBundle()
            bundle.integer = int(AccentsActionState.Mode.Errors)
            await self.tree.set_state_by_type(AccentsActionState, bundle)

        elif text == 'рекорд':
            await message.answer(
                text=f'Ваш рекорд: <b>{self.tree.user.data.rus_n4_score}</b>',
                reply_markup=reply.action_menu_kb,
                parse_mode='HTML'
            )
        
        elif text == 'топ ошибок':
            stats_d = {index: value for index, value 
                       in enumerate(self.tree.user.data.rus_n4_stats) if value > 0}
            
            if stats_d:
                stats_d = sorted(stats_d.items(), key=lambda x: x[1], reverse=True)
                errors: str = ''
                rn4 = ActivitiesHub.get(RussianNumber_4)
                for index, value in stats_d:
                    errors += f'{value} - {rn4.get_pair(index)[0]}\n'
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

        elif text == 'назад':
            await self.tree.set_state_by_type(MainMenuState)

        else:
            await super().get_bot().send_message(
                chat_id=super().get_id(),
                text='Неизвестная команда',
                reply_markup=reply.action_menu_kb
            )





class AccentsActionState(State):
    class Mode(enum.IntEnum):
        Random = 0,
        Errors = 1

    def __init__(self, tree: StateTree):
        super().__init__(tree)
        self.memory: FixedSizeList = FixedSizeList(10)

    async def enable(self, bundle):
        self.mode: AccentsActionState.Mode = bundle.integer
        self.score = 0
        await self.get_bot().send_message(
            chat_id=self.get_id(),
            text='Выберите слово с правильным ударением.',
            reply_markup=self.generate_keyboard()
        )

    async def process_message(self, message):
        text: str = message.text

        res: bool = ActivitiesHub.get(RussianNumber_4).is_word_correct(text)
        word_id: int = ActivitiesHub.get(RussianNumber_4).get_word_id(text)
        self.memory.add(word_id)

        if word_id != -1:
            self.tree.user.data.rus_n4_stats[word_id] += -1 if res else 1

        if res:
            self.score += 1
            await self.get_bot().send_message(
                chat_id=self.get_id(),
                text='✅Правльно!',
                reply_markup=self.generate_keyboard()
            )

        else:
            correct_answer: str = ActivitiesHub.get(RussianNumber_4).get_correct_word(text)

            if self.tree.user.data.rus_n4_score >= self.score:
                await self.get_bot().send_message(
                    chat_id=self.get_id(),
                    text=f'❌Ошибка! Счёт: {self.score}'
                )
            else:
                await self.get_bot().send_message(
                    chat_id=self.get_id(),
                    text=f'❌Ошибка! 🎉Новый рекорд: {self.score}'
                )
                self.tree.user.data.rus_n4_score = self.score

            await message.reply(
                text=f'Правильный ответ: {correct_answer}'
            )
            self.score=0
            await self.tree.set_state_by_type(AccentsMenuState)

    def get_random_word_id(self) -> int:
        rn4 = ActivitiesHub.get(RussianNumber_4)

        match self.mode:
            case AccentsActionState.Mode.Random:
                w_idx: int = rn4.get_random_id()
                while w_idx in self.memory:
                    w_idx = rn4.get_random_id()
                return w_idx
            
            case AccentsActionState.Mode.Errors:
                ml: int = len(self.memory) + 1
                weights = self.tree.user.data.rus_n4_stats

                total_weight = sum(weights)
                if total_weight == 0:
                    normalized_weights = [1 / len(weights)] * len(weights)
                else:
                    normalized_weights = [w / total_weight for w in weights]
                
                w_idxs = random.choices(range(len(normalized_weights)), weights=normalized_weights, k=ml)
                for w_idx in w_idxs:
                    if w_idx not in self.memory:
                        return w_idx
                return rn4.get_random_id()
        raise NotImplementedError()

    def generate_keyboard(self) -> ReplyKeyboardMarkup:
        words: list[str] = list(ActivitiesHub.get(RussianNumber_4)
                                .get_pair(self.get_random_word_id()))
        random.shuffle(words)
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text=words[0]),
                    KeyboardButton(text=words[1])
                ]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )