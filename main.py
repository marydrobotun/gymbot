import asyncio
import logging
import sys
from os import getenv
from sqlalchemy.exc import IntegrityError
import emoji
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from queries import add_user, print_user_id, add_training

# Bot token can be obtained via https://t.me/BotFather
TOKEN = getenv('TOKEN')
TRAINING_NAME_AWAIT = []
MACHINE_NAME_AWAIT = {}
users_table = []
trainings_table = []
machines_table = []
settings_table = []
# All handlers should be attached to the Router (or Dispatcher)

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    users_table.append({'chat_id': message.from_user.id})
    try:
        add_user(message.from_user.id)
    except IntegrityError:
        print('user already exists')

#    print_user_id(message.from_user.id)
    """
    This handler receives messages with `/start` command
    """
    # Most event objects have aliases for API methods that can be called in events' context
    # For example if you want to answer to incoming message you can use `message.answer(...)` alias
    # and the target chat will be passed to :ref:`aiogram.methods.send_message.SendMessage`
    # method automatically or call API method directly via
    # Bot instance: `bot.send_message(chat_id=message.chat.id, ...)`

    builder = InlineKeyboardBuilder()

    start_buttons = {
        'create_training': ':memo: Новая тренировка',
        'select_training': ':woman_lifting_weights: Выбрать тренировку',
        'trainings_stats': ':chart_increasing: Статистика тренировок',
    }
    start_buttons = {key: emoji.emojize(value) for key, value in start_buttons.items()}
    for slug, button in start_buttons.items():
        builder.button(text=button, callback_data=slug)
        builder.adjust(1, 1, 1)
    await message.answer(
        (
            f"Привет, {html.bold(message.from_user.full_name)}! Я "
            f"бот для настройки тренажёров в спортзале. Я умею сохранять вес"
            f" и другие регулировки тренажёров, чтобы напомнить их на следующей тренировке!\n"
            f"\n"
            f"Основные команды:\n"
        ), reply_markup=builder.as_markup()
    )


@dp.callback_query(lambda c: c.data == 'create_training')
async def create_training_callback(callback: CallbackQuery):
    TRAINING_NAME_AWAIT.append(callback.from_user.id)
    await callback.message.answer('Введи название тренировки: ')


@dp.callback_query(lambda c: c.data == 'trainings_stats')
async def trainigs_stats_callback(callback: CallbackQuery):
    await callback.message.answer(emoji.emojize('Эта функция пока в разработке :pensive_face:'))


@dp.message()
async def text_handler(message: Message) -> None:
    """
    Handler will forward receive a message back to the sender

    By default, message handler will handle all message types (like a text, photo, sticker etc.)
    """
    if message.from_user.id in TRAINING_NAME_AWAIT:
        add_training(chat_id=message.from_user.id, title=message.text)
        trainings_table.append({'chat_id': message.from_user.id, 'title': message.text})
        training_id = trainings_table.index({'chat_id': message.from_user.id, 'title': message.text})
        TRAINING_NAME_AWAIT.remove(message.from_user.id)
        MACHINE_NAME_AWAIT[message.from_user.id] = training_id
        await message.answer('Введи название тренажера: ')
    if message.from_user.id in MACHINE_NAME_AWAIT:
        machine_name = message.text
        print(f'Название тренажёра:{machine_name}')  # to database
    if message.from_user.id in MACHINE_NAME_AWAIT.keys():
        print(f'Добавляю тренажер {message.text} в тренировку {trainings_table[MACHINE_NAME_AWAIT[message.from_user.id]]["title"]}')



async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    # And the run events dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
