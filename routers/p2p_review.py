from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext

from classes import APIURLCreator, APIRequestCreator
from filters import LoggedInUserFilter
from states import CompleteP2PReviewStates, LoginStates


router = Router()


@router.message(Command('start_review'), LoggedInUserFilter())
async def start_p2p_review(message: Message, state: FSMContext):

    is_success, response_json = await APIRequestCreator(message.from_user.id).do_response(
        message, state, 'get', APIURLCreator.CREATE_P2P_REVIEW_URL
    )

    if is_success:

        if repository_link := response_json.get('repository_link'):
            await message.answer(
                f"[Ссылка на репозиторий]({repository_link}) для вашего review, комментарий создателя:"
                f" {response_json.get('comment', '')}",
                parse_mode=ParseMode.MARKDOWN_V2,
            )

        else:
            await message.answer(f"Не удалось начать новое review (ответ API: {response_json.get('context', '')})")


@router.message(Command('complete_review'), LoggedInUserFilter())
async def complete_p2p_review(message: Message, state: FSMContext):

    await state.set_state(CompleteP2PReviewStates.WAITING_FOR_LINK)

    await message.answer('Пришлите ссылку на ваше review')


@router.message(CompleteP2PReviewStates.WAITING_FOR_LINK)
async def complete_p2p_review_waiting_for_link(message: Message, state: FSMContext):

    await state.set_state(LoginStates.LOGGED_IN)

    is_success, response_json = await APIRequestCreator(message.from_user.id).do_response(
        message, state, 'get', APIURLCreator.GET_P2P_REVIEWS_LIST_URL, params={'review_state': 'progress'}
    )

    if is_success:

        if not response_json:
            await message.answer('У вас нет активных review')

        elif p2p_review_id := response_json[0].get('id'):

            is_success, response_json = await APIRequestCreator(message.from_user.id).do_response(
                message,
                state,
                'post',
                APIURLCreator.COMPLETE_P2P_REVIEW_URL,
                params={'link': message.text, 'p2p_review_id': p2p_review_id},
            )

            if is_success:

                if response_context := response_json.get('context'):
                    await message.answer(f'Не удалось завершить review (ответ API: {response_context})')

                else:
                    await message.answer('Review завершено успешно!')

        else:
            await message.answer(
                'Не удалось получить review из ответа API, попробуйте снова или обратитесь в поддержку'
            )


@router.message(Command('view_requests'), LoggedInUserFilter())
async def view_p2p_requests(message: Message, state: FSMContext):

    is_success, response_json = await APIRequestCreator(message.from_user.id).do_response(
        message, state, 'get', APIURLCreator.GET_P2P_REQUESTS_LIST_URL
    )

    if is_success:

        if isinstance(response_json, list):

            # answer_text = "Ваши p2p request-ы:\n" + "[Ссылка](url), комментарий: comment\n" * amount of p2p requests
            answer_text = 'Ваши p2p request\\-ы:\n' + '\n'.join([
                f"[Ссылка]({p2p_request['repository_link']}), комментарий: {p2p_request['comment']}"
                for p2p_request in response_json
            ])

            await message.answer(answer_text,  parse_mode=ParseMode.MARKDOWN_V2)

        else:
            await message.answer(
                'Не удалось получить данные из ответа API, попробуйте снова или обратитесь в поддержку'
            )
