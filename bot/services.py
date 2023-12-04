import re

from aiogram import types
from aiogram.client.session import aiohttp
from aiogram.types import URLInputFile
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states import ShopState
from keyboards_config import kb_confirmation
from config import BASE_URL


async def get_channels_id_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{BASE_URL}shop/subscribe_approved_channels/", headers={'Content-Type': 'application/json'},
                json={}
        ) as resp:
            response = await resp.json()
    return response


async def register(tg_id, username, name):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{BASE_URL}accounts/authentication/auth/",
                                headers={'Content-Type': 'application/json'},
                                json={
                                    "telegram_id": tg_id, "username": username, "name": name
                                }
                                ) as resp:
            ...
    return resp


async def get_category_list():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{BASE_URL}shop/shop/get_category/", headers={'Content-Type': 'application/json'}, json={}
        ) as resp:
            response = await resp.json()
    resp = 200
    return response, resp


async def get_subcategory_list(category_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{BASE_URL}shop/shop/get_subcategory/", headers={'Content-Type': 'application/json'},
                json={"category_name": category_name}
        ) as resp:
            response = await resp.json()
    resp = 200
    return response, resp


async def get_goods_list(subcategory_name):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{BASE_URL}shop/shop/get_goods/", headers={'Content-Type': 'application/json'},
                json={"subcategory_name": subcategory_name}
        ) as resp:
            response = await resp.json()
    return response


async def goods_in_basket(goods_id, user_tg_id, quantity_goods):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{BASE_URL}shop/shop/add_goods_in_basket/", headers={'Content-Type': 'application/json'},
                json={"goods_id": goods_id, "telegram_id": user_tg_id, "quantity_goods": quantity_goods}
        ) as resp:
            response = await resp.json()
    return response


async def get_basket(telegram_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{BASE_URL}shop/shop/get_basket/", headers={'Content-Type': 'application/json'},
                json={"telegram_id": telegram_id}
        ) as resp:
            response = await resp.json()
    return response


async def get_detail_goods(goods_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{BASE_URL}shop/shop/get_detail_goods/", headers={'Content-Type': 'application/json'},
                json={"goods_id": goods_id}
        ) as resp:
            response = await resp.json()
    return response


async def send_photo(message, goods, basket_id):
    builder = InlineKeyboardBuilder()

    try:
        image_from_url = URLInputFile(f"{BASE_URL + goods['image_url']}")
        builder.row(types.InlineKeyboardButton(text=f"Добавить в корзину", callback_data=f"goods_{goods['id']}"))
        # await message.answer_photo(image_from_url,
        #                            caption=f"Название: {goods['name']}\nЦена: {goods['price']}\nОписание: {goods['description']}",
        #                            reply_markup=builder.as_markup()
        #                            )
    except:
        image_from_url = URLInputFile(f"{BASE_URL + goods['image']}")
        builder.row(types.InlineKeyboardButton(text=f"Удалить из корзины", callback_data=f"del_goods_{basket_id}"))
    await message.answer_photo(image_from_url,
                               caption=f"Название: {goods['name']}\nЦена: {goods['price']}\nОписание: {goods['description']}",
                               reply_markup=builder.as_markup()
                               )


async def del_goods_from_basket(basket_id, telegram_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{BASE_URL}shop/shop/del_goods_from_basket/", headers={'Content-Type': 'application/json'},
                json={"basket_id": basket_id, "telegram_id": telegram_id}
        ) as resp:
            response = await resp.json()
    return response


async def get_payment(telegram_id, order_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(
                f"{BASE_URL}shop/shop/get_payment/", headers={'Content-Type': 'application/json'},
                json={"telegram_id": telegram_id, "order_data": order_data}
        ) as resp:
            response = await resp.json()
    return response


async def get_faq_questions():
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{BASE_URL}shop/faq/get_faq/", headers={'Content-Type': 'application/json'},
                json={}
        ) as resp:
            response = await resp.json()
    return response


async def get_all_answer_on_first_faq_question(question_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{BASE_URL}shop/faq/get_all_answer_on_first_faq_question/",
                headers={'Content-Type': 'application/json'},
                json={"question_id": question_id}
        ) as resp:
            response = await resp.json()
    return response


async def get_all_questions_on_first_faq_answer(answer_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{BASE_URL}shop/faq/get_all_questions_on_first_faq_answer/",
                headers={'Content-Type': 'application/json'},
                json={"answer_id": answer_id}
        ) as resp:
            response = await resp.json()
    return response


async def get_last_faq_answer(question_id):
    async with aiohttp.ClientSession() as session:
        async with session.get(
                f"{BASE_URL}shop/faq/get_last_faq_answer/", headers={'Content-Type': 'application/json'},
                json={"question_id": question_id}
        ) as resp:
            response = await resp.json()
    return response


def validate_phone_number(phone_number):
    pattern = r"^(?:\+7 \(\d{3}\) \d{3}-\d{2}-\d{2}|\+?\d{11}|8\d{10})$"
    if re.match(pattern, phone_number):
        return True
    else:
        return False


async def inline_pagination_buttons(callback_data, position, response, callback, new_category, category, category_name,
                                    state):
    builder = InlineKeyboardBuilder()
    if category_name != None:

        if callback_data == "next" or callback_data == "➡":

            if len(response["data"]) < position + 5 or len(response["data"]) == position + 5:

                for btn in response["data"][-(len(response["data"]) - position):]:
                    builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{category}_{btn}_{5}"))
                if category_name:

                    builder.row(types.InlineKeyboardButton(text=f"⬅️", callback_data=f"{category}_{category_name}"))
                else:

                    builder.row(
                        types.InlineKeyboardButton(text=f"⬅️", callback_data=f"{category}_⬅_{position - 5}"))
            else:

                for btn in response["data"][position:position + 5]:
                    builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{category}_{btn}_{5}"))
                builder.row(types.InlineKeyboardButton(text=f"➡️",
                                                       callback_data=f"{category}_➡_{position + 5}_{category_name}"))
                builder.row(types.InlineKeyboardButton(text=f"⬅️",
                                                       callback_data=f"{category}_⬅_{position - 5}_{category_name}"))
            await callback.message.edit_reply_markup(reply_markup=builder.as_markup())

        elif callback_data == "previous" or callback_data == "⬅":
            if position == 0 or position == -5:
                for btn in response["data"][:5]:
                    builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{category}_{btn}_{5}"))
                builder.row(
                    types.InlineKeyboardButton(text=f"➡️", callback_data=f"{category}_➡_{5}_{category_name}"))
            else:
                if len(response["data"][position:position - 4]) == 0:
                    for btn in response["data"][-(len(response["data"]) - position):]:
                        builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{category}_{btn}_{5}"))
                    builder.row(
                        types.InlineKeyboardButton(text=f"⬅️", callback_data=f"{category}_⬅_{position - 5}"))
                else:
                    for btn in response["data"][position:position - 4]:
                        builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{category}_{btn}_{5}"))
                    builder.row(types.InlineKeyboardButton(text=f"➡️", callback_data=f"{category}_➡_{position + 5}"))
                    builder.row(
                        types.InlineKeyboardButton(text=f"⬅️", callback_data=f"{category}_⬅_{position - 5}"))
            await callback.message.edit_reply_markup(reply_markup=builder.as_markup())

        else:
            if new_category != None:
                new_btns = await get_subcategory_list(callback_data)

                response = new_btns[0]
                for btn in response["data"][:5]:
                    builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{new_category}_{btn}_{5}"))
                builder.row(types.InlineKeyboardButton(text=f"➡️",
                                                       callback_data=f"{new_category}_➡_{callback_data}"))  # {position + 5}"))
                await callback.message.edit_text(f"{callback_data}", reply_markup=builder.as_markup())

            else:
                # keyboard = types.ReplyKeyboardMarkup(keyboard=confirmation_buttons, resize_keyboard=True,
                #                                      one_time_keyboard=True)
                await callback.message.answer(f'Вы выбрали: {callback_data}?', reply_markup=kb_confirmation)
                await state.update_data(chosen_subcategory=callback_data)
                await state.set_state(ShopState.show_goods)

    else:
        if callback_data == "next":
            if len(response["data"]) < position + 5 or len(response["data"]) == position + 5:
                for btn in response["data"][-(len(response["data"]) - position):]:
                    builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{category}_{btn}_{5}"))
                if category_name:

                    builder.row(types.InlineKeyboardButton(text=f"⬅️", callback_data=f"{category}_{category_name}"))
                else:

                    builder.row(
                        types.InlineKeyboardButton(text=f"⬅️", callback_data=f"{category}_previous_{position - 5}"))
            else:

                for btn in response["data"][position:position + 5]:
                    builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{category}_{btn}_{5}"))
                builder.row(types.InlineKeyboardButton(text=f"➡️", callback_data=f"{category}_next_{position + 5}"))
                builder.row(types.InlineKeyboardButton(text=f"⬅️", callback_data=f"{category}_previous_{position - 5}"))
            await callback.message.edit_reply_markup(reply_markup=builder.as_markup())

        elif callback_data == "previous":

            if position == 0 or position == -5:
                for btn in response["data"][:5]:
                    builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{category}_{btn}_{5}"))
                # builder.row(types.InlineKeyboardButton(text=f"➡️", callback_data=f"{category}_next_{5}"))
                builder.row(
                    types.InlineKeyboardButton(text=f"➡️", callback_data=f"{category}_next_{5}_{category_name}"))
            else:
                if len(response["data"][position:position - 4]) == 0:
                    for btn in response["data"][-(len(response["data"]) - position):]:
                        builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{category}_{btn}_{5}"))
                    builder.row(
                        types.InlineKeyboardButton(text=f"⬅️", callback_data=f"{category}_previous_{position - 5}"))
                else:
                    for btn in response["data"][position:position - 4]:
                        builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{category}_{btn}_{5}"))
                    builder.row(types.InlineKeyboardButton(text=f"➡️", callback_data=f"{category}_next_{position + 5}"))
                    builder.row(
                        types.InlineKeyboardButton(text=f"⬅️", callback_data=f"{category}_previous_{position - 5}"))
            await callback.message.edit_reply_markup(reply_markup=builder.as_markup())

        else:
            if new_category != None:
                new_btns = await get_subcategory_list(callback_data)
                response = new_btns[0]
                for btn in response["data"][:5]:
                    builder.row(types.InlineKeyboardButton(text=f"{btn}", callback_data=f"{new_category}_{btn}_{5}"))
                builder.row(types.InlineKeyboardButton(text=f"➡️",
                                                       callback_data=f"{new_category}_next_{callback_data}"))  # {position + 5}"))
                await callback.message.edit_text(f"{callback_data}", reply_markup=builder.as_markup())

            else:
                await callback.message.answer(f'Вы выбрали: {callback_data}?')
