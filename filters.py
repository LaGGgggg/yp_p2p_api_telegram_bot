from aiogram.filters import Filter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from states import LoginStates


class LoggedInUserFilter(Filter):
    async def __call__(self, _: Message, state: FSMContext) -> bool:
        return await state.get_state() == LoginStates.LOGGED_IN
