from aiogram.filters.callback_data import CallbackData


class OrderData(CallbackData, prefix="buy"):
    # product: Product
    id: int
    name: str
    price: int
