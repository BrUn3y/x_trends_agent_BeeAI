import os
import asyncio
from collections.abc import AsyncGenerator

from a2a.types import AgentSkill, Message
from a2a.utils.message import get_message_text
from agentstack_sdk.server import Server
from agentstack_sdk.server.context import RunContext
from agentstack_sdk.a2a.types import AgentMessage
from agentstack_sdk.a2a.extensions import AgentDetail, AgentDetailTool

from beeai_framework.agents.experimental import RequirementAgent
from beeai_framework.agents.experimental.requirements.conditional import ConditionalRequirement
from beeai_framework.middleware.trajectory import GlobalTrajectoryMiddleware
from beeai_framework.tools.search.duckduckgo import DuckDuckGoSearchTool
from beeai_framework.tools.think import ThinkTool
from beeai_framework.backend import ChatModel

INSTRUCTIONS = (
    "Your goal is to be a friendly and insightful analyst of X (formerly Twitter) trends. "
    "1. First, analyze the user's query to identify if a specific country is mentioned. "
    "2. If a country is mentioned (e.g., 'Mexico', 'Spain'), construct the URL for that country on trends24.in (e.g., https://trends24.in/mexico/). If not, use the main page https://trends24.in/. "
    "3. Use the DuckDuckGo tool to get the content of that specific URL. From the result, extract the top 5 trending topics. "
    "4. For each of the top 5 trends, perform a new, specific search using queries like '[Trend Name] news', 'what happened with [Trend Name]', or 'why is [Trend Name] trending' to find the immediate reason for the trend. "
    "5. Finally, synthesize all the information into a single, coherent summary report. For each trend, provide a simple explanation of the context you found as if you were explaining it to a friend. Use emojis (💡, 📰, etc.) to make it engaging. You MUST include the source URL of the news article where you found the context."
)

AGENT_DETAIL = AgentDetail(
    user_greeting="Hello! I analyze X trends",
    version="1.0.0",
    framework="BeeAI",
    author={"name": "Edgar Bruney"},
    tools=[
        AgentDetailTool(name="Think", description="Advanced reasoning and analysis."),
        AgentDetailTool(name="DuckDuckGo", description="Search the web for current information.")
    ],
)

AGENT_SKILLS = [
    AgentSkill(
        id="x-trends-agent",
        name="X Trends Agent",
        description="This Agent is an AI-powered conversational tool for accessing trends on X.",
        tags=["Chat"],
        examples=[
            "What are the 5 most important trends in the United States?",
            "What is the most relevant news in Mexico today?"
        ]
    )
]

server = Server()

def create_trends_agent():
    return RequirementAgent(
        llm=ChatModel.from_name("ollama:granite4:tiny-h"),
        tools=[ThinkTool(), DuckDuckGoSearchTool()],
        instructions=INSTRUCTIONS,
        requirements=[
            ConditionalRequirement(DuckDuckGoSearchTool, min_invocations=2, max_invocations=7),
            ConditionalRequirement(ThinkTool, min_invocations=1),
        ]
    )

@server.agent(name="X Trends Agent", detail=AGENT_DETAIL, skills=AGENT_SKILLS)
async def simple_trends_agent(input: Message, context: RunContext) -> AsyncGenerator[AgentMessage, None]:
    user_query = get_message_text(input)
    print(f"--- Agent received query: '{user_query}' ---")

    agent = create_trends_agent()
    
    run_context = await agent.run(user_query).middleware(GlobalTrajectoryMiddleware())

    print(f"--- Agent finished processing. ---")
    
    try:
        final_answer = run_context.output_structured.response
    except Exception as e:
        final_answer = f"Error: Could not parse the final answer. Details: {e}"
        print(f"--- DEBUG: Failed to parse response. Full run_context: {run_context} ---")

    yield AgentMessage(text=final_answer)

def run():
    print("Starting server...")
    server.run(host=os.getenv("HOST", "127.0.0.1"), port=int(os.getenv("PORT", 8000)))

if __name__ == "__main__":
    run()
