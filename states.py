from aiogram.fsm.state import StatesGroup, State


class LoginStates(StatesGroup):

    NOT_LOGGED_IN = State()
    LOGGED_IN = State()


class AddP2PRequestStates(StatesGroup):
    """Assumed that a user is authorized"""

    NOT_STARTED = State()
    WAITING_FOR_LINK = State()
    WAITING_FOR_COMMENT = State()


class CompleteP2PReviewStates(StatesGroup):
    """Assumed that a user is authorized"""

    NOT_STARTED = State()
    WAITING_FOR_LINK = State()
