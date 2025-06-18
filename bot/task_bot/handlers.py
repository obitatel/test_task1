from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from bot.task_bot.dialogs import tasks_dialog

async def start_command(message: types.Message, state: FSMContext):
    await message.answer("Привет! Я бот для управления задачами. Используй /tasks для просмотра списка задач.")

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_command, Command("start"))
    dp.register_message_handler(
        tasks_dialog.start,
        Command("tasks"),
        state="*"
    )
    dp.register_dialog(tasks_dialog)