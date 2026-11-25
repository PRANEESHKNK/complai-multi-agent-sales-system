from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

from complai.config import required_env, get_model_names


def build_models():
    names = get_model_names()

    gemini_client = AsyncOpenAI(
        api_key=required_env("GOOGLE_API_KEY"),
        base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
    )
    openrouter_client = AsyncOpenAI(
        api_key=required_env("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1",
    )
    groq_client = AsyncOpenAI(
        api_key=required_env("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1",
    )

    return {
        "gemini": OpenAIChatCompletionsModel(
            model=names["gemini"], openai_client=gemini_client
        ),
        "kimi": OpenAIChatCompletionsModel(
            model=names["openrouter"], openai_client=openrouter_client
        ),
        "oss": OpenAIChatCompletionsModel(
            model=names["groq"], openai_client=groq_client
        ),
        "manager": OpenAIChatCompletionsModel(
            model=names["manager"], openai_client=gemini_client
        ),
        "checker": OpenAIChatCompletionsModel(
            model=names["checker"], openai_client=gemini_client
        ),
    }
