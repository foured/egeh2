from aiogram import Bot
from aiogram.types import Message

from src.state_machine.state_tree import StateTree
from src.state_machine.states.default_states import *
from src.activities.activities_hub import *

class User():
    class Data():
        def __init__(self, rus_n4_score: int = 0):
            self.rus_n4_score: int = rus_n4_score
            self.rus_n4_stats: list[int] \
                = ActivitiesHub.get(RussianNumber_4).create_statistics_array()

        def to_dict(self):
            return {
                'rus_n4_score': self.rus_n4_score,
                'rus_n4_stats': self.rus_n4_stats
            }
        
        @staticmethod
        def from_dict(data) -> 'User.Data':
            d = User.Data(data['rus_n4_score'])
            d.rus_n4_stats = list(data['rus_n4_stats'])
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
        ams = AccentsMenuState_2(self.tree)
        aas = AccentsActionState_2(self.tree)
        self.tree.add_state(mms)
        self.tree.add_state(ams)
        self.tree.add_state(aas)
    
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