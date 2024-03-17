from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from requests import get

from states import LoginStates, AddP2PRequestStates
from api_uri_creator import APIURICreator
from filters import LoggedInUserFilter


router = Router()


@router.message(Command('add_p2p_request'), LoggedInUserFilter())
async def add_p2p_request_not_started(message: Message, state: FSMContext):

    await state.set_state(AddP2PRequestStates.WAITING_FOR_LINK)

    await message.answer('Пришлите ссылку на репозиторий, пожалуйста')


@router.message(AddP2PRequestStates.WAITING_FOR_LINK)
async def add_p2p_request_waiting_for_link(message: Message, state: FSMContext):

    await state.set_state(AddP2PRequestStates.WAITING_FOR_COMMENT)
    await state.set_data({'link': message.text})

    await message.answer('Пришлите комментарий к p2p request-у, пожалуйста')


@router.message(AddP2PRequestStates.WAITING_FOR_COMMENT)
async def add_p2p_request_waiting_for_link(message: Message, state: FSMContext):

    state_data = await state.get_data()
    await state.set_state(AddP2PRequestStates.NOT_STARTED)

    if not (link := state_data.get('link')):

        await message.answer('Произошла ошибка, попробуйте ещё раз или обратитесь в поддержку')

        return

    response = get(
        await APIURICreator.get_create_p2p_request_uri(), params={'repository_link': link, 'comment': message.text}
    )

    match response.status_code:

        case 401:

            await message.answer('Не удалось войти в аккаунт, пожалуйста, войдите заново')

            await state.set_state(LoginStates.NOT_LOGGED_IN)

        case 200:

            await message.answer('Ваш запрос создан успешно!')

            await state.set_data({})
            await state.set_state(LoginStates.LOGGED_IN)

        case _:
            await message.answer('Ошибка обращения к API, попробуйте ещё раз или обратитесь в поддержку')
