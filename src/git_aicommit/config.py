from typing import Optional, Literal, Self
from pathlib import Path
from yaml import safe_load
from pydantic import BaseModel, SecretStr, Field, model_validator


class OllamaConfig(BaseModel):
    model: str
    base_url: str = "http://localhost:11434"
    temperature: float = 0.0


class OpenAIConfig(BaseModel):
    model: str
    api_key: SecretStr
    temperature: float = 0.0


class GoogleGenAIConfig(BaseModel):
    model: str
    api_key: SecretStr
    temperature: float = 0.0


class Config(BaseModel):
    provider: Literal["ollama", "openai", "google-genai"]
    ollama: Optional[OllamaConfig] = None
    openai: Optional[OpenAIConfig] = None
    google_genai: Optional[GoogleGenAIConfig] = Field(
        default=None, alias="google-genai"
    )

    @model_validator(mode="after")
    def validate_provider_config(self) -> Self:
        if self.provider == "ollama" and self.ollama is None:
            raise ValueError(
                "ollama configuration is required when provider is 'ollama'"
            )
        if self.provider == "openai" and self.openai is None:
            raise ValueError(
                "openai configuration is required when provider is 'openai'"
            )
        if self.provider == "google-genai" and self.google_genai is None:
            raise ValueError(
                "google-genai configuration is required when provider is 'google-genai'"
            )
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
