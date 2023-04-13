from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

cancel_btn_text = "❌ Отменить"

add_worker = InlineKeyboardButton('1️⃣ Добавить', callback_data='add_worker')
users_progress = InlineKeyboardButton('2️⃣ Прогрессы', callback_data='users_progress')
messages = InlineKeyboardButton('3️⃣ Сообщения', callback_data='messages')
answer_question = InlineKeyboardButton('4️⃣ Дать ответ на сообщения', callback_data='answer_question')
add_worker_kb = InlineKeyboardMarkup().add(add_worker, users_progress, messages, answer_question)

add_worker_done = InlineKeyboardButton('✅ Верно!', callback_data='add_worker_done')
add_worker_done_kb = InlineKeyboardMarkup().add(add_worker_done)

acquaintance = InlineKeyboardButton('😉 Рад знакомству!', callback_data='acquaintance')
acquaintance_kb = InlineKeyboardMarkup().add(acquaintance)

office_testing = InlineKeyboardButton('1️⃣ Приступить!', callback_data='office_testing')
office_testing_kb = InlineKeyboardMarkup().add(office_testing)

acquaintance_next = InlineKeyboardButton('1️⃣ К тесту!', callback_data='acquaintance_next')
acquaintance_reset = InlineKeyboardButton('2️⃣ Хочу узнать офис', callback_data='office_start')
acquaintance_next_reset_kb = InlineKeyboardMarkup().add(acquaintance_next, acquaintance_reset)

ask_question = InlineKeyboardButton('❓ Задать вопрос', callback_data='ask_question')
messages = InlineKeyboardButton('📨 Сообщения!', callback_data='messages')
code = InlineKeyboardButton('🔏 Ввести код', callback_data='code')
profile_acquaintance_reset = InlineKeyboardButton('❌ Сбросить прогресс', callback_data='acquaintance_reset')
ask_question_kb = InlineKeyboardMarkup().add(ask_question, messages, code, profile_acquaintance_reset)

office_testing_continue = InlineKeyboardButton('1️⃣ Продолжить', callback_data='office_testing')
office_testing_reset = InlineKeyboardButton('2️⃣ Ознакомиться заново', callback_data='acquaintance_reset')
office_testing_new_kb = InlineKeyboardMarkup().add(office_testing_continue, office_testing_reset)

works = InlineKeyboardButton('✨ Ясно!', callback_data='works')
works_kb = InlineKeyboardMarkup().add(works)

acquaintance_reset_1 = InlineKeyboardButton('1️⃣ Заново', callback_data='acquaintance_reset')
office_testing_1 = InlineKeyboardButton('➡️ Знакомство с офисом', callback_data='office_start')
acquaintance_next_reset_1_kb = InlineKeyboardMarkup().add(acquaintance_reset_1, office_testing_1)