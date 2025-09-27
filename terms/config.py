from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DISCORD_TOKEN: str
    GUILD_ID: int
    SHARPS_ROLE_NAME: str = "Sharps"
    DATABASE_URL: str = "sqlite:///./consent.db"
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"
