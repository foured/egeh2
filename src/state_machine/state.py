from abc import abstractmethod
from aiogram.types import Message
from aiogram import Bot

class StateBundle():
    def __init__(self):
        self.integer = 0

class State():
    def __init__(self, tree) -> None:
        from src.state_machine.state_tree import StateTree
        self.tree: 'StateTree' = tree
        tree.add_state(self)

    @abstractmethod
    async def enable(self, bundle: StateBundle = None) -> None:
        pass

    @abstractmethod
    async def disable(self) -> None:
        pass

    @abstractmethod
    async def process_message(self, message: Message) -> None:
        pass

    def get_bot(self) -> Bot:
        return self.tree.user.bot
    
    def get_id(self) -> str:
        return self.tree.user.id
