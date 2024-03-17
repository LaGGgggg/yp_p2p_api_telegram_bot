from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from requests import post

from states import LoginStates
from api_uri_creator import APIURICreator
from sql.crud import UserCrud
from sql.database import Session


router = Router()


@router.message(Command('login'))
async def login(message: Message, state: FSMContext, command: CommandObject):

    command_args = command.args

    args = command_args.split() if command_args else []

    if len(args) != 2:

        await message.answer(
            'Некорректно составлена команда, вот пример правильного варианта: `/login username password`',
            parse_mode=ParseMode.MARKDOWN_V2,
        )

        return

    response = post(await APIURICreator.get_login_uri(), data={'username': args[0], 'password': args[1]})

    match response.status_code:

        case 401:
            await message.answer('Не удалось войти в аккаунт, пожалуйста, проверьте правильность введённых данных')

        case 200:

            access_token = response.json().get('access_token')

            if not access_token:

                await message.answer(
                    'Вход не был завершён, не удалось получить необходимую информацию из ответа API. Попробуйте ещё'
                    ' раз или обратитесь в поддержку'
                )

                return

            with Session() as db:

                user_crud = UserCrud(db)

                if user := user_crud.get(telegram_id=message.from_user.id):
                    user_crud.update(user, api_token=access_token)

                else:
                    user_crud.create(telegram_id=message.from_user.id, api_token=access_token)

            await state.set_state(LoginStates.LOGGED_IN)

            await message.answer('Вход в аккаунт выполнен успешно!')

        case _:
            await message.answer('Ошибка обращения к API, попробуйте ещё раз или обратитесь в поддержку')


@router.message(Command('logout'))
async def logout(message: Message, state: FSMContext):

    with Session() as db:

        user_crud = UserCrud(db)

        if user := user_crud.get(telegram_id=message.from_user.id):
            user_crud.update(user, api_token=None)

    await state.set_state(LoginStates.NOT_LOGGED_IN)

    await message.answer('Выход из аккаунта произведён успешно')
