# X Trends Agent - OpenAI API

## Introduction

The X Trends Agent is an AI-powered conversational agent designed to analyze trending topics on X (formerly Twitter). It is built with the **BeeAI framework** and exposes a **OpenAI-compatible API** to consume the agent.

The agent:
- detects the country mentioned in the prompt,
- retrieves X trends from `trends24.in`,
- extracts the top trending topics,
- synthesizes a friendly summary in natural language.

## Requirements

- **Python:** 3.11 or higher
- **uv:** installed locally
- **Ollama:** installed locally
- **Model:** `granite4:tiny-h`

## Project Setup

Clone the repository and enter the project folder:

```bash
git clone --branch OpenAI_API --single-branch https://github.com/BrUn3y/x_trends_agent_BeeAI.git
cd x_trends_agent_BeeAI
```

Create a virtual environment with Python 3.12:

```bash
python3.12 -m venv .venv
```

Activate the virtual environment:

```bash
source .venv/bin/activate
```

Install the dependencies:

```bash
uv sync
```

Install the Ollama model:

```bash
ollama pull granite4:tiny-h
```

## Running the OpenAI API Server

Start the API server:

```bash
uv run src/beeai_agents/agent.py
```

The server will run on `http://localhost:9998` (OpenAI chat completions endpoint).

## Usage

Query the agent via cURL:

```bash
curl -X POST http://localhost:9998/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agent",
    "messages": [
      {"role": "user", "content": "What are the trends in Mexico?"}
    ]
  }'
```

Or use Python with the `requests` library:

```python
import requests

response = requests.post(
    "http://localhost:9998/chat/completions",
    json={
        "model": "agent",
        "messages": [
            {"role": "user", "content": "What are the trends in Mexico?"}
        ]
    }
)
print(response.json()["choices"][0]["message"]["content"])
```

## Optional Environment Variables

You can override the default model:

```bash
export LLM_CHAT_MODEL_NAME="ollama:granite4:tiny-h"
```

## How It Works

The agent uses a `RequirementAgent` from BeeAI:

1. Detects whether the user mentioned a country.
2. Builds the appropriate `trends24.in` URL.
3. Uses `DuckDuckGoSearchTool` to retrieve trend page results.
4. Extracts and summarizes the top trends.
5. Avoids per-trend searches like `"[Trend Name] news"` to reduce failures and unnecessary tool calls.

## Project Structure

- `src/beeai_agents/agent.py`: OpenAI API server implementation
- `pyproject.toml`: project metadata and dependencies
- `README.md`: setup and usage instructions

## Notes

- Make sure Ollama is running before starting the server.
- DuckDuckGo access may occasionally fail due to network or upstream service issues.