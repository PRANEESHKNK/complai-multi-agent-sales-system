
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI
from complai.config import required_env, get_model_names

load_dotenv()
names = get_model_names()

providers = {
    "Gemini": {
        "key": "GOOGLE_API_KEY",
        "url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "model": names["gemini"],
    },
    "OpenRouter": {
        "key": "OPENROUTER_API_KEY",
        "url": "https://openrouter.ai/api/v1",
        "model": names["openrouter"],
    },
    "Groq": {
        "key": "GROQ_API_KEY",
        "url": "https://api.groq.com/openai/v1",
        "model": names["groq"],
    },
}

async def test_provider(name, config):
    print(f"\nTesting {name}...")

    try:
        client = AsyncOpenAI(
            api_key=required_env(config["key"]),
            base_url=config["url"],
            max_retries=1,
        )

        response = await client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": "Reply with Hello"}],
        )

        print("SUCCESS:", response.choices[0].message.content)

    except Exception as e:
        print("FAILED:", type(e).__name__, str(e))

async def main():
    for name, config in providers.items():
        await test_provider(name, config)

asyncio.run(main())
