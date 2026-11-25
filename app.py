
import asyncio
from agents import Runner, trace

from complai.models import build_models
from complai.sales_agents import build_sales_agents
from complai.sales_manager import build_sales_manager


TASK = """
Create a cold sales email for a prospective business customer
who may need help preparing for SOC 2 compliance.

Write a compelling, professional and credible email.
Do not invent customer facts or product capabilities.
"""


from openai import APIStatusError
import asyncio

async def run_agent_with_retry(agent, task, retries=3):

    for attempt in range(1, retries + 1):
        try:
            print(f"{agent.name}: Attempt {attempt}")

            result = await Runner.run(agent, task)

            return result

        except APIStatusError as e:

            if e.status_code not in (429, 500, 502, 503, 504):
                raise

            if attempt == retries:
                raise

            wait_time = 2 ** attempt

            print(
                f"{agent.name}: Temporary API error "
                f"{e.status_code}. Retrying in {wait_time}s..."
            )

            await asyncio.sleep(wait_time)

async def main():

    # Step 1: Build model clients
    models = build_models()

    # Step 2: Create three sales agents
    sales_agents = build_sales_agents(models)

    # Step 3: Execute all three agents concurrently
    with trace("ComplAI Parallel Sales Agents"):

        print("\nGenerating three sales email drafts...\n")

        results = await asyncio.gather(
            *[
                run_agent_with_retry(agent, TASK)
                for agent in sales_agents
            ],
            return_exceptions=True,
        )

    # Step 4: Collect successful drafts
    drafts = []

    for agent, result in zip(sales_agents, results):

        if isinstance(result, Exception):
            print(f"FAILED: {agent.name}")
            print(type(result).__name__, str(result))
            continue

        draft = result.final_output

        drafts.append(
            f"\n{agent.name}:\n{draft}\n"
        )

        print(f"SUCCESS: {agent.name}")

    # Step 5: Require all three drafts
    if len(drafts) != 3:
        print(
            f"\nWorkflow stopped: Only {len(drafts)} "
            "out of 3 agents generated drafts."
        )
        return

    # Step 6: Build the Sales Manager
    sales_manager = build_sales_manager(
        manager_model=models["manager"]
    )

    manager_input = (
        "Compare the following three sales email drafts. "
        "Choose the strongest one, explain your choice, "
        "and use the email tool once.\n\n"
        + "\n".join(drafts)
    )

    # Step 7: Manager selects and submits one draft
    with trace("ComplAI Sales Manager"):

        print("\nSales Manager is comparing drafts...\n")

        result = await Runner.run(
            sales_manager,
            manager_input,
        )

    print("\nSALES MANAGER RESULT\n")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
