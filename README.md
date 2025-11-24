# X Trends Agent

## Introduction

The X Trends Agent is an AI-powered conversational system designed to analyze trending topics on X (formerly Twitter). Built on the BeeAI framework with AgentStack SDK, it specializes in identifying trending topics by country, researching the context behind each trend, and providing friendly, engaging summaries with emojis and source citations.


## Requirements

### Minimum Requirements

- **Python:** Version 3.11 or higher.
- **Dependency Management:** `uv` is used for managing Python packages.
- **Ollama:** Required for running the local LLM (`granite4:tiny-h`).

### Python Dependencies

The project's dependencies are managed by `uv` and are defined in `pyproject.toml`. The main dependencies are:

- `agentstack-sdk==0.4.0rc1`
- `beeai_framework>=0.1.68`

A complete list of all transient dependencies is available in the `uv.lock` file.

### Tools Used

The agent uses the following BeeAI tools:

- **ThinkTool:** Advanced reasoning and analysis for complex queries.
- **DuckDuckGoSearchTool:** Web search for retrieving trending topics and news articles.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd x_trends_agent
    ```

2.  **Install dependencies:**
    Ensure you have `uv` installed. Then, run the following command to install the required Python packages into a virtual environment:
    ```bash
    uv sync
    ```

3.  **Install Ollama and the model:**
    ```bash
    # Install Ollama (if not already installed)
    # Visit https://ollama.ai for installation instructions
    
    # Pull the granite4 model
    ollama pull granite4:tiny-h
    ```

## Running the Agent

1.  **Start the agent:**
    Use `uv` to run the agent server:
    ```bash
    uv run server
    ```
    The agent will start and be ready to receive requests on `http://127.0.0.1:8000` by default.

## Usage

You can interact with the agent by asking about trending topics on X (Twitter). The agent can analyze trends globally or for specific countries.

### Example Queries

- "What are the 5 most important trends in the United States?"
- "What is the most relevant news in Mexico today?"
- "What's trending in Spain right now?"
- "Tell me about the top trends on X"

### How It Works

1. **Country Detection:** The agent analyzes your query to identify if a specific country is mentioned.
2. **Trend Retrieval:** It searches trends24.in for the top 5 trending topics in that country (or globally).
3. **Context Research:** For each trend, it performs targeted web searches to find out why it's trending.
4. **Summary Report:** It synthesizes all information into a friendly, engaging summary with emojis and source URLs.

## Consuming the Agent (A2A Example)

You can interact with the agent using the `a2a-sdk`. The following is a basic example of how to send a query to the agent and receive a response.

```python
import asyncio
from a2a.client import Client
from a2a.types import Message

async def main():
    """
    Connects to the X Trends Agent and sends a query.
    """
    agent_url = "http://127.0.0.1:8000"  # Assuming the agent is running locally

    try:
        async with Client(agent_url) as client:
            # The query to send to the agent
            query = "What are the 5 most important trends in the United States?"
            
            # Create a message
            message = Message(content=query.encode("utf-8"), content_type="text/plain")

            print(f"Sending query: '{query}'")

            # Send the message and get the response
            response_stream = await client.send_message(message)

            # Process the response stream
            async for response_message in response_stream:
                if response_message.content_type == "text/plain":
                    print("Agent response:", response_message.content.decode("utf-8"))
                else:
                    print("Received non-text response.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Agent Configuration

The agent uses the following configuration:

- **LLM:** `ollama:granite4:tiny-h` (local model via Ollama)
- **Requirements:**
  - DuckDuckGo searches: 2-7 invocations per query
  - Think tool: minimum 1 invocation per query

## Future Improvements

| Feature | Description |
|---|---|
| Multi-language Support | Add support for analyzing trends in different languages. |
| Trend History | Track and compare trends over time. |
| Custom Trend Sources | Support for additional trend tracking platforms beyond trends24.in. |
| Sentiment Analysis | Analyze the sentiment around trending topics. |

## Notes

- The agent uses `GlobalTrajectoryMiddleware` for debugging and observability during development.
- All web searches are performed using DuckDuckGo to ensure privacy and avoid API rate limits.

## Disclaimer

This agent is functional for its intended purpose but is still under active development. The use of this agent in a production environment is at your own risk. The authors are not responsible for any issues that may arise from its use in a production setting.