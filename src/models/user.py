from aiogram import Bot
from aiogram.types import Message

from src.state_machine.state_tree import StateTree
from src.state_machine.states.default_states import *
from src.activities.activities_hub import *

class User():
    class Data():
        def __init__(self, rus_n4_score: int = 0, rus_htr: int = 0,
                     rus_vcblr: int = 0, rus_vrb_sfx: int = 0, 
                     rus_pre_pri: int = 0):
            self.rus_n4_score: int = rus_n4_score
            self.rus_n4_stats: list[int] \
                = ActivitiesHub.get(RussianNumber_4).create_statistics_array()
            
            self.rus_n9_score: int = rus_htr
            self.rus_n9_stats: list[int] \
                = ActivitiesHub.get(RussianNumber_9).create_statistics_array()
            
            self.rus_vcblr_score = rus_vcblr
            self.rus_vcblr_stats: list[int] \
                = ActivitiesHub.get(RussianVocabulary_Insert).create_statistics_array()
            
            self.rus_vrb_sfx_score = rus_vrb_sfx
            self.rus_vrb_sfx_stats: list[int] \
                = ActivitiesHub.get(RussianVerbSuffix).create_statistics_array()
            
            self.rus_prepri_score = rus_pre_pri
            self.rus_prepri_stats: list[int] \
                = ActivitiesHub.get(RussianPrePri).create_statistics_array()

        def to_dict(self):
            return {
                'rus_n4_score': self.rus_n4_score,
                'rus_n4_stats': self.rus_n4_stats,
                'rus_n9_score': self.rus_n9_score,
                'rus_n9_stats': self.rus_n9_stats,
                'rus_vcblr_score': self.rus_vcblr_score,
                'rus_vcblr_stats': self.rus_vcblr_stats,
                'rus_vrb_sfx_score': self.rus_vrb_sfx_score,
                'rus_vrb_sfx_stats': self.rus_vrb_sfx_stats,
                'rus_prepri_score': self.rus_prepri_score,
                'rus_prepri_stats': self.rus_prepri_stats
            }
        
        @staticmethod
        def from_dict(data) -> 'User.Data':
            d = User.Data(data['rus_n4_score'], data['rus_n9_score'], 
                            data['rus_vcblr_score'], data['rus_vrb_sfx_score'],
                            data['rus_prepri_score'])
            d.rus_n4_stats = list(data['rus_n4_stats'])
            d.rus_n9_stats = list(data['rus_n9_stats'])
            d.rus_vcblr_stats = list(data['rus_vcblr_stats'])
            d.rus_vrb_sfx_stats = list(data['rus_vrb_sfx_stats'])
            d.rus_prepri_stats = list(data['rus_prepri_stats'])
            return d

    def __init__(self, id: str, bot: Bot, data: 'User.Data' = None) -> None:
        self.id = id
        self.bot = bot
        self.tree = StateTree(self)
        self.data = data if data is not None else User.Data()

    async def get_chat(self):
        return await self.bot.get_chat(self.id)
    
    async def process_message(self, message: Message) -> None:
        await self.tree.execute_current_state(message)

    async def enable_first_state(self) -> None:
        await self.tree.states[0].enable()

    def setup_default_tree(self):
        mms = MainMenuState(self.tree)
        ams = AccentsMenuState(self.tree)
        aas = AccentsActionState(self.tree)
        n9ms = N9_MenuState(self.tree)
        n9as = N9_ActionState(self.tree)
        vms = Vocabulary_MenuState(self.tree)
        vas = Vocabulary_ActionState(self.tree)
        vsfms = VerbSuffix_MenuState(self.tree)
        vsfas = VerbSuffix_ActionState(self.tree)
        PrePri_MenuState(self.tree)
        PrePri_ActionState(self.tree)
    
    def to_dict(self):
        return {
            'id': self.id,
            'udata': self.data.to_dict()
        }

    @staticmethod
    def from_dict(data, bot: Bot) -> 'User':
        user = User(data['id'], bot, User.Data.from_dict(data['udata']))
        user.setup_default_tree()
        return user