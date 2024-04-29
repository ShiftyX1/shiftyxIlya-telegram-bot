from dotenv import load_dotenv
from pathlib import Path

import os

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

class Settings:
    TOKEN: str = os.getenv("TOKEN")


settings = Settings()

