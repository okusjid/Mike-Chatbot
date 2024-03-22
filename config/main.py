"""
    Contains the main configuration for project.
"""

from pydantic_settings import BaseSettings
import os


class Settings(BaseSettings):
    """
        These are the settings read from environment.
    """
    OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY") or ""
    LLM_MODEL: str = os.environ.get("LLM_MODEL") or "gpt-4-1106-preview"
    ASSISTANT_ID: str = os.environ.get("ASSISTANT_ID") or ""
    MATT_EMAIL: str = os.environ.get("MATT_EMAIL") or ""
    MAIL_USERNAME: str = os.environ.get("MAIL_USERNAME") or ""
    MAIL_PASSWORD: str = os.environ.get("MAIL_PASSWORD") or ""
    MAIL_PORT: int = int(os.environ.get("MAIL_PORT") or 587)
    MAIL_SERVER: str = os.environ.get("MAIL_SERVER") or ""
    MAIL_EMAIL: str = os.environ.get("MAIL_EMAIL") or ""
    MAIL_FROM_NAME: str = os.environ.get("MAIL_FROM_NAME") or "Mike Assistant"

settings = Settings()
