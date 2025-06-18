from aiogram import types
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Row, Back
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog import DialogManager
from datetime import datetime


async def get_tasks_data(dialog_manager: DialogManager, **kwargs):
    django = dialog_manager.data["django"]
    user_id = dialog_manager.event.from_user.id
    tasks = await django.get_user_tasks(user_id)
    return {
        "tasks": tasks,
        "count": len(tasks)
    }


async def on_task_selected(callback: types.CallbackQuery, widget, manager: DialogManager, task_id: str):
    pass


async def on_add_task_click(callback: types.CallbackQuery, button: Button, manager: DialogManager):
    await manager.dialog().switch_to("add_task_title")


async def on_title_entered(message: types.Message, dialog: Dialog, manager: DialogManager):
    manager.dialog_data["title"] = message.text
    await manager.dialog().switch_to("add_task_description")


async def on_description_entered(message: types.Message, dialog: Dialog, manager: DialogManager):
    manager.dialog_data["description"] = message.text
    await manager.dialog().switch_to("add_task_due_date")


async def on_due_date_entered(message: types.Message, dialog: Dialog, manager: DialogManager):
    try:
        due_date = datetime.strptime(message.text, "%d.%m.%Y %H:%M")
        manager.dialog_data["due_date"] = due_date
    except ValueError:
        await message.answer("Неверный формат даты. Используйте ДД.ММ.ГГГГ ЧЧ:ММ")
        return

    django = manager.data["django"]
    user_id = message.from_user.id
    task = await django.create_task(
        user_id=user_id,
        title=manager.dialog_data["title"],
        description=manager.dialog_data["description"],
        due_date=manager.dialog_data.get("due_date")
    )

    if task:
        await message.answer(f"Задача '{task.title}' создана!")
    else:
        await message.answer("Ошибка при создании задачи")

    await manager.done()


tasks_dialog = Dialog(
    Window(
        Const("📝 Ваши задачи:"),
        Format("Всего задач: {count}"),
        Button(Const("➕ Добавить задачу"), id="add_task", on_click=on_add_task_click),
        state="tasks_list",
        getter=get_tasks_data
    ),
    Window(
        Const("Введите название задачи:"),
        MessageInput(on_title_entered),
        state="add_task_title"
    ),
    Window(
        Const("Введите описание задачи:"),
        MessageInput(on_description_entered),
        state="add_task_description"
    ),
    Window(
        Const("Введите дату и время выполнения (ДД.ММ.ГГГГ ЧЧ:ММ):"),
        MessageInput(on_due_date_entered),
        state="add_task_due_date"
    )
)