import aiohttp

from aiogram import types, BaseMiddleware
from bot.task_bot.models import Task, Category

class DjangoMiddleware(BaseMiddleware):
    def __init__(self, api_url):
        super().__init__()
        self.api_url = api_url

    async def get_user_tasks(self, user_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}tasks/",
                params={"user__id": user_id}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return [Task(**task) for task in data]
                return []

    async def get_user_categories(self, user_id):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.api_url}categories/",
                params={"user__id": user_id}
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    return [Category(**category) for category in data]
                return []

    async def create_task(self, user_id, title, description, due_date=None, categories=None):
        async with aiohttp.ClientSession() as session:
            data = {
                "title": title,
                "description": description,
                "user": user_id,
                "due_date": due_date.isoformat() if due_date else None,
                "categories": categories or []
            }
            async with session.post(f"{self.api_url}tasks/", json=data) as response:
                if response.status == 201:
                    data = await response.json()
                    return Task(**data)
                return None

    async def on_pre_process_message(self, message: types.Message, data: dict):
        data["django"] = self