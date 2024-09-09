import asyncio

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from src.config import TOKEN


from src.handlers.user_private import user_private_router


bot = Bot(token=TOKEN,parse_mode=ParseMode.HTML)
dp = Dispatcher()

dp.include_routers(
    user_private_router,
)


async def on_shutdown(bot):
    print('бот лег')



async def main()-> None:

    await dp.start_polling(
        bot
        )



asyncio.run(main())