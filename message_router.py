from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import Message
import keyboards as kb

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(f"Hello world")



@router.message(Command("тест"))
async def cmd_start(message: Message):
    await message.answer(f"стартуем")

