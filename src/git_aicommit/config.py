from typing import Optional, Literal
from pathlib import Path
from yaml import safe_load
from pydantic import BaseModel, model_validator


class OllamaConfig(BaseModel):
    model: str
    base_url: str = "http://localhost:11434"
    temperature: float = 0.0


class OpenAIConfig(BaseModel):
    model: str
    api_key: str
    temperature: float = 0.0


class Config(BaseModel):
    provider: Literal["ollama", "openai"]
    ollama: Optional[OllamaConfig] = None
    openai: Optional[OpenAIConfig] = None

    @model_validator(mode="after")
    def validate_provider_config(self):
        if self.provider == "ollama" and self.ollama is None:
            raise ValueError("ollama configuration is required when provider is 'ollama'")
        if self.provider == "openai" and self.openai is None:
            raise ValueError("openai configuration is required when provider is 'openai'")
        return self


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
