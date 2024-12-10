from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton


@dp.message_handler(commands=['start'])
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
