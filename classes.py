from typing import Literal

from requests import get, post
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from settings import SETTINGS
from sql.database import Session
from sql.crud import UserCrud
from states import LoginStates
from exceptions import UnknownHTTPMethodError


API_BASE_URL = SETTINGS.API_BASE_URL


class APIURLCreator:

    LOGIN_URL = f'{API_BASE_URL}/token'
    CREATE_P2P_REQUEST_URL = f'{API_BASE_URL}/p2p_request/create'
    CREATE_P2P_REVIEW_URL = f'{API_BASE_URL}/p2p_request/review/start'
    COMPLETE_P2P_REVIEW_URL = f'{API_BASE_URL}/p2p_request/review/complete'
    GET_P2P_REVIEWS_LIST_URL = f'{API_BASE_URL}/p2p_request/review/list'
    GET_P2P_REQUESTS_LIST_URL = f'{API_BASE_URL}/p2p_request/list'


class APIRequestCreator:

    def __init__(self, user_telegram_id: int) -> None:
        with Session() as db:
            self.api_token = UserCrud(db).get(telegram_id=user_telegram_id).api_token

    async def do_response(
            self,
            telegram_message: Message,
            telegram_state: FSMContext,
            request_type: Literal['get', 'post'],
            *args,
            cookies: dict[str, str] | None = None,
            **kwargs,
    ) -> tuple[bool, dict]:

        if cookies:
            cookies['access-token'] = self.api_token

        else:
            cookies = {'access-token': self.api_token}

        match request_type:

            case 'get':
                request_function = get

            case 'post':
                request_function = post

            case _:
                raise UnknownHTTPMethodError(request_type)

        response = request_function(*args, cookies=cookies, **kwargs)

        match response.status_code:

            case 401:

                await telegram_message.answer('Не удалось войти в аккаунт, пожалуйста, войдите заново')

                await telegram_state.set_state(LoginStates.NOT_LOGGED_IN)

            case 200:
                # success code
                pass

            case _:
                await telegram_message.answer('Ошибка обращения к API, попробуйте ещё раз или обратитесь в поддержку')

        return response.status_code == 200, response.json()
