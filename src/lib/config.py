from typing import Optional
from pathlib import Path
from yaml import safe_load
from pydantic import BaseModel


class OllamaConfig(BaseModel):
    model: str
    base_url: str = "http://localhost:11434"
    temperature: float = 0.0


class Config(BaseModel):
    ollama: OllamaConfig


def load_config() -> Config:
    config_path = find_config_path()
    if config_path is None:
        raise FileNotFoundError("Configuration file not found.")

    with open(config_path, "r") as f:
        data = safe_load(f)

    return Config(**data)


def find_config_path() -> Optional[str]:
    filenames = [
        ".aicommit.yml",
        "aicommit.yml",
        ".aicommit.yaml",
        "aicommit.yaml",
    ]
    current = Path.cwd()

    for parent in [current] + list(current.parents):
        for filename in filenames:
            config_path = parent / filename
            if config_path.is_file():
                return str(config_path)

    return None
