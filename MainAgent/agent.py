from google.adk.agents.llm_agent import Agent
import os
import json

def get_context(file_path):
    with open(file_path, 'r') as f:
        return f.read()

root_agent = Agent(
    model='gemini-1.5-pro-002', # Assuming access to your preferred model
    name='root_agent',
    description='Orchestrator for the PGame development pipeline.',
    instruction=(
        "You are a Senior Technical Architect. "
        "Your task is to read the .md files in the /agents directory and the roadmap.json. "
        "Use these to spawn sub-agents for specific tasks (e.g., SentimentConcierge, SecurityAgent). "
        "Always maintain consistency with the existing FastAPI backend structure."
    ),
)

# Example: Loading a spec to initialize a sub-agent
sentiment_spec = get_context('agents/SentimentConcierge.md')
# You would then instantiate the sub-agent using this context