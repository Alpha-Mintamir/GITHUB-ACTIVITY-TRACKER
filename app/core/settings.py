from pydantic_settings import BaseSettings
from typing import Optional
from pathlib import Path
import os

class Settings(BaseSettings):
    app_name: str = "GitHub Activity Analyzer"
    debug: bool = False
    version: str = "1.0.0"
    github_token: str
    github_api_url: str = "https://api.github.com"
    host: str = "0.0.0.0"
    port: int = 8002
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "allow",
        "env_prefix": "",
        "env_nested_delimiter": "__",
        "alias_generator": lambda x: x.upper()  # Convert field names to uppercase for env vars
    }

    @property
    def base_dir(self) -> Path:
        return Path(__file__).parent.parent.parent

settings = Settings()