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
from src.state_machine.states.quiz_states import QuizActionState


StateT = TypeVar('StateT', bound=State)
T = TypeVar('T')


class PDActionStateBase(QuizActionState):
    def __init__(self, tree, question_msg: str, return_to: StateT, activity: T):
        super().__init__(tree, question_msg, return_to, activity)

    async def process_message(self, message: Message):
        text: str = message.text

        res: bool = ActivitiesHub.get(self.activity).is_word_correct(text)
        word_id: int = ActivitiesHub.get(self.activity).get_word_id(text)

        if word_id != -1:
            self.add_weight(word_id, -1 if res else 1)
            self.memory.add(word_id)            

        if res:
            await self.congratulate()

        else:
            correct_answer: str = ActivitiesHub.get(self.activity).get_correct_word(text)

            await self.check_score()

            await self.send_correct_answer_and_return(message, correct_answer)


    def get_random_not_in_memoty_id(self) -> int:
        act: PairDependendActivity = ActivitiesHub.get(self.activity)
        w_idx: int = act.get_random_id()
        while w_idx in self.memory:
            w_idx = act.get_random_id()
        return w_idx

    def generate_keyboard(self) -> ReplyKeyboardMarkup:
        words: list[str] = list(ActivitiesHub.get(self.activity)
                                .get_pair(self.get_random_id()))
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