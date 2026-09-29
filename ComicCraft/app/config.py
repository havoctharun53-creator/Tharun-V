from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    app_name: str = "ComicCraft"
    gemini_api_key: str = ""
    hf_api_key: str = ""

    # Current Gemini models. Override in .env if desired.
    gemini_flash_model: str = "gemini-3.8-flash"
    gemini_pro_model: str = "gemini-3.8-pro"

    # "huggingface" uses hosted inference; "local" uses Diffusers.
    image_provider: str = "huggingface"
    image_model: str = "stabilityai/stable-diffusion-3.5-large"
    hf_provider: str = "auto"

    # Used only by the optional local Diffusers provider.
    local_image_model: str = "runwayml/stable-diffusion-v1-5"
    local_device: str = "auto"

    max_prompt_length: int = 2000
    panel_count: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
