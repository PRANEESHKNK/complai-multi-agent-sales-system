import asyncio
from agents import Runner, trace

from complai.models import build_models
from complai.sales_agents import build_sales_agents
from complai.sales_manager import build_sales_manager

TASK = """
Create a cold sales email for a prospective business customer who may need
help preparing for SOC 2 compliance. Use each of the three sales-agent tools
to create a draft, compare them, choose one, and use the email tool once.
"""


async def main():
    models = build_models()
    sales_agents = build_sales_agents(models)
    sales_manager = build_sales_manager(
        sales_agents=sales_agents,
        manager_model=models["manager"],
    )

    with trace("ComplAI Multi-Agent Sales Workflow"):
        result = await Runner.run(sales_manager, TASK)

    print("\nSALES MANAGER RESULT\n")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
