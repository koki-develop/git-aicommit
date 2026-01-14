from typing import Optional, Literal, Self
from pathlib import Path
from yaml import safe_load
from pydantic import (
    BaseModel,
    SecretStr,
    Field,
    ValidationError,
    model_validator,
    ConfigDict,
)
from git_aicommit.error import InvalidConfigurationError


class AWSBedrockConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model: str
    region: str
    temperature: float = 0.0


class AnthropicConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model: str
    api_key: SecretStr = Field(alias="api-key")
    temperature: float = 0.0


class GoogleGenAIConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model: str
    api_key: SecretStr = Field(alias="api-key")
    temperature: float = 0.0


class OllamaConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model: str
    base_url: str = Field(
        default="http://localhost:11434",
        alias="base-url",
    )
    temperature: float = 0.0


class OpenAIConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    model: str
    api_key: SecretStr = Field(alias="api-key")
    temperature: float = 0.0


class Config(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: Literal["aws-bedrock", "anthropic", "google-genai", "ollama", "openai"]
    prompt: Optional[str] = None
    aws_bedrock: Optional[AWSBedrockConfig] = Field(default=None, alias="aws-bedrock")
    anthropic: Optional[AnthropicConfig] = None
    google_genai: Optional[GoogleGenAIConfig] = Field(
        default=None, alias="google-genai"
    )
    ollama: Optional[OllamaConfig] = None
    openai: Optional[OpenAIConfig] = None

    @model_validator(mode="after")
    def validate_provider_config(self) -> Self:
        if self.provider == "aws-bedrock" and self.aws_bedrock is None:
            raise ValueError(
                "aws-bedrock configuration is required when provider is 'aws-bedrock'"
            )
        if self.provider == "anthropic" and self.anthropic is None:
            raise ValueError(
                "anthropic configuration is required when provider is 'anthropic'"
            )
        if self.provider == "google-genai" and self.google_genai is None:
            raise ValueError(
                "google-genai configuration is required when provider is 'google-genai'"
            )
        if self.provider == "ollama" and self.ollama is None:
            raise ValueError(
                "ollama configuration is required when provider is 'ollama'"
            )
        if self.provider == "openai" and self.openai is None:
            raise ValueError(
                "openai configuration is required when provider is 'openai'"
            )
        return self


def load_config() -> Config:
    config_path = find_config_path()
    if config_path is None:
        raise FileNotFoundError("Configuration file not found.")

    with open(config_path, "r") as f:
        try:
            data = safe_load(f)
        except Exception as e:
            raise InvalidConfigurationError(f"YAML parsing error: {str(e)}") from e

    if data is None:
        raise InvalidConfigurationError("Configuration file is empty.")

    try:
        return Config(**data)
    except ValidationError as e:
        raise InvalidConfigurationError(str(e)) from e


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
