from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from states import LoginStates, AddP2PRequestStates
from classes import APIURLCreator, APIRequestCreator
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

    is_success, _ = await APIRequestCreator(message.from_user.id).do_response(
        message,
        state,
        'post',
        APIURLCreator.CREATE_P2P_REQUEST_URL,
        params={'repository_link': link, 'comment': message.text},
    )

    if is_success:

        await message.answer('Ваш запрос создан успешно!')

        await state.set_data({})
        await state.set_state(LoginStates.LOGGED_IN)
