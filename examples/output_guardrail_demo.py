"""Optional output-guardrail example adapted from the learning notebook."""

import asyncio
from agents import (
    Agent,
    Runner,
    output_guardrail,
    GuardrailFunctionOutput,
    OutputGuardrailTripwireTriggered,
)

from complai.checker import EmailReview
from complai.models import build_models
from complai.sales_agents import SALES_INSTRUCTIONS


async def main():
    models = build_models()
    checker = Agent(
        name="Checker",
        instructions="Review potential sales emails.",
        model=models["checker"],
        output_type=EmailReview,
    )

    @output_guardrail
    async def email_guardrail(ctx, agent, message):
        review_result = await Runner.run(
            checker, message, context=ctx.context
        )
        review = review_result.final_output
        is_problem = (
            review.contains_placeholders or not review.is_professional
        )
        return GuardrailFunctionOutput(
            output_info={"review": review},
            tripwire_triggered=is_problem,
        )

    cowboy = Agent(
        name="Cowboy",
        instructions=SALES_INSTRUCTIONS + "\nSpeak like a cowboy.",
        model=models["gemini"],
        output_guardrails=[email_guardrail],
    )

    try:
        result = await Runner.run(cowboy, "Write a cold sales email.")
        print(result.final_output)
    except OutputGuardrailTripwireTriggered:
        print("Email rejected by the output guardrail.")


if __name__ == "__main__":
    asyncio.run(main())
