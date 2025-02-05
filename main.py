import asyncio
from aiogram import Bot, Dispatcher 

from src.models.db import DB
from src.handlers import user_contact
from src.activities.activities_hub import *

async def bot_main():
    print('Starting bot')
    bot = Bot('7293433895:AAHlgtcDok8056aDxgkoQ5i93TPfkYKnZ54')
    dp = Dispatcher()
    ActivitiesHub.setup()
    DB.initialize(bot)
    DB.load_from_file('save.json')
    dp.include_routers(
        user_contact.router
    )

    asyncio.create_task(DB.save_periodically(10))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(bot_main())