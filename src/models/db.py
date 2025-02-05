from src.models.user import User

import asyncio
from aiogram import Bot
import json
import datetime

class DB():
    users: list[User] = []
    bot: Bot

    @staticmethod
    def get_user(id: str) -> User:
        for user in DB.users:
            if user.id == id:
                return user
        user = User(id, DB.bot)
        user.setup_default_tree()
        DB.users.append(user)
        return user
    
    @staticmethod
    def initialize(bot: Bot) -> None:
        DB.bot = bot

    @staticmethod
    def save_to_file(path: str) -> None:
        with open(path, 'w', encoding='utf-8') as file:
            json.dump([user.to_dict() for user in DB.users], file, ensure_ascii=False)

    @staticmethod
    def load_from_file(path: str) -> None:
        try:
            with open(path, 'r', encoding='utf-8') as file:
                user_data = json.load(file)
                DB.users = [User.from_dict(data, DB.bot) for data in user_data]
        except Exception:
            DB.users = []

    @staticmethod
    async def save_periodically(interval: int, log: bool = False):
        while True:
            await asyncio.sleep(interval)
            DB.save_to_file('save.json')
            if log:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"DB saved at {current_time}.")
