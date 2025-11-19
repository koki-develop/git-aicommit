from typing import Protocol
from pydantic import SecretStr
from langchain_core.language_models import BaseChatModel
from langchain_aws import ChatBedrockConverse
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from git_aicommit.config import Config
from git_aicommit.error import InvalidConfigurationError


class Provider(Protocol):
    name: str
    model_name: str
    chat_model: BaseChatModel


def provider_from_config(config: Config) -> Provider:
    # Amazon Bedrock
    if config.provider == "aws-bedrock":
        assert config.aws_bedrock is not None
        return AWSBedrockProvider(
            model=config.aws_bedrock.model,
            region=config.aws_bedrock.region,
            temperature=config.aws_bedrock.temperature,
        )

    # Anthropic
    elif config.provider == "anthropic":
        assert config.anthropic is not None
        return AnthropicProvider(
            model=config.anthropic.model,
            api_key=config.anthropic.api_key,
            temperature=config.anthropic.temperature,
        )

    # Google GenAI
    elif config.provider == "google-genai":
        assert config.google_genai is not None
        return GoogleGenAIProvider(
            model=config.google_genai.model,
            api_key=config.google_genai.api_key,
            temperature=config.google_genai.temperature,
        )

    # Ollama
    elif config.provider == "ollama":
        assert config.ollama is not None
        return OllamaProvider(
            model=config.ollama.model,
            base_url=config.ollama.base_url,
            temperature=config.ollama.temperature,
        )

    # OpenAI
    elif config.provider == "openai":
        assert config.openai is not None
        return OpenAIProvider(
            model=config.openai.model,
            api_key=config.openai.api_key,
            temperature=config.openai.temperature,
        )

    else:
        raise InvalidConfigurationError(f"Unsupported provider: {config.provider}")


class AWSBedrockProvider:
    def __init__(self, model: str, region: str, temperature: float):
        self.name: str = "aws-bedrock"
        self.model_name: str = model
        self.chat_model: BaseChatModel = ChatBedrockConverse(
            model=model,
            region_name=region,
            temperature=temperature,
        )


class AnthropicProvider:
    def __init__(self, model: str, api_key: SecretStr, temperature: float):
        self.name: str = "anthropic"
        self.model_name: str = model
        self.chat_model: BaseChatModel = ChatAnthropic(
            model_name=model,
            api_key=api_key,
            temperature=temperature,
            timeout=None,
            stop=None,
        )


class GoogleGenAIProvider:
    def __init__(self, model: str, api_key: SecretStr, temperature: float):
        self.name: str = "google-genai"
        self.model_name: str = model
        self.chat_model: BaseChatModel = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=temperature,
        )


class OllamaProvider:
    def __init__(self, model: str, base_url: str, temperature: float):
        self.name: str = "ollama"
        self.model_name: str = model
        self.chat_model: BaseChatModel = ChatOllama(
            model=model,
            base_url=base_url,
            temperature=temperature,
        )


class OpenAIProvider:
    def __init__(self, model: str, api_key: SecretStr, temperature: float):
        self.name: str = "openai"
        self.model_name: str = model
        self.chat_model: BaseChatModel = ChatOpenAI(
            model=model,
            api_key=api_key,
            temperature=temperature,
        )
