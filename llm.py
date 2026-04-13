import requests

def run_llama(prompt: str, model: str = "llama3"):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"]

    except Exception as e:
        print("LLM Error:", e)
        return ""