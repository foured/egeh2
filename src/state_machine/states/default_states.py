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

        elif text == 'трудные слова (9)':
            await self.tree.set_state_by_type(N9_MenuState)

        elif text == 'трудные слова (10)':
            await self.tree.set_state_by_type(N10_MenuState)

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
    
    def rest_weights(self):
        self.tree.user.data.rus_n4_stats \
            = ActivitiesHub.get(RussianNumber_4).create_statistics_array()




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




class N9_MenuState(PDActioMenuStateBase):
    def __init__(self, tree):
        super().__init__(tree, 'Меню номера 9. Выберите действие', MainMenuState,
                          N9_ActionState, RussianNumber_9)
        
    def get_weights(self):
        return self.tree.user.data.rus_n9_stats
    
    def get_score(self):
        return self.tree.user.data.rus_n9_score
    
    def rest_weights(self):
        self.tree.user.data.rus_n9_stats \
            = ActivitiesHub.get(RussianNumber_9).create_statistics_array()




class N9_ActionState(PDActionStateBase):
    def __init__(self, tree):
        super().__init__(tree, 'Выберите слово с правильным написанием.', 
                         N9_MenuState, RussianNumber_9)

    def get_weights(self):
        return self.tree.user.data.rus_n9_stats
    
    def add_weight(self, idx, val):
        self.tree.user.data.rus_n9_stats[idx] += val

    def get_score(self):
        return self.tree.user.data.rus_n9_score
    
    def set_score(self, value):
        self.tree.user.data.rus_n9_score = value



class N10_MenuState(PDActioMenuStateBase):
    def __init__(self, tree):
        super().__init__(tree, 'Меню номера 10. Выберите действие', MainMenuState,
                          N10_ActionState, RussianNumber_10)
        
    def get_weights(self):
        return self.tree.user.data.rus_n10_stats
    
    def get_score(self):
        return self.tree.user.data.rus_n10_score
    
    def rest_weights(self):
        self.tree.user.data.rus_n10_stats \
            = ActivitiesHub.get(RussianNumber_10).create_statistics_array()




class N10_ActionState(PDActionStateBase):
    def __init__(self, tree):
        super().__init__(tree, 'Выберите слово с правильным написанием.', 
                         N10_MenuState, RussianNumber_10)

    def get_weights(self):
        return self.tree.user.data.rus_n10_stats
    
    def add_weight(self, idx, val):
        self.tree.user.data.rus_n10_stats[idx] += val

    def get_score(self):
        return self.tree.user.data.rus_n10_score
    
    def set_score(self, value):
        self.tree.user.data.rus_n10_score = value