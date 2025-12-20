import json
import os

from pydantic_settings import BaseSettings, SettingsConfigDict


class ConfigManager:
    def __init__(self):
        self.is_created = self.create_config_file()

    def _append_config(self, session_name: str, data: dict) -> None:
        if self.is_created:
            config = self.load_config()
            config[session_name] = data

            with open("config.json", "w", encoding="utf-8") as f:
                json.dump(config, f)

    def load_config(self) -> list[dict[str, str]]:
        with open("config.json", encoding="utf-8") as f:
            return json.load(f)

    def load_config_by_profile(self, session_name: str) -> dict[str, str]:
        with open("config.json", encoding="utf-8") as f:
            data = json.load(f)
            return data[session_name]

    def create_config_file(self) -> None:
        if not os.path.exists("config.json"):
            with open("config.json", "w", encoding="utf-8") as f:
                json.dump({}, f)
        return True

    def create_config_profile(self, session_name: str) -> None:
        if self.is_created:
            print(
                f"Config was created successfully\nYou can edit it in {os.path.join(os.getcwd(), 'config.json')}"
            )
            profile_config = {"proxy": None}

            self._append_config(session_name, profile_config)


class Settings(BaseSettings):
    api_id: int
    api_hash: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
