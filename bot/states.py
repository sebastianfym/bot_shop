from aiogram.fsm.state import StatesGroup, State


class ShopState(StatesGroup):
    show_category = State()
    show_subcategory = State()
    show_goods = State()
    add_goods = State()
    quantity_goods = State()
    confirmation_order = State()


class BasketState(StatesGroup):
    show_basket = State()
    delivery_address = State()
    recipient_name = State()
    recipient_phone = State()
    making_an_order = State()


class FAQState(StatesGroup):
    show_faq = State()
    first_faq_answer = State()