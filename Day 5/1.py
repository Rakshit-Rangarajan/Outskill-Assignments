from __future__ import annotations

import os
from typing import Any
from dotenv import load_dotenv
load_dotenv()


OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
DEFAULT_MODEL = "openai/gpt-4o-mini"


def resolve_api_key(api_key: str | None = None) -> str:
    """Return an API key from the function argument or environment."""
    # TODO 1: return the stripped api_key if provided.
    print("[TODO 1] Checking if api_key is provided...")
    if api_key and api_key.strip():
        print("[TODO 1] Using provided api_key.")
        return api_key.strip()
    # TODO 2: otherwise read OPENROUTER_API_KEY from the environment.
    print("[TODO 2] Checking environment for OPENROUTER_API_KEY...")
    env_key = os.getenv("OPENROUTER_API_KEY")
    if env_key and env_key.strip():
        print("[TODO 2] Using OPENROUTER_API_KEY from environment.")
        return env_key.strip()
    # TODO 3: raise ValueError if neither exists.
    print("[TODO 3] No API key found. Raising error.")
    raise ValueError("OpenRouter API key not provided. Set OPENROUTER_API_KEY in environment or pass as argument.")


def create_openrouter_client(api_key: str) -> Any:
    """Create an OpenAI SDK client configured for OpenRouter."""
    # TODO 4: return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)
    print("[TODO 4] Creating OpenAI client for OpenRouter...")
    from openai import OpenAI
    return OpenAI(base_url=OPENROUTER_BASE_URL, api_key=api_key)


def build_text_messages(
    user_prompt: str,
    history: list[dict[str, Any]] | None = None,
) -> list[dict[str, str]]:
    """Convert prior chat history plus the new prompt into OpenRouter messages."""
    messages: list[dict[str, str]] = []

    for item in history or []:
        role = item.get("role")
        content = item.get("content")
        if role in {"user", "assistant"} and isinstance(content, str) and content.strip():
            # TODO 5: append the previous message as {"role": role, "content": content.strip()}
            print(f"[TODO 5] Appending previous message: role={role}")
            messages.append({"role": role, "content": content.strip()})

    # TODO 6: append the latest user prompt.
    print("[TODO 6] Appending latest user prompt.")
    messages.append({"role": "user", "content": user_prompt.strip()})
    return messages


def ask_text_model(
    prompt: str,
    api_key: str | None = None,
    model: str = DEFAULT_MODEL,
    history: list[dict[str, Any]] | None = None,
) -> str:
    """Send one text-only chat request and return the assistant response."""
    print("[TODO 7] Creating OpenRouter client and sending chat request...")
    client = create_openrouter_client(resolve_api_key(api_key))

    response = client.chat.completions.create(
        model=model,
        messages=build_text_messages(prompt, history),
        extra_body={"provider": {"data_collection": "deny"}}
    )
    print("[TODO 8] Returning assistant response.")
    # OpenAI SDK returns objects, not dicts. Use dot notation.
    if hasattr(response, "choices") and response.choices:
        message = response.choices[0].message
        if hasattr(message, "content"):
            return message.content or ""
    return ""


if __name__ == "__main__":
    user_prompt = input("Enter your prompt: ")
    print(ask_text_model(user_prompt))
