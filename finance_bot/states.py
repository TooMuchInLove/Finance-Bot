from aiogram.fsm.state import State, StatesGroup


class StateWallet(StatesGroup):
    add = State()


class StateCategory(StatesGroup):
    add = State()
