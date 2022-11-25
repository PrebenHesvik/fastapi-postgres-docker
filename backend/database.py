import beanie
import motor
import motor.motor_asyncio
from .models import TodoList, TodoItem

from .config import settings

database_name = settings.database_name
username = settings.database_username
password = settings.database_password
port = settings.database_port
hostname = settings.database_hostname


async def init_db():
    client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://localhost:27017")

    await beanie.init_beanie(
        database=client.db_name, document_models=[TodoList, TodoItem]  # type: ignore
    )
