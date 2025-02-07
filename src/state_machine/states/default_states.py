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
            await self.tree.set_state_by_type(AccentsMenuState)

        elif text == 'трудные слова (9-12)':
            await self.tree.set_state_by_type(HTRMenuState)

        else:
            await super().get_bot().send_message(
                chat_id=self.tree.user.id,
                text='Неизвестная команда',
                reply_markup=reply.main_menu_kb
            )





class AccentsMenuState(PDActioMenuStateBase):
    def __init__(self, tree):
        super().__init__(tree, 'Меню ударений. Выберите действие', MainMenuState,
                          AccentsActionState, RussianNumber_4)
        
    def get_weights(self):
        return self.tree.user.data.rus_n4_stats
    
    def get_score(self):
        return self.tree.user.data.rus_n4_score




class AccentsActionState(PDActionStateBase):
    def __init__(self, tree):
        super().__init__(tree, 'Выберите слово с правильным ударением.', 
                         AccentsMenuState, RussianNumber_4)

    def get_weights(self):
        return self.tree.user.data.rus_n4_stats
    
    def add_weight(self, idx, val):
        self.tree.user.data.rus_n4_stats[idx] += val

    def get_score(self):
        return self.tree.user.data.rus_n4_score
    
    def set_score(self, value):
        self.tree.user.data.rus_n4_score = value




class HTRMenuState(PDActioMenuStateBase):
    def __init__(self, tree):
        super().__init__(tree, 'Меню трудных слов. Выберите действие', MainMenuState,
                          HTRActionState, RussianHTR)
        
    def get_weights(self):
        return self.tree.user.data.rus_htr_stats
    
    def get_score(self):
        return self.tree.user.data.rus_htr_score




class HTRActionState(PDActionStateBase):
    def __init__(self, tree):
        super().__init__(tree, 'Выберите слово с правильным написанием.', 
                         HTRMenuState, RussianHTR)

    def get_weights(self):
        return self.tree.user.data.rus_htr_stats
    
    def add_weight(self, idx, val):
        self.tree.user.data.rus_htr_stats[idx] += val

    def get_score(self):
        return self.tree.user.data.rus_htr_score
    
    def set_score(self, value):
        self.tree.user.data.rus_htr_score = value