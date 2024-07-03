from pydantic_settings import BaseSettings, SettingsConfigDict


class _Settings(BaseSettings):
    YOUTUBE_USERNAME: str
    YOUTUBE_PASSWORD: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = _Settings()
