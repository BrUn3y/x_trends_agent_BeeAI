import asyncio
import os
import sys
import traceback

from beeai_framework.agents.requirement import RequirementAgent
from beeai_framework.agents.requirement.requirements.conditional import ConditionalRequirement
from beeai_framework.backend import ChatModel
from beeai_framework.errors import FrameworkError
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.think import ThinkTool
from beeai_framework.tools.tool import Tool
from dotenv import load_dotenv

load_dotenv()

INSTRUCTIONS = (
    "Your goal is to be a friendly and insightful analyst of X (formerly Twitter) trends. "
    "1. First, analyze the user's query to identify if a specific country is mentioned. "
    "2. If a country is mentioned (e.g., 'Mexico', 'Spain'), construct the URL for that country on trends24.in (e.g., https://trends24.in/mexico/). If not, use the main page https://trends24.in/. "
    "3. Use the DuckDuckGo tool to get the content of that specific URL. From the result, extract the top 5 trending topics. "
    "4. Do not perform a separate search for each individual trend. Use only the information already retrieved from the trends page results. If the context is insufficient, say that there is not enough information. "
    "5. Never perform searches in the form '[Trend Name] news', 'what happened with [Trend Name]' or 'why is [Trend Name] trending'. "
    "6. Finally, synthesize all the information into a single, coherent summary report. For each trend, provide a simple explanation of the context you found as if you were explaining it to a friend. Use emojis (💡, 📰, etc.) to make it engaging."
)


def create_trends_agent() -> RequirementAgent:
    return RequirementAgent(
        llm=ChatModel.from_name(os.getenv("LLM_CHAT_MODEL_NAME", "ollama:granite4:tiny-h")),
        tools=[ThinkTool(), DuckDuckGoSearchTool()],
        instructions=INSTRUCTIONS,
        requirements=[
            ConditionalRequirement(DuckDuckGoSearchTool, min_invocations=2, max_invocations=7),
            ConditionalRequirement(ThinkTool, min_invocations=1),
        ],
        middlewares=[GlobalTrajectoryMiddleware(included=[Tool])],
    )


async def main() -> None:
    agent = create_trends_agent()

    prompt = " ".join(sys.argv[1:]).strip()
    if not prompt:
        prompt = os.getenv("X_TRENDS_PROMPT", "What are the 5 most important trends in the United States?")

    response = await agent.run(prompt, max_iterations=8, max_retries_per_step=3, total_max_retries=10)
    print(response.last_message.text)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except FrameworkError as e:
        traceback.print_exc()
        sys.exit(e.explain())