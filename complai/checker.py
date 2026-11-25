from pydantic import BaseModel, Field
from agents import Agent, Runner

from complai.models import build_models


class EmailReview(BaseModel):
    is_professional: bool = Field(
        description="Whether the email is professional and appropriate."
    )
    number_of_sentences: int = Field(
        description="Number of body sentences, excluding greeting and signature."
    )
    contains_placeholders: bool = Field(
        description="Whether the email contains personalization placeholders."
    )


async def review_email(email: str):
    models = build_models()
    checker = Agent(
        name="Checker",
        instructions=(
            "Review the supplied sales email. Evaluate professionalism, "
            "count body sentences excluding greeting and signature, and "
            "identify unresolved personalization placeholders."
        ),
        model=models["checker"],
        output_type=EmailReview,
    )
    result = await Runner.run(checker, email)
    return result.final_output
