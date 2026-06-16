# X Trends Agent - MCP Server

## Introduction

The X Trends Agent is an AI-powered conversational agent designed to analyze trending topics on X (formerly Twitter). It is built with the **BeeAI framework** and exposes a **Model Context Protocol (MCP) Server** to integrate with external systems supporting the MCP standard.

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
git clone --branch MCP_server --single-branch https://github.com/BrUn3y/x_trends_agent_BeeAI.git
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

## Running the MCP Server

The MCP server runs with stdio transport (standard input/output). Bob will automatically start and manage the server process.

For local development, you can also run it directly:

```bash
uv run src/beeai_agents/agent.py
```

## Usage

The MCP server exposes the trends agent as a tool available to MCP clients. Bob automatically manages the server process via stdio.

Example with an MCP client configuration (IBM Bob):

```json
{
  "mcpServers": {
    "x-trends-agent": {
      "command": "uv",
      "args": ["run", "src/beeai_agents/agent.py"],
      "cwd": "/path/to/x_trends_agent_BeeAI"
    }
  }
}
```

**For deploying on a remote server**, you would need to configure a separate HTTP MCP server wrapper.

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

- `src/beeai_agents/agent.py`: MCP server implementation
- `pyproject.toml`: project metadata and dependencies
- `README.md`: setup and usage instructions

## Notes

- Make sure Ollama is running before starting the server.
- DuckDuckGo access may occasionally fail due to network or upstream service issues.
- The MCP server uses stdio transport by default.