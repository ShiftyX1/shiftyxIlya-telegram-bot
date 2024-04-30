from dotenv import load_dotenv
from pathlib import Path

import os

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

class Settings:
    TOKEN: str = os.getenv("TOKEN")
    ADMIN_ID: int = os.getenv("ADMIN_ID")

    # Данные БД берем из переменных окружения
    DB_USER: str = os.getenv("DB_USER")
    DB_PASS: str = os.getenv("DB_PASS")
    DB_NAME: str = os.getenv("DB_NAME")
    DB_PORT: str = os.getenv("DB_PORT")
    DB_HOST: str = os.getenv("DB_HOST")
    DB_URL: str = f"postgres://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    # Конфиг tortoise orm создаем для работы миграций Aerich, в apps подключены модели для миграций
    TORTOISE_CONFIG: dict = {
    "connections": {"default": DB_URL},
    "apps": {
            "gpt_history" :{
                "models": ["models.gpt_models"],
            },
            "models": {
                "models": ["aerich.models"],
                "default_connection": "default",
            },
        },
    }



settings = Settings()

