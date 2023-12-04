import asyncio
import logging
from datetime import datetime

from aiogram import F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

import aiohttp
from aiogram import Dispatcher, types

from states import ShopState, BasketState, FAQState
from config import BASE_URL, bot, logger
from keyboards_config import kb_main, kb_confirmation, kb_start
from services import (register, get_category_list, get_subcategory_list, inline_pagination_buttons, get_goods_list,
                      send_photo,
                      goods_in_basket, get_basket, get_detail_goods, del_goods_from_basket, get_payment,
                      get_faq_questions, get_all_answer_on_first_faq_question, get_all_questions_on_first_faq_answer,
                      get_last_faq_answer, validate_phone_number, get_channels_id_list)

logging.basicConfig(level=logging.INFO)

storage = MemoryStorage()
dp = Dispatcher(bot=bot, storage=storage)


@dp.message(Command("start"))
async def start(message: types.Message):
    tg_id = message.from_user.id
    channel_checker = False
    try:
        channels_list = await get_channels_id_list()

        for channel in channels_list['data']:
            user_channel_status = await bot.get_chat_member(chat_id=f'{channel["chat_id"]}', user_id=tg_id)
            if user_channel_status.status == 'left':
                await message.answer(f'Вы не являетесь участником канала: @{channel["title"]}. Пожалуйста, подпишитесь на канал.', reply_markup=kb_start)
                return
        channel_checker = True
        if channel_checker:
            username = message.from_user.username
            name = message.from_user.full_name

            resp = await register(tg_id, username, name)
            if resp.status == 200:
                logger.info(f"Пользователь с {tg_id} был зарегестрирован в {datetime.now()}")
                await message.answer(text='Вы в главном меню. Вот наш функционал.', reply_markup=kb_main)
            else:
                logger.error(
                    f"При регистрации пользователя {message.from_user.username} произошла ошибка в {datetime.now()}")
                await message.answer(
                    'Произошла непредвиденная ошибка, мы уже знаем о ней и скоро она будет исправлена.')
    except:
        logger.error(
            f"При проверки подписки пользователя {message.from_user.username} произошла ошибка в {datetime.now()}")
        await message.answer('Произошла непредвиденная ошибка, мы уже знаем о ней и скоро она будет исправлена.')




@dp.message(StateFilter(None), F.text.lower() == "каталог")
async def shop(message: types.Message, state: FSMContext):
    result = await get_category_list()
    response = result[0]
    resp = result[1]

    if resp == 200:
        builder = InlineKeyboardBuilder()
        for btn in response["data"][:5]:
            builder.row(types.InlineKeyboardButton(
                text=f"{btn}", callback_data=f"category_{btn}_{5}")
            )
        builder.row(types.InlineKeyboardButton(text=f"➡️", callback_data=f"category_next_{5}"))
        await message.answer(text='Какая категория товаров Вас интересует?', reply_markup=builder.as_markup())

    else:
        logger.error(f"При попытке получить категории в каталоге произошла ошибка в {datetime.now()}")
        await message.answer('Произошла непредвиденная ошибка, мы уже знаем о ней и скоро она будет исправлена.')


@dp.callback_query(StateFilter(None), F.data.startswith("category_"))
async def category_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.split('_')[1]
    position = int(callback.data.split('_')[2])
    result = await get_category_list()
    response = result[0]

    await inline_pagination_buttons(callback_data, position, response, callback, "subcategory", "category", None, None)


@dp.callback_query(StateFilter(None), F.data.startswith("subcategory_"))
async def subcategory_callback_handler(callback: types.CallbackQuery, state: FSMContext):
    callback_data = callback.data.split('_')[1]
    try:
        position = int(callback.data.split('_')[2])
    except ValueError:
        position = 10
        callback_data = '➡'
    except IndexError:
        position = -5
        callback_data = '⬅'
    try:
        category_name = int(callback.data.split('_')[2])
        category_name = callback.data.split('_')[3]
    except ValueError:
        category_name = callback.data.split('_')[2]
    except IndexError:
        category_name = callback.data.split('_')[1]

    result = await get_subcategory_list(category_name)
    response = result[0]
    await inline_pagination_buttons(callback_data, position, response, callback, None, "subcategory", category_name,
                                    state)


@dp.message(StateFilter(ShopState), F.text.lower() == "нет")
async def return_main_menu(message: Message, state: FSMContext):
    await message.answer(
        text="Тогда я предлагаю Вам вернуться в главное меню.\n\n"
             "Пожалуйста, выберите одно действие из списка ниже:",
        reply_markup=kb_main
    )
    await state.clear()


@dp.message(ShopState.show_goods, F.text.lower() == "да")
async def show_goods(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    subcategory = user_data["chosen_subcategory"]
    result = await get_goods_list(subcategory)
    if len(result['data']) != 0:
        for goods in result['data']:
            if goods["image_url"]:
                await send_photo(message, goods, None)
            else:
                await message.answer(
                    f'Название:{goods["name"]}\nЦена:{goods["price"]}\nОписание:{goods["description"]}')
        logger.info(f"Пользователь выбрал категорию: {subcategory}")
        await message.answer(f'Это все товары в: {subcategory}', reply_markup=kb_main)
        await state.set_state(ShopState.add_goods)
    else:
        await message.answer(f'В категории {subcategory} нет товаров', reply_markup=kb_main)
        await state.clear()


@dp.callback_query(ShopState.add_goods, F.data.startswith("goods_"))
async def add_goods_in_basket(callback: types.CallbackQuery, state: FSMContext):
    goods_id = callback.data.split('_')[1]
    await state.update_data(goods_id=goods_id)
    logger.info(f"Пользователь выбрал товар id: {goods_id}")
    await callback.message.answer("Укажите необходимое количество", reply_markup=None)
    await state.set_state(ShopState.quantity_goods)


@dp.message(ShopState.quantity_goods)
async def select_quantity_goods(message: types.Message, state: FSMContext):
    try:
        quantity_goods = int(message.text)
        await state.update_data(quantity_goods=quantity_goods)
        await message.answer('Вы выбрали количество товара\nПодтверждаете заказ?', reply_markup=kb_confirmation)
        await state.set_state(ShopState.confirmation_order)
    except ValueError:
        await message.answer('Введите целое число')


@dp.message(ShopState.confirmation_order, F.text.lower() == "да")
async def confirmation_order(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    goods_id = state_data["goods_id"]
    quantity_goods = state_data["quantity_goods"]
    telegram_id = message.from_user.id
    result = await goods_in_basket(goods_id, telegram_id, quantity_goods)
    logger.info(f"Пользователь {message.from_user.id} подтвердил заказ в {datetime.now()}")
    await message.answer(f'{result["data"]}', reply_markup=kb_main)
    await state.clear()


@dp.message(F.text.lower() == "корзина")
async def basket(message: types.Message, state: FSMContext):
    telegram_id = message.from_user.id
    result = await get_basket(telegram_id)

    if len(result['data']) == 0:
        await message.answer("Ваша корзина пуста", reply_markup=kb_main)
    else:
        await state.set_state(BasketState.show_basket)
        for goods in result['data']:
            result = await get_detail_goods(goods['products'])
            if result["data"]["image"]:
                await send_photo(message, result['data'], goods['id'])
            else:
                await message.answer(f'Название:{result["data"]["name"]}\nЦена:{result["data"]["price"]}\n'
                                     f'Описание:{result["data"]["description"]}')

        await message.answer(f'Хотите оформить заказ?', reply_markup=kb_confirmation)


@dp.message(BasketState.show_basket, F.text.lower() == "да")
async def select_delivery_address(message: types.Message, state: FSMContext):
    await state.set_state(BasketState.delivery_address)
    await message.answer('Введите адрес доставки', reply_markup=kb_main)
    logger.info(f"Пользователь {message.from_user.id} решил оформить заказ в {datetime.now()}")


@dp.message(BasketState.show_basket, F.text.lower() == "нет")
async def cancel_order(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer('Конечно, приходите еще, мы Вам всегда рады.', reply_markup=kb_main)


@dp.message(BasketState.delivery_address)
async def select_recipient_name(message: types.Message, state: FSMContext):
    await state.update_data(delivery_address=message.text)
    await state.set_state(BasketState.recipient_name)
    await message.answer('Введите имя получателя', reply_markup=kb_main)


@dp.message(BasketState.recipient_name)
async def select_recipient_phone(message: types.Message, state: FSMContext):
    await state.update_data(recipient_name=message.text)
    await message.answer('Введите номер телефона получателя.\nНапример:\n+7 (812) 000-00-00\n+78120000000\n88120000000',
                         reply_markup=kb_main)
    await state.set_state(BasketState.recipient_phone)


@dp.message(BasketState.recipient_phone)
async def select_all_data_about_recipient(message: types.Message, state: FSMContext):
    phone_number_validate = validate_phone_number(message.text)

    if phone_number_validate:
        await state.update_data(recipient_phone=message.text)
        order_data = await state.get_data()

        result = await get_payment(message.from_user.id, order_data)
        await state.clear()
        await message.answer(f'Ваша ссылка для оплаты:\n{result["data"]}', reply_markup=kb_main)
        logger.info(
            f"Пользователь {message.from_user.id} ввел данные для заказа и получил ссылку на оплату в {datetime.now()}")
    else:
        await message.answer('Номер введен некорректно.\nВведите номер телефона получателя', reply_markup=kb_main)


@dp.callback_query(BasketState.show_basket, F.data.startswith("del_goods_"))
async def delete_goods_from_basket(callback: types.CallbackQuery, state: FSMContext):
    basket_id = callback.data.split('_')[2]
    telegram_id = callback.from_user.id
    result = await del_goods_from_basket(basket_id, telegram_id)
    await callback.message.answer(f'{result["data"]}')
    logger.info(f"Пользователь {callback.from_user.id} решил оформить заказ в {datetime.now()}")


@dp.callback_query(StateFilter(FAQState, None), F.data.startswith("exit_faq"))
async def exit_faq(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer(f'Вы в главном меню', reply_markup=kb_main)
    await state.clear()


@dp.message(F.text.lower() == "faq")
async def faq(message: types.Message, state: FSMContext):
    await state.set_state(FAQState.show_faq)
    response = await get_faq_questions()
    builder = InlineKeyboardBuilder()
    for btn in response["data"]:
        builder.row(types.InlineKeyboardButton(text=f"{btn['question']}", callback_data=f"faq_{btn['id']}"))
    builder.row(types.InlineKeyboardButton(text=f"Мне все понятно, спасибо.", callback_data=f"exit_faq"))
    await message.answer(text='Часто задаваемые вопросы', reply_markup=builder.as_markup())


@dp.callback_query(FAQState.show_faq, F.data.startswith("faq_"))
async def first_faq_answer(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(FAQState.first_faq_answer)
    builder = InlineKeyboardBuilder()
    question_id = callback.data.split('_')[1]
    response = await get_all_answer_on_first_faq_question(int(question_id))
    if response["data"]["question"] is not None:
        await callback.message.edit_text(text=response["data"]["answer"], reply_markup=builder.as_markup())
        new_questions = await get_all_questions_on_first_faq_answer((response["data"]["id"]))
        for btn in new_questions["data"]:
            builder.row(types.InlineKeyboardButton(text=f"{btn['title']}", callback_data=f"new_faq_{btn['id']}"))
        builder.row(types.InlineKeyboardButton(text=f"Мне все понятно, спасибо.", callback_data=f"exit_faq"))
        await callback.message.edit_reply_markup(reply_markup=builder.as_markup())
    else:
        builder.row(types.InlineKeyboardButton(text=f"Мне все понятно, спасибо.", callback_data=f"exit_faq"))
        await callback.message.edit_text(text="На этот вопрос у меня нет ответа", reply_markup=builder.as_markup())


@dp.callback_query(FAQState.first_faq_answer, F.data.startswith("new_faq_"))
async def second_faq_answer(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()
    question_id = callback.data.split('_')[2]
    response = await get_last_faq_answer(int(question_id))
    builder = InlineKeyboardBuilder()
    if response["data"]["question"] is not None:
        builder.row(types.InlineKeyboardButton(text=f"Мне все понятно, спасибо.", callback_data=f"exit_faq"))
        await callback.message.edit_text(text=response["data"]["answer"], reply_markup=builder.as_markup())
    else:
        builder.row(types.InlineKeyboardButton(text=f"Мне все понятно, спасибо.", callback_data=f"exit_faq"))
        await callback.message.edit_text(text="На этот вопрос у меня нет ответа", reply_markup=builder.as_markup())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
