
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ryu_base_url: str = "http://192.168.100.100:8080"
    ryu_timeout_seconds: float = Field(default=3.0, gt=0)

    model_config = SettingsConfigDict(
        env_file=Path(__file__).resolve().parents[1] / ".env",
        env_prefix="SDN_FIREWALL_",
        extra="ignore",
    )


settings = Settings()
