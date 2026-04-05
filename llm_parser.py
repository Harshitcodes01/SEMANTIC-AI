import subprocess
import json

OLLAMA_PATH = r"C:\Users\Harshit\AppData\Local\Programs\Ollama\ollama.exe"


def call_ollama(prompt):
    result = subprocess.run(
        [OLLAMA_PATH, "run", "llama3"],
        input=prompt,
        text=True,
        capture_output=True
    )
    return result.stdout


def clean_json(text):
    start = text.find("{")
    end = text.rfind("}") + 1
    return text[start:end]


def parse_prompt(user_input: str):
    prompt = f"""
You are a strict scientific system.

Convert input into VALID JSON ONLY.

Rules:
- No explanation
- No extra text
- Only JSON
- Follow schema strictly

Schema:
{{
  "crop": "",
  "location": "",
  "temperature": number,
  "stress": [],
  "traits_required": []
}}

Input:
{user_input}
"""

    raw = call_ollama(prompt)

    try:
        return json.loads(clean_json(raw))
    except:
        return {"error": "invalid_json", "raw": raw}