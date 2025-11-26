# Repository Guidelines

## Project Overview

git-aicommit is a Python CLI tool that generates commit messages using AI. It analyzes staged git changes and recent commit history to produce contextually appropriate commit messages via AI providers (Amazon Bedrock, Anthropic, Google GenAI, Ollama, or OpenAI).

## Development Setup

This project uses:
- **Python 3.14.0** managed via mise (`mise.toml`)
- **uv** as the package manager (modern Python package/project manager)
- **setuptools** for building (pyproject.toml build-backend)

### Essential Commands

```bash
# Install dependencies
uv sync

# Build the package
uv build

# Run linting
uv run ruff check

# Initialize configuration file
uv run git-aicommit init

# Run the tool locally (after staging changes)
uv run git-aicommit
```

## Architecture

The codebase follows a clean separation of concerns across 5 main modules:

### Core Components

- **cli.py** - Entry point and user interaction loop
  - Click-based CLI with rich terminal UI (using `rich` and `halo`)
  - **CLI Structure**: Uses `@click.group()` with `invoke_without_command=True` to support both default behavior and subcommands
    - Default (no subcommand): Generate commit message from staged changes
    - `init` subcommand: Create configuration file template with all provider examples
  - Interactive loop: generate → preview → (commit|regenerate|quit)
  - Maintains conversation history for regeneration with feedback
  - Reads single keypress actions (c/r/q) via `readchar`
  - `_load_model()` function: Initializes the appropriate AI model (Amazon Bedrock, Anthropic, Google GenAI, Ollama, or OpenAI) based on configuration

- **ai.py** - LLM integration
  - Uses LangChain with AI providers (`langchain-anthropic`, `langchain-aws`, `langchain-google-genai`, `langchain-ollama`, or `langchain-openai`)
  - Provider-agnostic: Accepts any `BaseChatModel` implementation
  - Structured output via Pydantic `Commit` model
  - Prompt includes: recent logs + diff + conversation history
  - XML escaping applied to all user inputs (security against prompt injection)

- **git.py** - Git operations wrapper
  - Wraps GitPython (`git.Repo`)
  - Key methods: `logs()`, `is_staged()`, `diff()`, `commit()`
  - **Important**: Uses direct git command execution for `commit()` to support GPG signing (not `repo.index.commit`)

- **config.py** - Configuration management
  - Loads from `.aicommit.yml` or `aicommit.yaml` (with/without leading dot)
  - **Config discovery**: Walks up directory tree from cwd to find config
  - Pydantic models:
    - `Config`: Contains `provider` (Literal["anthropic", "aws-bedrock", "google-genai", "ollama", "openai"]) and optional provider-specific configs
    - `AWSBedrockConfig`: model, region, temperature
    - `AnthropicConfig`: model, api-key, temperature
    - `GoogleGenAIConfig`: model, api-key, temperature
    - `OllamaConfig`: model, base-url, temperature
    - `OpenAIConfig`: model, api-key, temperature
  - Custom validator ensures the correct provider config is present based on `provider` field

- **error.py** - Custom exceptions
  - `AbortCommitError`: User aborts commit operation

### Data Flow

1. CLI checks for staged changes (`git.is_staged()`)
2. Retrieves staged diff and last 10 commit messages
3. Sends to AI with system prompt describing engineer role
4. User reviews generated message and can:
   - Commit (calls `git.commit()`)
   - Regenerate with feedback (appends to history as `HumanMessage`)
   - Quit (raises `AbortCommitError`)

## Configuration

Users can generate a configuration file template using `git-aicommit init`, which creates `aicommit.yml` with examples for all supported providers.

Alternatively, users can manually create a configuration file at repository or parent directory level.

### Amazon Bedrock Example

```yaml
provider: aws-bedrock
aws-bedrock:
  model: "us.anthropic.claude-3-5-sonnet-20240620-v1:0"  # Required
  region: "us-west-2"  # Required
  temperature: 0.0  # Optional
```

**Authentication**: AWS credentials must be configured via environment variables:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_SESSION_TOKEN` (optional, for temporary credentials)

### Anthropic Example

```yaml
provider: anthropic
anthropic:
  model: "claude-haiku-4-5-20251001"  # Required
  api-key: "<anthropic-api-key>"  # Required
  temperature: 0.0  # Optional
```

### Google GenAI Example

```yaml
provider: google-genai
google-genai:
  model: "gemini-2.5-flash"  # Required
  api-key: "<google-api-key>"  # Required
  temperature: 0.0  # Optional
```

### Ollama Example

```yaml
provider: ollama
ollama:
  model: "llama3.2"  # Required
  base-url: "http://localhost:11434"  # Optional, defaults shown
  temperature: 0.0  # Optional
```

### OpenAI Example

```yaml
provider: openai
openai:
  model: "gpt-4"  # Required
  api-key: "sk-..."  # Required
  temperature: 0.0  # Optional
```

## Key Implementation Details

- **CLI Architecture**: Click group with `invoke_without_command=True` allows default behavior (commit message generation) while supporting subcommands (`init`)
- **Init Command**: Creates `aicommit.yml` with all provider examples commented out; checks for existing config files before creation
- **Multi-Provider Support**: Supports Amazon Bedrock, Anthropic, Google GenAI, Ollama, and OpenAI via LangChain's `BaseChatModel` abstraction
- **Provider Selection**: `_load_model()` function in `cli.py` initializes the correct provider based on configuration
- **Structured Output**: Uses `model.with_structured_output(Commit)` for reliable message extraction
- **Prompt Injection Protection**: All user input (feedback, diff, logs) is XML-escaped before including in prompts
- **Conversation History**: LangChain `MessagesPlaceholder` enables multi-turn refinement
- **Exit Codes**: 1 for abort, 130 for Ctrl+C (standard terminal conventions)
- **Git Signing Support**: Direct git command execution preserves commit hooks and signing configuration

## CI/CD

GitHub Actions workflow (`.github/workflows/ci.yml`):
- **Build job**: Runs `uv build`
- **Lint job**: Runs `uv run ruff check`
- Uses mise-action for Python/uv installation
