from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_URI: str
    REDIS_URL: str
    MONGO_DB_NAME: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    ALGORITHM: str = "HS256"
    GOOGLE_CLIENT_ID: str
    GOOGLE_CLIENT_SECRET: str
    GOOGLE_REDIRECT_URI: str
    OPENAI_API_KEY: str
    KR_GOV_DATA_API_KEY: str
    SLACK_BOT_TOKEN: str
    ACCU_WEATHER_API_KEY: str
    PERPLEXITY_API_KEY: str
    model_config = SettingsConfigDict(extra="allow", env_file=".env")


settings = Settings()
