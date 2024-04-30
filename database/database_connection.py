from tortoise import Tortoise
from config.config import settings

async def connect_database():
    """
    Подключаем Tortoise ORMк нашей базе данных
    """
    try:
        # db_url и modules более кстати не нужны, закоментил их на всякий случай
        await Tortoise.init(
            config=settings.TORTOISE_CONFIG
        )
        print(f"Successfully conected to DB {settings.DB_NAME}!")
    except Exception as e:
        print(f"Couldn't connect to database {settings.DB_NAME}, raised an exception:\n{e}")
