from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Bot_Settings(BaseSettings):
    BOT_TOKEN: SecretStr

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


bot_settings = Bot_Settings()

if __name__ == "__main__":
    # to check settings run `python config.py`
    print(bot_settings.model_dump())
