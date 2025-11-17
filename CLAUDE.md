# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

git-aicommit is a Python CLI tool that generates commit messages using AI. It analyzes staged git changes and recent commit history to produce contextually appropriate commit messages via Ollama.

## Development Setup

This project uses:
- **Python 3.13.7** managed via mise (`mise.toml`)
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

# Run the tool locally (after staging changes)
uv run python -m git_aicommit.cli
```

## Architecture

The codebase follows a clean separation of concerns across 5 main modules:

### Core Components

- **cli.py** - Entry point and user interaction loop
  - Click-based CLI with rich terminal UI (using `rich` and `halo`)
  - Interactive loop: generate → preview → (commit|regenerate|quit)
  - Maintains conversation history for regeneration with feedback
  - Reads single keypress actions (c/r/q) via `readchar`

- **ai.py** - LLM integration
  - Uses LangChain with Ollama (`langchain-ollama`)
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
  - Pydantic models: `Config` → `OllamaConfig` (model, base_url, temperature)

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

Users must provide a configuration file at repository or parent directory level:

```yaml
ollama:
  model: "llama3.2"  # Required
  base_url: "http://localhost:11434"  # Optional, defaults shown
  temperature: 0.0  # Optional
```

## Key Implementation Details

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
