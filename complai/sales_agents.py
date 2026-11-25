
from agents import Agent, ModelSettings

SALES_INSTRUCTIONS = """
You are a sales agent working for ComplAI, a company that provides a SaaS
tool for helping businesses with SOC 2 compliance and audit preparation,
powered by AI.

Write compelling, credible sales emails that are likely to receive a response.

Do not invent customer facts, product capabilities, statistics,
certifications, or guarantees.
"""


def build_sales_agents(models: dict):

    return [
        Agent(
            name="Gemini Sales Agent",
            instructions=SALES_INSTRUCTIONS,
            model=models["gemini"],
        ),

        Agent(
            name="Kimi Sales Agent",
            instructions=SALES_INSTRUCTIONS,
            model=models["kimi"],
            model_settings=ModelSettings(max_tokens=2048),
        ),

        Agent(
            name="GPT-OSS Sales Agent",
            instructions=SALES_INSTRUCTIONS,
            model=models["oss"],
        ),
    ]
