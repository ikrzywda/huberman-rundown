from pydantic import BaseSettings


class Settings(BaseSettings):
    YOUTUBE_API_KEY: str
    YT_CHANNEL_ID: str
    YT_PLAYLIST_ID: str

    class Config:
        env_file = ".env"


settings = Settings()
