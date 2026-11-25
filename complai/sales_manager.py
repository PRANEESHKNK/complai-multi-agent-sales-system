from agents import Agent
from complai.email_tools import send_email_tool

MANAGER_INSTRUCTIONS = """
You are a Sales Manager at ComplAI. Prepare one strong, accurate cold sales
email using the available sales-agent tools.

Use all three sales-agent tools to generate separate drafts. Compare the
drafts for relevance, clarity, professionalism, credibility, and likely
response. Do not invent product capabilities, customer facts, statistics,
certifications, or guarantees.

Choose one draft only. Then use the email tool once to send the selected
draft. If the tool reports that sending is disabled or failed, report that
accurately. Never claim an email was sent unless the tool confirms submission.
"""


def build_sales_manager(sales_agents: list, manager_model):
    description = "Write one sales email using the supplied task or context."
    writer_tools = [
        agent.as_tool(
            tool_name=f"write_email_{index}",
            tool_description=description,
        )
        for index, agent in enumerate(sales_agents, start=1)
    ]

    return Agent(
        name="Sales Manager",
        instructions=MANAGER_INSTRUCTIONS,
        tools=[*writer_tools, send_email_tool],
        model=manager_model,
    )
