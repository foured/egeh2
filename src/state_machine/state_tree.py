from src.state_machine.state import State, StateBundle
from aiogram.types import Message
from typing import TypeVar

T = TypeVar('T')

class StateTree():
    def __init__(self, user):
        from src.models.user import User

        self.user: 'User' = user
        self.states: list[State] = []
        self.current_state = 0

    def add_state(self, state: State) -> None:
        self.states.append(state)
    
    async def set_state_by_type(self, type: T, bundle: StateBundle = None) -> None:
        for i in range(len(self.states)):
            if isinstance(self.states[i], type):
                await self.states[i].disable()
                self.current_state = i
                await self.states[i].enable(bundle)
                return
        raise ValueError(f"No such state in tree of type: {type}.")

    async def execute_current_state(self, message: Message) -> None:
        await self.states[self.current_state].process_message(message)

    def clear(self):
        self.current_state = 0
        self.states.clear()