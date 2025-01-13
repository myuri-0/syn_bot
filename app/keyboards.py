from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton,
                           InlineKeyboardMarkup, InlineKeyboardButton)

tests = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Приступить к тесту', callback_data='testss')],
                                              [InlineKeyboardButton(text='Нет', callback_data='stop_test')]])




