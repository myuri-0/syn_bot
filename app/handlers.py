from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardMarkup, InlineKeyboardButton

import pandas as pd

router = Router()

# Глобальная переменная для отслеживания текущего вопроса
current_question_index = {}

# Глобальная переменная для хранения ответов пользователей
user_answers = {}

current_test = {}

# Функция для загрузки вопросов и вариантов ответов из Excel
def load_questions_and_answers(file_path, question_col, options_cols):
    """Функция для загрузки вопросов и вариантов ответов из указанных колонок Excel файла"""
    try:
        df = pd.read_excel(file_path)
        if question_col in df.columns and all(col in df.columns for col in options_cols):
            questions = []
            for _, row in df.iterrows():
                question = row[question_col]
                options = [str(row[col]) for col in options_cols if not pd.isna(row[col])]
                questions.append((question, options))
            return questions
        else:
            print(f"Файл должен содержать колонку '{question_col}' и все указанные колонки для вариантов ответов: {options_cols}.")
            return []
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return []

# Укажите название колонки для вопросов и список колонок для вариантов ответов
question_column = 'question'
options_columns = [f'option{i}' for i in range(1, 11)]  # Поддержка до 10 вариантов ответов

# Загружаем вопросы и ответы из Excel при старте приложения
questions_and_answers = load_questions_and_answers('app/voprosy.xlsx', question_column, options_columns)
humanities = load_questions_and_answers('app/Humanities.xlsx', question_column, options_columns)

@router.message(CommandStart())
async def cmd_start(message: Message):
    user_id = message.from_user.id
    current_question_index[user_id] = 0  # Устанавливаем первый вопрос для пользователя
    user_answers[user_id] = []  # Инициализируем список для ответов пользователя
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Приступить к тесту", callback_data="start_test")]
    ])
    await message.answer('Привет!')
    await message.answer('Готов приступить к тесту?', reply_markup=keyboard)

async def send_question(message, user_id):
    """Отправляет текущий вопрос пользователю"""
    index = current_question_index.get(user_id, 0)
    if index < len(questions_and_answers):
        question, options = questions_and_answers[index]
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=option, callback_data=f"answer_{index}_{i}")]
            for i, option in enumerate(options)
        ])
        await message.answer(question, reply_markup=keyboard)
    else:
        # Сохранение ответов пользователя в Excel файл
        save_answers_to_excel(user_id)
        # Выдача результата теста
        result = calculate_result(user_id)
        await message.answer(f"Тест завершён. Ваш результат: {result}")


@router.callback_query(F.data == "start_test")
async def start_test(callback: CallbackQuery):
    user_id = callback.from_user.id
    await callback.answer()
    await send_question(callback.message, user_id)

@router.callback_query(F.data == "start_second_test")
async def start_second_test(callback: CallbackQuery):
    user_id = callback.from_user.id
    current_test[user_id] = 2
    current_question_index[user_id] = 0  # Сбросить индекс вопросов для второго теста
    user_answers[user_id] = []  # Сбросить ответы
    await callback.answer()
    await send_question(callback.message, user_id)

@router.callback_query(F.data.startswith("answer_"))
async def handle_answer(callback: CallbackQuery):
    user_id = callback.from_user.id
    data = callback.data.split("_")
    question_index = int(data[1])
    selected_option_index = int(data[2])

    # Логика обработки ответа
    selected_option = questions_and_answers[question_index][1][selected_option_index]
    user_answers[user_id].append({
        "user_id": user_id,
        "question": questions_and_answers[question_index][0],
        "answer": selected_option
    })
    print(f"Пользователь {user_id} выбрал: {selected_option}")

    # Переходим к следующему вопросу
    await callback.message.edit_reply_markup(reply_markup=None)
    current_question_index[user_id] = question_index + 1

    await callback.answer()  # Закрыть уведомление
    await send_question(callback.message, user_id)

def save_answers_to_excel(user_id):
    """Сохраняет ответы пользователя в Excel файл"""
    if user_id in user_answers:
        answers = user_answers[user_id]
        df = pd.DataFrame(answers)
        file_name = f"app/otvety.xlsx"
        df.to_excel(file_name, index=False)
        print(f"Ответы пользователя {user_id} сохранены в файл {file_name}.")

def calculate_result(user_id):
    """Вычисляет результат теста на основе ответов пользователя"""
    if user_id not in user_answers:
        return "Результаты недоступны."

    # расчёт результата
    answers = user_answers[user_id]
    result_mapping = {
        "a": "Гуманитарные науки и педагогика. Вы любите помогать другим, делиться знаниями и заботиться о развитии людей.",
        "b": "Искусство, культура и медиа. Творчество и искусство — это ваша стихия. Вы стремитесь самовыражаться и вдохновлять.",
        "c": "Юриспруденция и безопасность. Вы цените порядок, законы и готовы защищать права людей.",
        "d": "Инженерия и технологии. Вы любите работать с техникой, проектировать и разрабатывать новые решения.",
        "e": "Информационные технологии и цифровые технологии. Вас привлекает мир ИT, программирования и инноваций.",
        "f": "Экономика и управление. Вы видите себя лидером, организатором",
        "g": "Менеджмент и предпринимательство. Вы видите себя организатором или предпринимателем",
        "h": "Здравоохранение и медицина. Вам важно помогать людям быть здоровыми и счастливыми.",
        "i": "Спорт и физическая культура. Активный образ жизни, работа над телом и спорт мотивируют вас.",
        "j": "Коммуникации, маркетинг и лингвистика."
    }

    counts = {}
    for answer in answers:
        option = answer["answer"]
        counts[option] = counts.get(option, 0) + 1

    # Определяем направление с максимальным количеством ответов
    if counts:
        best_match = max(counts, key=counts.get)
        return result_mapping.get(str(best_match)[0], "Общее направление")

    return "Результаты не определены."
