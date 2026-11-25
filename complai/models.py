
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

from complai.config import required_env, get_model_names


def build_models():
    names = get_model_names()

    # 1. Gemini client
    gemini_client = AsyncOpenAI(
        api_key=required_env("GOOGLE_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )

    # 2. OpenRouter client
    openrouter_client = AsyncOpenAI(
        api_key=required_env("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )

    # 3. Groq client
    groq_client = AsyncOpenAI(
        api_key=required_env("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )

    return {
        # Sales Agent 1
        "gemini": OpenAIChatCompletionsModel(
            model=names["gemini"],
            openai_client=gemini_client,
        ),

        # Sales Agent 2
        "kimi": OpenAIChatCompletionsModel(
            model=names["openrouter"],
            openai_client=openrouter_client,
        ),

        # Sales Agent 3
        "oss": OpenAIChatCompletionsModel(
            model=names["groq"],
            openai_client=groq_client,
        ),

        # Sales Manager - using Groq
        "manager": OpenAIChatCompletionsModel(
            model=names["manager"],
            openai_client=groq_client,
        ),

        # Email Checker - using Gemini
        "checker": OpenAIChatCompletionsModel(
            model=names["checker"],
            openai_client=gemini_client,
        ),
    }
