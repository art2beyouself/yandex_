import asyncio
import json
import validators
import time as timea


from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from main import seleniums
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Checkbox, ManagedCheckboxAdapter
from aiogram_dialog.widgets.text import Const
import operator

from aiogram_dialog.widgets.kbd import Multiselect
from aiogram_dialog.widgets.text import Format

time = []
loop = asyncio.get_event_loop()
bot = Bot(token="6056925922:AAGUDyJGdiOZ8ATTBzTHNGkJ3hhS5iM_RZs", parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, loop=loop, storage=MemoryStorage())

class StateGroupExample(StatesGroup):
    add_url = State() #создаёте состояние
    parsing = State()
    get_date = State()


async def check_changed(event: ChatEvent, checkbox: ManagedCheckboxAdapter, manager: DialogManager):
    print("Check status changed:", checkbox.is_checked())


check = Checkbox(
    Const("✓  Checked"),
    Const("Unchecked"),
    id="check",
    default=True,  # so it will be checked by default,
    on_state_changed=check_changed,)

@dp.message_handler()
async def help(message: types.Message, state: FSMContext):
    if message.text == 'Начать парсинг':
        with open("users_db.json") as file:
            data = json.load(file)

        start_buttons = ["Главное меню"]
        print(start_buttons)
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)
        await message.answer("Укажите период: по шаблону формат даты такой 2022-01-01/2023-02-01", reply_markup=keyboard)
        await StateGroupExample.get_date.set()  # теперь бот б

    elif message.text == 'Добавить ссылку':
        await message.answer(text='Отправьте имя ресурса и ссылку в формате: \n название:ссылка')
        await StateGroupExample.add_url.set()
    else:
        start_buttons = ["Начать парсинг", "Добавить ссылку", "Главное меню"]
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*start_buttons)

        with open("users_db.json") as file:
            data = json.load(file)

        try:
            data[message.from_user.username]
        except KeyError:
            data[f"{message.from_user.username}"] = {}

            with open('users_db.json', 'w') as f:
                json.dump(data, f)

        await message.answer(f"{message.from_user.username}, Вы в главном меню: - выберите в меню желаемое действие", reply_markup=keyboard)


@dp.message_handler(state=StateGroupExample.get_date)
async def parsing(message: types.Message, state: FSMContext):
    with open("users_db.json") as file:
        data = json.load(file)
    for i in data[message.from_user.username]:
        if i == message.text:
            print(i)

            start_buttons = ["Кнопки недоступны"]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*start_buttons)
            await message.answer(f"{message.from_user.username}, Пожалуйста ждите", reply_markup=keyboard)

            with open("users_db.json") as file:
                data = json.load(file)

            data = seleniums(data[message.from_user.username][message.text], time[0], i)
            start_buttons = ["Начать парсинг", "Добавить ссылку", "Главное меню"]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*start_buttons)
            await message.answer(f"{data}", reply_markup=keyboard)
            await state.finish()
            time.clear()
            return

    time.clear()
    data2 = message.text
    print(data2)
    flag = True


    try:
        one = data2.partition("/")[0]
        two = data2.partition("/")[2]
        print(one)
        print(two)
        timea.strptime(one, "%Y-%m-%d")
        timea.strptime(two, "%Y-%m-%d")
    except:
        if message.text == 'Главное меню':
            flag = False
            await state.finish()
            start_buttons = ["Начать парсинг", "Добавить ссылку", "Главное меню"]
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*start_buttons)
            await message.answer(
                f"{message.from_user.username}, Вы в главном меню: - выберите в меню желаемое действие",
                reply_markup=keyboard)
        else:
            flag = False
            await message.answer("Неверная дата, попробуйте еще!")


    if "/" in data2:
        if flag == True:
            time.append(data2)
            await state.finish()
            start_buttons = data[f"{message.from_user.username}"]
            print(start_buttons)
            keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
            keyboard.add(*start_buttons)
            await message.answer("Выберите в меню url для парсинга", reply_markup=keyboard)
            await StateGroupExample.get_date.set()




# @dp.message_handler(state=StateGroupExample.parsing)
# async def parsing(message: types.Message, state: FSMContext):
#         print(StateGroupExample.get_date)
#         with open("users_db.json") as file:
#             data = json.load(file)
#         for i in data[message.from_user.username]:
#             if i == message.text:
#                 print(i)
                # start_buttons = ["Начать парсинг", "Добавить ссылку", "Главное меню"]
                # keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
                # keyboard.add(*start_buttons)
                # await message.answer(f"{message.from_user.username}, Пожалуйста ждите", reply_markup=keyboard)
                #
                # with open("users_db.json") as file:
                #     data = json.load(file)
                #
                # data = seleniums(data[message.from_user.username][message.text])
                # await message.answer(f"{data}", reply_markup=keyboard)
#
#             await state.finish()

@dp.message_handler(state=StateGroupExample.add_url)
async def help(message: types.Message, state: FSMContext):
    if "Главное меню" in message.text:
        await state.finish()

    if ":" in message.text:
        name = message.text.partition(":")[0]
        www = message.text.partition(":")[2]
        data = validators.url(www)
        if data is True:
            print(data)
            print(name)
            print(www)
            with open("users_db.json") as file:
                data = json.load(file)

            # data[message.from_user.username] = {f'{name}': f'{www}'}
            new_dict = {f'{name}': f'{www}'}

            data[message.from_user.username].update(new_dict)

            # data[message.from_user.username] = {f'{name}': f'{www}'}
            # print(data)
            with open('users_db.json', 'w') as f:
                json.dump(data, f)

            await message.answer(text='Ссылка добавлена: \n доступна в Парсинг листе')
            await state.finish()
        else:
            await message.answer(text='Ссылка не добавлена: \n неверный формат')
    else:
        await message.answer(text='Ссылка не добавлена: \n неверный формат')


# @dp.message_handler(Text(equals="Начать парсинг"))
# async def get_discount_sneakers(message: types.Message):
#     # await message.answer("Please waiting...")
#
#     with open("users_db.json") as file:
#         data = json.load(file)
#
#
#     start_buttons = data[f"{message.from_user.username}"]
#     print(start_buttons)
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     keyboard.add(*start_buttons)
#
#     await message.answer("Выберите в меню желаемое действие", reply_markup=keyboard)

    # seleniums()

    # with open("result_data.json") as file:
    #     data = json.load(file)
    #
    # for item in data:
    #     card = f"{hlink(item.get('title'), item.get('link'))}\n" \
    #            f"{hbold('Категория: ')} {item.get('category')}\n" \
    #            f"{hbold('Прайс: ')} {item.get('price_base')}\n" \
    #            f"{hbold('Прайс со скидкой: ')} -{item.get('discount_percent')}%: {item.get('price_sale')}🔥"

        # await message.answer(card)


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
