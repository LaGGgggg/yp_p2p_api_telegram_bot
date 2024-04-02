from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode


router = Router()


@router.message(Command('help', 'start'))
async def start(message: Message):
    await message.answer(
        'Здесь вы можете присылать ссылки на ваши проекты, чтобы их проверили, и самому ревьюить проекты других '
        'пользователей.  Вот краткая инструкция пользования ботом:\n\n'
        '<b>Вход</b>\nЧтобы войти в аккаунт, введите команду <code>/login username password</code>, где username - ваш '
        'логин, а password - ваш пароль.\n\n'
        '<b>Отправка проекта</b>\nВведите команду /add_p2p_request, далее отправьте ссылку на ваш репозиторий '
        'с проектом на GitHub.  Затем напишите комментарий, который увидит ревьюер во время проверки.\nПо команде '
        '/view_requests можно посмотреть список ссылок и комментариев всех ваших отправленных проектов.\n\n'
        '<b>Ревью</b>\nПо команде /start_review вы получите ссылку на репозиторий проекта на GitHub и комментарий '
        'создателя.\nВведя команду /complete_review, вы сможете отправить ссылку на ваше ревью.\n'
        'У вас не может быть сразу несколько ревью одновременно!\n\n'
        '<b>Выход</b>\nЧтобы выйти из аккаунта, введите команду /logout.',
        parse_mode=ParseMode.HTML
    )
