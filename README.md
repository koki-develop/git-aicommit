# git-aicommit

[![GitHub release (latest by date)](https://img.shields.io/github/v/release/koki-develop/git-aicommit)](https://github.com/koki-develop/git-aicommit/releases/latest)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/koki-develop/git-aicommit/ci.yml?logo=github)](https://github.com/koki-develop/git-aicommit/actions/workflows/ci.yml)
[![LICENSE](https://img.shields.io/github/license/koki-develop/git-aicommit)](./LICENSE)

Generate commit messages using AI.

## Installation

```console
$ pip install git+https://github.com/koki-develop/git-aicommit.git
```

## Usage

### Setup

Create a configuration file.

```yaml
# aicommit.yml
ollama:
  model: "<model>" # Required
  base_url: "http://localhost:11434" # Optional
  temperature: 0 # Optional
```

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
