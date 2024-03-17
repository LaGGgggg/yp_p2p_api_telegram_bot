from asyncio import run as asyncio_run

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from settings import SETTINGS
from routers import users, p2p_request
from sql.database import create_all_tables


async def main() -> None:

    dp = Dispatcher(storage=MemoryStorage())

    @dp.shutdown()
    async def shutdown() -> None:
        await dp.storage.close()

    dp.include_routers(users.router, p2p_request.router)

    bot = Bot(token=SETTINGS.BOT_TOKEN)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':

    create_all_tables()

    asyncio_run(main())

