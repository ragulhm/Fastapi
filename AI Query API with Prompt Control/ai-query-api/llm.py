# llm.py

import requests
from config import OPENROUTER_API_KEY, MODEL_NAME

def get_llm_response(prompt: str) -> str:
    """
    Sends a prompt to the OpenRouter API and gets a response from the specified model.
    """
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY is not set. Please set it as an environment variable.")

    try:
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        # Handle connection errors, timeouts, etc.
        raise RuntimeError(f"API request failed: {e}")
    except (KeyError, IndexError) as e:
        # Handle unexpected API response format
        raise RuntimeError(f"Failed to parse API response: {e}")

