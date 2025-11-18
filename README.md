# git-aicommit

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/koki-develop/git-aicommit)](https://github.com/koki-develop/git-aicommit/releases/latest)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/koki-develop/git-aicommit/ci.yml?logo=github)](https://github.com/koki-develop/git-aicommit/actions/workflows/ci.yml)
[![LICENSE](https://img.shields.io/github/license/koki-develop/git-aicommit)](./LICENSE)

Generate commit messages using AI.

## Supported Providers

- [Amazon Bedrock](https://aws.amazon.com/bedrock/)
- [Anthropic](https://www.anthropic.com/)
- [Google Generative AI](https://ai.google.dev)
- [Ollama](https://ollama.com/)
- [OpenAI](https://openai.com/)

## Installation

```console
$ pip install git+https://github.com/koki-develop/git-aicommit.git
```

## Usage

### Setup

Create a configuration file.

#### Using Amazon Bedrock

```yaml
# aicommit.yml
provider: aws-bedrock
aws-bedrock:
  model: "<model>" # Required (e.g. "us.anthropic.claude-sonnet-4-20250514-v1:0")
  region: "<region>" # Required (e.g. "us-west-2", "us-east-1")
  temperature: 0.0 # Optional (default: 0.0)
```

Configure AWS credentials via environment variables:

```bash
export AWS_ACCESS_KEY_ID="<your-access-key>"
export AWS_SECRET_ACCESS_KEY="<your-secret-key>"
export AWS_SESSION_TOKEN="<your-session-token>" # Optional, for temporary credentials
```

#### Using Anthropic

```yaml
# aicommit.yml
provider: anthropic
anthropic:
  model: "<model>" # Required (e.g. "claude-haiku-4-5-20251001", "claude-sonnet-4-5-20250929")
  api-key: "<api-key>" # Required
  temperature: 0.0 # Optional (default: 0.0)
```

#### Using Google GenAI

```yaml
# aicommit.yml
provider: google-genai
google-genai:
  model: "<model>" # Required (e.g. "gemini-2.5-flash", "gemini-2.5-pro")
  api-key: "<api-key>" # Required
  temperature: 0.0 # Optional (default: 0.0)
```

#### Using Ollama

```yaml
# aicommit.yml
provider: ollama
ollama:
  model: "<model>" # Required
  base-url: "http://localhost:11434" # Optional (default: http://localhost:11434)
  temperature: 0.0 # Optional (default: 0.0)
```

#### Using OpenAI

```yaml
# aicommit.yml
provider: openai
openai:
  model: "<model>" # Required (e.g. "gpt-5", "gpt-4.1")
  api-key: "<api-key>" # Required
  temperature: 0.0 # Optional (default: 0.0)
```

---

Place a configuration file in your repository or any parent directory.  
Supported file names:

- `aicommit.yml`
- `aicommit.yaml`
- `.aicommit.yml`
- `.aicommit.yaml`

### Generate a Commit Message

Run `git aicommit` in your git repository to generate a commit message using AI:

```console
$ git aicommit
```

## License

[MIT](./LICENSE)
