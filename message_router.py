from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton
import keyboards as kb


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Hello world")

@router.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    kb = [
        [
            types.KeyboardButton(text="Узнать погоду"),
            types.KeyboardButton(text="А хта это такэ?")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb)

    await message.reply("Привет!\nЯ Эхобот от Skillbox!\nОтправь мне любое сообщение, а я тебе обязательно отвечу.",
                        reply_markup=keyboard)

@router.message(Command("тест"))
async def cmd_start(message: Message):
    await message.answer(f"стартуем")

