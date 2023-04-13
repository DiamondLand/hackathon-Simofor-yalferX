import psycopg2
import asyncio
import itertools
import configparser
import logging
import answers
import keyboards
import random

from aiofile import async_open
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.input_file import InputFile
from aiogram.dispatcher.filters.state import State, StatesGroup
from io import BytesIO
from PIL import Image
from base64 import b16decode as dec64


logging.basicConfig(level=logging.INFO)
config = configparser.ConfigParser()
config.read("settings.ini")

bot = Bot(token=config["Config"]["token"])
dp = Dispatcher(bot, storage=MemoryStorage())

connection = psycopg2.connect(
    user=config["Database"]["user"],
    password=config["Database"]["password"],
    database=config["Database"]["database"],
    host=config["Database"]["host"]
)
cursor = connection.cursor()
connection.autocommit = True


class AddWorker(StatesGroup):
    name = State()
    age = State()
    in_company_age = State()
    description = State()
    to_database = State()


class WorkerTesting(StatesGroup):
    first_person = State()
    second_person = State()
    third_person = State()
    fourth_person = State()
    fifth_person = State()


class OfficeTesting(StatesGroup):
    first_office = State()
    second_office = State()
    third_office = State()
    fourth_office = State()
    fifth_office = State()


class SendMessage(StatesGroup):
    on_sending = State()
    on_answer = State()
    on_answer_ans = State()


class EnterCode(StatesGroup):
    on_code = State()


@dp.message_handler(state='*', commands=keyboards.cancel_btn_text)
@dp.message_handler(Text(equals=keyboards.cancel_btn_text, ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply(
        "Заполнение формы было завершено!",
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    await bot.send_message(
        message.chat.id,
        answers.on_start,
        parse_mode="html"
    )


@dp.message_handler(commands=['panel'])
async def cmd_panel(message: types.Message):
    if str(message.chat.id) == str(config["Config"]["administrator_id"]):
        await bot.send_message(
            message.chat.id,
            answers.on_admin_panel,
            parse_mode="html",
            reply_markup=keyboards.add_worker_kb
        )
    else:
        progress_result = await basic_progress(member=message.chat)
        step_teory = progress_result[3] if int(progress_result[3]) > 0 else 0
        await bot.send_message(
            message.chat.id,
            answers.on_no_admin_panel.format(
                step=progress_result[2] if int(progress_result[2]) > 0 else 0,
                step_teory=step_teory if int(progress_result[3]) <= 5 else "5+",
                office_step=progress_result[4] if int(
                    progress_result[4]) > 0 else 0,
                step_office="пройдена" if int(
                    progress_result[5]) > 0 else "не пройдена",
                code="активирован" if int(
                    progress_result[7]) > 0 else "не активирован"
            ),
            parse_mode="html",
            reply_markup=keyboards.ask_question_kb
        )


@dp.message_handler(commands=['acquaintance'])
async def cmd_acquaintance(message: types.Message):
    await bot.send_message(
        message.chat.id,
        answers.on_ready,
        parse_mode="html",
        reply_markup=keyboards.works_kb
    )


@dp.message_handler(state=AddWorker.name)
async def add_name(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await bot.send_message(
            message.chat.id,
            answers.command_on_text_input,
            parse_mode="html"
        )
    else:
        name_surname = message.text.split()
        name_surname_to_cout = " ".join(name_surname)
        name_surname_to_isalpha = "".join(name_surname)
        if len(name_surname_to_cout.split()) == 2 and name_surname_to_isalpha.isalpha():
            async with state.proxy() as data:
                data['name'] = message.text
            await bot.send_message(
                message.chat.id,
                answers.on_add_worker_2,
                parse_mode="html"
            )
            await AddWorker.next()
        else:
            await bot.send_message(
                message.chat.id,
                "Имя и Фамилия должны быть написанны отдельно, через пробел и без лишних символов! Повторите попытку:",
                parse_mode="html"
            )


@dp.message_handler(state=AddWorker.age)
async def add_age(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await bot.send_message(
            message.chat.id,
            answers.command_on_text_input,
            parse_mode="html"
        )
    else:
        value_compiler = "".join(str(message.text).split())
        value_compiler = ''.join(
            itertools.filterfalse(str.isalpha, value_compiler)
        )
        try:
            if int(value_compiler) >= 18 and int(value_compiler) <= 99:
                async with state.proxy() as data:
                    data['age'] = value_compiler
                await bot.send_message(
                    message.chat.id,
                    answers.on_add_worker_3,
                    parse_mode="html"
                )
                await AddWorker.next()
            else:
                await bot.send_message(
                    message.chat.id,
                    "Возраст должен быть в диапазоне от 18 до 99 лет! Повторите попытку:",
                    parse_mode="html"
                )
        except:
            await bot.send_message(
                message.chat.id,
                "Укажите <b>число</b> в диапазоне от 18 до 99 лет! Повторите попытку:",
                parse_mode="html"
            )


@dp.message_handler(state=AddWorker.in_company_age)
async def add_in_company_age(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await bot.send_message(
            message.chat.id,
            answers.command_on_text_input,
            parse_mode="html"
        )
    else:
        value_compiler = "".join(str(message.text).split())
        value_compiler = ''.join(
            itertools.filterfalse(str.isalpha, value_compiler)
        )
        try:
            if int(value_compiler) >= 1 and int(value_compiler) <= 99:
                async with state.proxy() as data:
                    data['in_company_age'] = value_compiler
                await bot.send_message(
                    message.chat.id,
                    answers.on_add_worker_4,
                    parse_mode="html"
                )
                await AddWorker.next()
            else:
                await bot.send_message(
                    message.chat.id,
                    "Опыт работы должен быть в диапазоне от 1 года и до 99 лет! Повторите попытку:",
                    parse_mode="html"
                )
        except:
            await bot.send_message(
                message.chat.id,
                "Укажите <b>число</b> в диапазоне от 1 до 99 лет, где число - годовой опыт работы в фирме! Повторите попытку:",
                parse_mode="html"
            )


@dp.message_handler(state=AddWorker.description)
async def add_worker_description(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await bot.send_message(
            message.chat.id,
            answers.command_on_text_input,
            parse_mode="html"
        )
    else:
        if len(message.text) <= 1000:
            async with state.proxy() as data:
                data['description'] = message.text
                await bot.send_message(
                    message.chat.id,
                    "Форма записана!\n\n<b>Имя и Фамилия</b>: {name}\n<b>Возраст</b>: {age}\n<b>Опыт работы в фирме</b>: {in_company_age}\n<b>Описание:</b> {description}.\n\nВсё верно?".format(
                        name=data["name"],
                        age=data["age"],
                        in_company_age=data["in_company_age"],
                        description=data["description"]
                    ),
                    parse_mode="html",
                    reply_markup=keyboards.add_worker_done_kb
                )
                await AddWorker.next()
        else:
            await bot.send_message(
                message.chat.id,
                "Слишком длинный текст! Повторите попытку, введя описание меньше чем 1.000 символов:",
                parse_mode="html"
            )


@dp.message_handler(state=WorkerTesting.first_person)
async def first_person(message: types.Message, state: FSMContext):
    await worker_to_testing(message=message, state=state, status=True)


@dp.message_handler(state=WorkerTesting.second_person)
async def second_person(message: types.Message, state: FSMContext):
    await worker_to_testing(message=message, state=state, status=True)


@dp.message_handler(state=WorkerTesting.third_person)
async def second_person(message: types.Message, state: FSMContext):
    await worker_to_testing(message=message, state=state, status=True)


@dp.message_handler(state=WorkerTesting.fourth_person)
async def second_person(message: types.Message, state: FSMContext):
    await worker_to_testing(message=message, state=state, status=True)


@dp.message_handler(state=WorkerTesting.fifth_person)
async def second_person(message: types.Message, state: FSMContext):
    await worker_to_testing(message=message, state=state, status=False)

# ============


@dp.message_handler(state=OfficeTesting.first_office)
async def first_office(message: types.Message, state: FSMContext):
    await office_to_testing(message=message, state=state, status=True)


@dp.message_handler(state=OfficeTesting.second_office)
async def second_office(message: types.Message, state: FSMContext):
    await office_to_testing(message=message, state=state, status=True)


@dp.message_handler(state=OfficeTesting.third_office)
async def third_office(message: types.Message, state: FSMContext):
    await office_to_testing(message=message, state=state, status=True)


@dp.message_handler(state=OfficeTesting.fourth_office)
async def fourth_office(message: types.Message, state: FSMContext):
    await office_to_testing(message=message, state=state, status=True)


@dp.message_handler(state=OfficeTesting.fifth_office)
async def fifth_office(message: types.Message, state: FSMContext):
    await office_to_testing(message=message, state=state, status=False)

# ============


@dp.message_handler(state=SendMessage.on_sending)
async def on_sending(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await bot.send_message(
            message.chat.id,
            answers.command_on_text_input,
            parse_mode="html"
        )
    else:
        if len(message.text) <= 1000:
            await basic_dm(
                sender=message.chat,
                recipient=int(config["Config"]["administrator_id"]),
                message=message.text
            )
            await bot.send_message(
                message.chat.id,
                "<b><i>✅ Собщение доставлено</i></b>\n\nКак только прийдёт ответ, он сразу же отобразится в вашей персональной панеле!",
                parse_mode="html",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await state.finish()
        else:
            await bot.send_message(
                message.chat.id,
                "<b><i>Упс!</i></b>\n\nПожалуйста, умести свой вопрос в 1.000 символов!",
                parse_mode="html"
            )


@dp.message_handler(state=SendMessage.on_answer)
async def on_answer(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await bot.send_message(
            message.chat.id,
            answers.command_on_text_input,
            parse_mode="html"
        )
    else:
        value_compiler = "".join(str(message.text).split())
        value_compiler = ''.join(
            itertools.filterfalse(str.isalpha, value_compiler)
        )
        cursor.execute(
            "SELECT * FROM messages WHERE sender_id = %s",
            (
                value_compiler,
            )
        )
        result = cursor.fetchone()
        if result is not None:
            async with state.proxy() as data:
                data['sender'] = value_compiler
            await bot.send_message(
                message.from_user.id,
                "<b><i>📨 Ответ на сообщение!</i></b>\n\nВведете ответ пользователю {id}:".format(
                    id=str(value_compiler)
                ),
                parse_mode="html"
            )
            await SendMessage.next()
        else:
            await bot.send_message(
                message.chat.id,
                "<b><i>❌ Упс!</i></b>\n\nЧеловек с таким ID не задавал вопрос!",
                parse_mode="html"
            )


@dp.message_handler(state=SendMessage.on_answer_ans)
async def on_answer_ans(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await bot.send_message(
            message.chat.id,
            answers.command_on_text_input,
            parse_mode="html"
        )
    else:
        if len(message.text) <= 1000:
            async with state.proxy() as data:
                await basic_dm(
                    sender=message.chat,
                    recipient=data['sender'],
                    message=message.text
                )
            await bot.send_message(
                message.chat.id,
                "<b><i>✅ Собщение доставлено!</i></b>\n\nОтвет пользователяю был отправлен в его персональную панель!",
                parse_mode="html",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await state.finish()
        else:
            await bot.send_message(
                message.chat.id,
                "<b><i>❌ Упс!</i></b>\n\nПожалуйста, умести свой вопрос в 1.000 символов!",
                parse_mode="html"
            )


@dp.message_handler(state=EnterCode.on_code)
async def on_code(message: types.Message, state: FSMContext):
    if message.text.startswith("/"):
        await bot.send_message(
            message.chat.id,
            answers.command_on_text_input,
            parse_mode="html"
        )
    else:
        if message.text == "2303":
            cursor.execute(
                "UPDATE progress SET stash = %s WHERE member_id = %s",
                (
                    1,
                    message.chat.id
                )
            )
            await bot.send_message(
                message.chat.id,
                "<b><i>💚 Да-да-да!</i></b>\n\nИнформация о том, что ты активировал секретный ключ передана руководству! Тебя ждёт бонус!",
                parse_mode="html",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await state.finish()
        else:
            await bot.send_message(
                message.chat.id,
                "<b><i>❌ Не-а!</i></b>\n\nКод не верный! Повтори попытку или отмени действие:",
                parse_mode="html"
            )


@dp.callback_query_handler(lambda c: c.data == 'works')
async def process_callback_users_progress(callback_query: types.CallbackQuery):
    progress_result = await basic_progress(member=callback_query.from_user)
    img = int(progress_result[6])+1
    if img < 4:
        cursor.execute(
            "SELECT * FROM images WHERE name = %s",
            (
                "product_{img}".format(img=str(img)),
            )
        )
        binary_image = cursor.fetchone()
        image = BytesIO(dec64(binary_image[2]))
        pillow = Image.open(image)
        pillow.save(
            fp="assests/{image}.png".format(image="product_{img}".format(img=str(img))), format="png")
        async with async_open("assests/{image}.png".format(image="product_{img}".format(img=str(img))), "rb") as photo:
            await bot.send_photo(
                chat_id=callback_query.from_user.id,
                photo=photo,
                caption="Дизайнер: GriFMenT",
                reply_markup=keyboards.works_kb
            )
            await callback_query.message.delete()

        cursor.execute(
            "UPDATE progress SET products = %s WHERE member_id = %s",
            (
                img,
                callback_query.from_user.id
            )
        )
    else:
        a = await bot.send_message(
            chat_id=callback_query.from_user.id,
            text="Опа, тайный ключ!\nКод: 2303"
        )
        if progress_result[7] == 0:
            await asyncio.sleep(1)
        await bot.edit_message_text(
            text=answers.on_duties,
            parse_mode="html",
            chat_id=callback_query.from_user.id,
            message_id=a.message_id,
            reply_markup=keyboards.acquaintance_kb
        )


@dp.callback_query_handler(lambda c: c.data == 'users_progress')
async def process_callback_users_progress(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    progress_result = cursor.execute(
        "SELECT * FROM progress"
    )
    progress_result = cursor.fetchall()
    text = ""
    for element in progress_result:
        text += "1. Пользователь: <b>{member_id}</b>\n2. Баллов тестирования: <b>{step}</b>\n3. Пройдено теории: <b>{stepstep}/5</b>\n4. Знание офиса <b>{stepstepstep}/5</b> [теория: <b>{yesno}</b>]\n5. Бонус: {code}\n\n".format(
            member_id=element[1],
            step=element[2],
            stepstep=element[3] if element[3] <= 5 else "5+",
            stepstepstep=element[4],
            yesno="пройдена" if int(element[5]) > 0 else "не пройдена",
            code="активирован" if int(element[7]) > 0 else "не активирован"
        )
    try:
        await callback_query.message.edit_text(
            text=text,
            parse_mode="html",
            reply_markup=keyboards.add_worker_kb
        )
    except:
        await callback_query.message.edit_text(
            "Пусто...\n\nНикто еще не начал проходить подготовку!",
            parse_mode="html",
            reply_markup=keyboards.add_worker_kb
        )


@dp.callback_query_handler(lambda c: c.data == 'add_worker')
async def process_callback_add_worker(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [keyboards.cancel_btn_text]
    keyboard.add(*buttons)
    await bot.send_message(
        callback_query.from_user.id,
        answers.on_add_worker_1,
        parse_mode="html",
        reply_markup=keyboard
    )
    await AddWorker.name.set()


@dp.callback_query_handler(lambda c: c.data == 'add_worker_done', state=AddWorker.to_database)
async def process_callback_add_worker_to_done(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    async with state.proxy() as data:
        try:
            cursor.execute(
                "INSERT INTO staff (name, surname, years, years_on_company, description, status) VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    data["name"].split()[0],
                    data["name"].split()[1],
                    data["age"],
                    data["in_company_age"],
                    data["description"],
                    "active"
                )
            )
        except:
            await bot.send_message(
                callback_query.from_user.id,
                "В памяти приложения отсутствуют упоминания о заносимом сотруднике! Вероятнее всего он уже был занесён в общую Базу Данных!"
            )
            return
    await state.finish()
    await bot.send_message(
        callback_query.from_user.id,
        "<b><i>✅ Отлично!</i></b>\n\nСотрудник был занесён в общую базу данных и теперь будет отображаться на заданиях!",
        parse_mode="html",
        reply_markup=types.ReplyKeyboardRemove()
    )


@dp.callback_query_handler(lambda c: c.data == 'acquaintance')
async def process_callback_acquaintance(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    progress_result = await basic_progress(member=callback_query.from_user)
    result = await on_workers_cheak(n=progress_result[3]+1)
    try:
        await callback_query.message.edit_text(
            answers.on_acquaintance.format(
                name=result[1],
                surname=result[2],
                years=result[4],
                description=result[5]
            ),
            parse_mode="html",
            reply_markup=keyboards.acquaintance_kb
        )
    except:
        await callback_query.message.edit_text(
            "<b><i>😉 Молодец!</i></b>\n\nТы ознакомился со всеми кто был представлен! Желаешь пройти тест на знания?",
            parse_mode="html",
            reply_markup=keyboards.acquaintance_next_reset_kb
        )
    cursor.execute(
        "UPDATE progress SET acquaintance_teory = %s WHERE member_id = %s",
        (
            progress_result[3]+1,
            callback_query.from_user.id,
        )
    )


@dp.callback_query_handler(lambda c: c.data == 'acquaintance_reset')
async def process_callback_add_worker_to_done(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    progress_result = cursor.execute(
        "SELECT * FROM progress WHERE member_id = %s",
        (
            callback_query.from_user.id,
        )
    )
    progress_result = cursor.fetchone()
    if progress_result:
        cursor.execute(
            "DELETE FROM progress WHERE member_id = %s",
            (
                callback_query.from_user.id,
            )
        )
    await callback_query.message.edit_text(
        "<b><i>✅ Статистика сброшена!</i></b>\n\nТеперь ты можешь заново пройти подготовку и накопить баллы тестирования!",
        parse_mode="html"
    )


@dp.callback_query_handler(lambda c: c.data == 'acquaintance_next')
async def process_callback_testing(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    progress_result = await basic_progress(member=callback_query.from_user)
    if int(progress_result[2]) >= 5:
        await bot.send_message(
            callback_query.from_user.id,
            "<b><i>❌ Ой-ой!</i></b>\n\nТы уже окончил прохождение тестирования!",
            parse_mode="html",
            reply_markup=keyboards.acquaintance_next_reset_1_kb
        )
        return
    staff_result = cursor.execute(
        "SELECT COUNT (*) FROM staff"
    )
    staff_result = cursor.fetchall()
    for res in staff_result:
        result = await on_workers_cheak(n=random.randint(1, res[0]))
    async with state.proxy() as data:
        data['result'] = result
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [keyboards.cancel_btn_text]
    keyboard.add(*buttons)
    try:
        await bot.send_message(
            callback_query.from_user.id,
            answers.on_acquaintance_testing.format(
                description=result[5]
            ),
            parse_mode="html",
            reply_markup=keyboard
        )
        await WorkerTesting.first_person.set()
    except:
        await callback_query.message.edit_text(
            "<b><i>❌ Ой-ой!</i></b>\n\nАнкеты для тестов не были заготовлены ранее. Повторите попытку позже!",
            parse_mode="html"
        )
        await state.finish()


@dp.callback_query_handler(lambda c: c.data == 'office_testing')
async def process_callback_acquaintance(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    progress_result = await basic_progress(member=callback_query.from_user)
    if progress_result[4] < 5:
        cursor.execute(
            "UPDATE progress SET ofice_acquaintance_teory = %s WHERE member_id = %s",
            (
                1,
                callback_query.from_user.id
            )
        )
        choices = "bathroom", "director", "installation-department", "meeting-room", "project-main-staff"
        randomer = random.choice(choices)
        async with state.proxy() as data:
            data['ofice_choices'] = randomer
        await callback_query.message.delete()
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [keyboards.cancel_btn_text]
        keyboard.add(*buttons)
        cursor.execute(
            "SELECT * FROM images WHERE name = %s",
            (
                "{randomer}".format(randomer=randomer),
            )
        )
        binary_image = cursor.fetchone()
        image = BytesIO(dec64(binary_image[2]))
        pillow = Image.open(image)
        pillow.save(
            fp="assests/{randomer}.png".format(randomer=randomer), format="png")
        async with async_open("assests/{randomer}.png".format(randomer=randomer), "rb") as photo:
            await bot.send_photo(
                callback_query.from_user.id,
                photo,
                caption=answers.on_office_testing,
                parse_mode="html",
                reply_markup=keyboard
            )
        await OfficeTesting.first_office.set()
    else:
        await bot.edit_message_text(
            text="<b><i>✨ Всё пройдено!</i></b>\n\nТы уже окончил тестирование по знакомству с офисом!",
            parse_mode="html",
            chat_id=callback_query.from_user.id,
            message_id=callback_query.message.message_id
        )


@dp.callback_query_handler(lambda c: c.data == 'ask_question')
async def process_callback_ask_question(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.answer_callback_query(callback_query.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [keyboards.cancel_btn_text]
    keyboard.add(*buttons)
    await bot.send_message(
        callback_query.from_user.id,
        "<b><i>📨 Задай свой вопрос!</i></b>\n\nНапиши в чат вопрос, а мы постаремся ответить как можно скорее!",
        parse_mode="html",
        reply_markup=keyboard
    )
    await SendMessage.on_sending.set()


@dp.callback_query_handler(lambda c: c.data == 'answer_question')
async def process_callback_answer_question(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    buttons = [keyboards.cancel_btn_text]
    keyboard.add(*buttons)
    await bot.send_message(
        callback_query.from_user.id,
        "<b><i>📨 Ответ на сообщение!</i></b>\n\nВведите ID пользователя:",
        parse_mode="html",
        reply_markup=keyboard
    )
    await SendMessage.on_answer.set()


@dp.callback_query_handler(lambda c: c.data == 'messages')
async def process_callback_questions(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    cursor.execute(
        "SELECT * from messages WHERE recipient_id = %s",
        (
            callback_query.from_user.id,
        )
    )
    message_result = cursor.fetchall()
    if message_result is not None:
        for element in message_result:
            if element[2] != callback_query.from_user.id or element[2] is None:
                await bot.send_message(
                    callback_query.from_user.id,
                    "<b><i>❌ Ничего нет!</i></b>\n\nНовых сообщений не поступало!",
                    parse_mode="html"
                )
                return
            await bot.send_message(
                callback_query.from_user.id,
                "<b><i>Сообщение от пользователя {user}</i></b>\n\n{question}!".format(
                    user=element[1],
                    question=element[3]
                ),
                parse_mode="html"
            )
    else:
        await bot.send_message(
            callback_query.from_user.id,
            "<b><i>❌ Ничего нет!</i></b>\n\nНовых сообщений не поступало!",
            parse_mode="html"
        )


@dp.callback_query_handler(lambda c: c.data == 'office_start')
async def process_callback_office_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    progress_result = await basic_progress(member=callback_query.from_user)
    cursor.execute(
        "SELECT * FROM images WHERE name = %s",
        (
            "ofice-plan",
        )
    )
    binary_image = cursor.fetchone()
    image = BytesIO(dec64(binary_image[2]))
    pillow = Image.open(image)
    pillow.save(fp="assests/ofice-plan.png", format="png")
    if int(progress_result[5]) == 0:
        async with async_open("assests/ofice-plan.png", "rb") as photo:
            await bot.send_photo(
                callback_query.from_user.id,
                photo=photo,
                caption=answers.on_office,
                parse_mode="html",
                reply_markup=keyboards.office_testing_kb
            )
    else:
        await bot.send_message(
            callback_query.from_user.id,
            "Похоже, что ты уже начал выполнять тестирование. Продолжить или же сбросить весь прогресс?",
            reply_markup=keyboards.office_testing_new_kb
        )


@dp.callback_query_handler(lambda c: c.data == 'code')
async def process_callback_office_start(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id)
    progress_result = await basic_progress(member=callback_query.from_user)
    if progress_result[7] == 0:
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        buttons = [keyboards.cancel_btn_text]
        keyboard.add(*buttons)
        await bot.send_message(
            callback_query.from_user.id,
            "<b><i>✌️ Правда нашёл код?</i></b>\n\nВведи код, который ты нашёл:",
            parse_mode="html",
            reply_markup=keyboard
        )
        await EnterCode.on_code.set()
    else:
        await bot.send_message(
            callback_query.from_user.id,
            "<b><i>❌ По-новому не получится!</i></b>\n\nТы уже активировал код!",
            parse_mode="html"
        )


async def on_workers_cheak(n):
    for i in range(10):
        cursor.execute(
            "SELECT * FROM staff WHERE key = %s AND status = %s",
            (
                n,
                "active",
            )
        )
        result = cursor.fetchone()
        return result


async def basic_progress(member):
    cursor.execute(
        "SELECT * FROM progress WHERE member_id = %s",
        (
            member.id,
        )
    )
    progress_result = cursor.fetchone()
    if progress_result is None:
        cursor.execute(
            "INSERT INTO progress (member_id, acquaintance, acquaintance_teory, ofice_acquaintance, ofice_acquaintance_teory, products, stash) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                member.id,
                0,
                0,
                0,
                0,
                0,
                0
            )
        )
        cursor.execute(
            "SELECT * FROM progress WHERE member_id = %s",
            (
                member.id,
            )
        )
        progress_result = cursor.fetchone()
    return progress_result


async def basic_dm(sender, recipient, message):
    cursor.execute(
        "INSERT INTO messages (sender_id, recipient_id, message) VALUES (%s, %s, %s)",
        (
            sender.id,
            recipient,
            message
        )
    )


async def worker_to_testing(message, state, status):
    if message.text.startswith("/"):
        await bot.send_message(
            message.chat.id,
            answers.command_on_text_input,
            parse_mode="html"
        )
    else:
        progress_result = await basic_progress(member=message.chat)
        name_surname = message.text.split()
        name_surname_to_cout = " ".join(name_surname)
        name_surname_to_isalpha = "".join(name_surname)
        if len(name_surname_to_cout.split()) == 2 and name_surname_to_isalpha.isalpha():
            async with state.proxy() as data:
                if data['result'][1].lower() == name_surname[0].lower() and data['result'][2].lower() == name_surname[1].lower():
                    cursor.execute(
                        "UPDATE progress SET acquaintance = %s WHERE member_id = %s",
                        (
                            progress_result[2]+1,
                            message.chat.id
                        )
                    )
                    if status == True:
                        await bot.send_message(
                            message.chat.id,
                            answers.on_testing_yes.format(
                                name=data['result'][1],
                                surname=data['result'][2],
                                footer="Идём дальше..."
                            ),
                            parse_mode="html"
                        )
                        staff_result = cursor.execute(
                            "SELECT COUNT (*) FROM staff"
                        )
                        staff_result = cursor.fetchall()
                        for res in staff_result:
                            result = await on_workers_cheak(n=random.randint(1, res[0]))
                        data['result'] = result
                        try:
                            await bot.send_message(
                                message.chat.id,
                                answers.on_acquaintance_testing.format(
                                    description=result[5]
                                ),
                                parse_mode="html"
                            )
                        except Exception as ex:
                            print(ex)
                            await bot.send_message(
                                message.chat.id,
                                "<b><i>❌ Ой-ой-ой!</i></b>\n\nАнкеты для тестов не были заготовлены ранее. Повторите попытку позже!",
                                parse_mode="html"
                            )
                            await state.finish()
                        await WorkerTesting.next()
                    if status == False:
                        await bot.send_message(
                            message.chat.id,
                            answers.on_testing_yes.format(
                                name=data['result'][1],
                                surname=data['result'][2],
                                footer="Тестирование завершено успешно!"
                            ),
                            parse_mode="html",
                            reply_markup=keyboards.acquaintance_next_reset_1_kb
                        )
                        await bot.send_message(
                            message.chat.id,
                            "Ну как, сложно было?\n\nАх да, где-то спрятан тайный ключ, если найдёшь - введи его в своей панели и ты получить приятный бонус!",
                            parse_mode="html",
                            reply_markup=types.ReplyKeyboardRemove()
                        )
                        await state.finish()
                else:
                    await bot.send_message(
                        message.chat.id,
                        "<b><i>❌ Ответ неверный!</i></b>\n\nМожет быть опечатка? Повтори ввод:",
                        parse_mode="html"
                    )
        else:
            await bot.send_message(
                message.chat.id,
                "Имя и Фамилия должны быть написанны отдельно, через пробел и без лишних символов! Повторите попытку:",
                parse_mode="html"
            )


async def office_to_testing(message, state, status):
    if message.text.startswith("/"):
        await bot.send_message(
            message.chat.id,
            answers.command_on_text_input,
            parse_mode="html"
        )
    else:
        progress_result = await basic_progress(member=message.chat)
        if progress_result[4] < 5:
            value_compiler = "".join(str(message.text).split())
            value_compiler = ''.join(
                itertools.filterfalse(str.isalpha, value_compiler)
            )
            try:
                if int(value_compiler) <= 0 or int(value_compiler) > 10:
                    await bot.send_message(
                        message.chat.id,
                        "Ответ должен быть в диапазоне от <b>1</b> до <b>10</b>! Повторите попытку:",
                        parse_mode="html"
                    )
                    return
            except:
                await bot.send_message(
                    message.chat.id,
                    "Укажите <b>число</b> в диапазоне от <b>1</b> до <b>10</b>! Повторите попытку:",
                    parse_mode="html"
                )
                return
            if status == True:
                async with state.proxy() as data:
                    if data['ofice_choices'] == "bathroom":
                        answer = 1
                    if data['ofice_choices'] == "director":
                        answer = 2
                    if data['ofice_choices'] == "installation-department":
                        answer = 5
                    if data['ofice_choices'] == "meeting-room":
                        answer = 4
                    if data['ofice_choices'] == "project-main-staff":
                        answer = 6
                if int(value_compiler) == int(answer):
                    cursor.execute(
                        "UPDATE progress SET ofice_acquaintance = %s WHERE member_id = %s",
                        (
                            progress_result[4]+1,
                            message.chat.id
                        )
                    )
                    choices = "bathroom", "director", "installation-department", "meeting-room", "project-main-staff"
                    randomer = random.choice(choices)
                    cursor.execute(
                        "SELECT * FROM images WHERE name = %s",
                        (
                            "{randomer}".format(randomer=randomer),
                        )
                    )
                    binary_image = cursor.fetchone()
                    image = BytesIO(dec64(binary_image[2]))
                    pillow = Image.open(image)
                    pillow.save(
                        fp="assests/{randomer}.png".format(randomer=randomer), format="png")
                    async with async_open("assests/{randomer}.png".format(randomer=randomer), "rb") as photo:
                        await bot.send_photo(
                            message.chat.id,
                            photo,
                            caption=answers.on_office_testing,
                            parse_mode="html",
                        )
                    async with state.proxy() as data:
                        data['ofice_choices'] = randomer
                    await OfficeTesting.next()
                else:
                    await bot.send_message(
                        message.chat.id,
                        "Ответ не верный! Вспомни и повтори попытку:",
                        parse_mode="html"
                    )
            else:
                cursor.execute(
                    "UPDATE progress SET ofice_acquaintance = %s WHERE member_id = %s",
                    (
                        progress_result[4]+1,
                        message.chat.id
                    )
                )
                await bot.send_message(
                    message.chat.id,
                    "<b><i>✨ Пройдено!</i></b>\n\nТестирование завершено, результат записан!",
                    parse_mode="html",
                    reply_markup=types.ReplyKeyboardRemove()
                )
                await state.finish()
        else:
            await bot.send_message(
                message.chat.id,
                "<b><i>✨ Пройдено!</i></b>\n\nТестирование завершено, результат записан!",
                parse_mode="html",
                reply_markup=types.ReplyKeyboardRemove()
            )
            await state.finish()


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop=loop)
    try:
        asyncio.run(main())
    except:
        pass
