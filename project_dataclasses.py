from dataclasses import dataclass


@dataclass
class Settings:

    BOT_TOKEN: str
    DB_URL: str
    DEBUG: bool
    API_BASE_URL: str
