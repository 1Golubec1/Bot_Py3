from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import *
from functions import FUNCTIONS
import sqlite3
func = FUNCTIONS
connect = sqlite3.connect(name_bd)
cursor = connect.cursor()
bl = []
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)



@dp.message_handler(commands=['start'])
async def start_menu(message: types.Message):
    user_id = str(message.from_user.id)
    func.Connect(connect, cursor)
    if func.check_pl(connect, cursor, user_id):
        func.save_info(connect, user_id, "state", "START")
        await message.answer("Вы успешно авторизовались")
    else:
        await message.answer("Вы уже нажимали на старт")

@dp.message_handler(commands=['compel'])
async def cсomp(message: types.Message):
    user_id = str(message.from_user.id)
    func.save_info(connect, user_id, "state", "COMPEL")
    await message.answer("Напишите свой код")

@dp.message_handler(commands=['comands'])
async def comand(message: types.Message):
    user_id = str(message.from_user.id)
    func.save_info(connect, user_id, "state", "ADDCOMAND")
    await message.answer("Напишите функции, которые хотели бы сохранить")

@dp.message_handler()
async def main(message: types.Message):
    from convert import CONVERT
    conv = CONVERT
    user_id = str(message.from_user.id)
    if message.text and func.get_variable(connect, user_id, "state") == "COMPEL":
        conv_file = open("convert.py", "w", encoding="UTF-8")
        base_conv_file = open("base_conv").read()
        conv_file.write(f"{base_conv_file}\n")
        conv_file.close()
        conv_file = open("convert.py", "a", encoding="UTF-8")
        text = "".join(list(map(lambda x: f"        {x}\n",message.text.replace("print", "return").split("\n"))))
        conv_file.write(f"{text}")
        conv_file.close()
        if "return" in text:
            print(text)
            print(str(conv.conv()))
            await message.answer(str(conv.conv()), reply_markup=types.ReplyKeyboardRemove())


executor.start_polling(dp)