from src.state_machine.state import State, StateBundle
from aiogram.types import Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import random
import enum
from typing import TypeVar
from abc import abstractmethod

from src.keyboards import reply
from src.activities.activities_hub import *
from src.containers.fixeds_list import FixedSizeList
from src.activities.insert_val_activity import InsertValueActivity
from src.state_machine.states.quiz_states import QuizActionState


StateT = TypeVar('StateT', bound=State)
T = TypeVar('T')


class IVActionSateBase(QuizActionState):
    def __init__(self, tree, question_msg: str, return_to: StateT, activity: T):
        super().__init__(tree, question_msg, return_to, activity)
        self.item: InsertValueActivity.InsertedItem = None

    async def enable(self, bundle = None):
        self.mode: QuizActionState.Mode = bundle.integer
        self.score = 0
        await self.get_bot().send_message(
            chat_id=self.get_id(),
            text=self.question_msg
        )
        kb = self.generate_keyboard()
        await self.get_bot().send_message(
            chat_id=self.get_id(),
            text=self.item.word,
            reply_markup=kb
        )


    async def process_message(self, message):
        text = message.text

        res: bool = self.item.check(text) if self.item != None else False
        item_id: int = self.item.id if self.item != None else -1

        if item_id != -1:
            self.add_weight(item_id, -1 if res else 1)
            self.memory.add(item_id)

        if res:
            self.score += 1
            await self.get_bot().send_message(
                    chat_id=self.get_id(),
                    text='✅Правильно!'
                )
            kb = self.generate_keyboard()
            await self.get_bot().send_message(
                    chat_id=self.get_id(),
                    text=self.item.word,
                    reply_markup=kb
                )

        else:
            correct_answer: str = self.item.get_correct()

            await self.check_score()

            await self.send_correct_answer_and_return(message, correct_answer)

    def get_random_not_in_memoty_id(self) -> int:
        act: InsertValueActivity = ActivitiesHub.get(self.activity)
        id = act.get_random_id()
        while id in self.memory:
            id = act.get_random_id()
        return id

    def generate_keyboard(self) -> ReplyKeyboardMarkup:
        self.item = ActivitiesHub.get(self.activity).get_item(self.get_random_id())
        choices = self.item.items.copy()
        random.shuffle(choices)
        return ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton(text=c) for c in choices]],
            resize_keyboard=True,
            one_time_keyboard=True
        )
        