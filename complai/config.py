
import os
from dotenv import load_dotenv

load_dotenv(override=True)


def required_env(name: str) -> str:
    value = os.getenv(name, "").strip()

    if not value:
        raise RuntimeError(
            f"Missing {name}. Add it to your local .env file."
        )

    return value


def get_model_names() -> dict[str, str]:
    return {
        "gemini": os.getenv(
            "MODEL_GEMINI", "gemini-3.1-flash-lite"
        ),
        "openrouter": os.getenv(
            "MODEL_OPENROUTER", "moonshotai/kimi-k2.6"
        ),
        "groq": os.getenv(
            "MODEL_GROQ", "openai/gpt-oss-120b"
        ),
        "manager": os.getenv(
            "MODEL_MANAGER", "gemini-3.1-flash-lite"
        ),
        "checker": os.getenv(
            "MODEL_CHECKER", "gemini-3.1-flash-lite"
        ),
    }
