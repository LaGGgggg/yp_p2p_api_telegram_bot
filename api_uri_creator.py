from settings import SETTINGS


API_BASE_URL = SETTINGS.API_BASE_URL


class APIURICreator:

    @staticmethod
    async def get_login_uri() -> str:
        return f'{API_BASE_URL}/token'

    @staticmethod
    async def get_create_p2p_request_uri() -> str:
        return f'{API_BASE_URL}/create'
