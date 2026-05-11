# X Trends Agent - Built with BeeAI

## Introduction

The X Trends Agent is an AI-powered conversational agent designed to analyze trending topics on X (formerly Twitter). It is built with the **BeeAI framework** and runs locally using **Ollama** with the **IBM Granite 4 Tiny** model.

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
git clone --branch without_agentstack --single-branch https://github.com/BrUn3y/x_trends_agent_BeeAI.git
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

## Running the Agent

Run the agent directly with a prompt:

```bash
uv run src/beeai_agents/agent.py "What are the 5 most important trends in Mexico?"
```

You can also run it without arguments:

```bash
uv run src/beeai_agents/agent.py
```

In that case, it uses the default fallback prompt.

## Optional Environment Variables

You can override the default model:

```bash
export LLM_CHAT_MODEL_NAME="ollama:granite4:tiny-h"
```

You can also provide a default prompt through an environment variable:

```bash
export X_TRENDS_PROMPT="What are the 5 most important trends in Spain?"
uv run src/beeai_agents/agent.py
```

## How It Works

The agent uses a `RequirementAgent` from BeeAI:

1. Detects whether the user mentioned a country.
2. Builds the appropriate `trends24.in` URL.
3. Uses `DuckDuckGoSearchTool` to retrieve trend page results.
4. Extracts and summarizes the top trends.
5. Avoids per-trend searches like `"[Trend Name] news"` to reduce failures and unnecessary tool calls.

## Project Structure

- `src/beeai_agents/agent.py`: main BeeAI standalone agent
- `pyproject.toml`: project metadata and dependencies
- `README.md`: setup and usage instructions

## Notes

- Make sure Ollama is running before executing the agent.
- The project no longer depends on AgentStack.
- DuckDuckGo access may occasionally fail due to network or upstream service issues.