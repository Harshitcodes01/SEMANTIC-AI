import subprocess
import json
from scoring import compute_confidence

# ----------------------------------------
# OLLAMA PATH (IMPORTANT)
# ----------------------------------------
OLLAMA_PATH = r"C:\Users\Harshit\AppData\Local\Programs\Ollama\ollama.exe"


# ----------------------------------------
# BASE FUNCTIONS
# ----------------------------------------
'''def run_llama(prompt):
    result = subprocess.run(
    [OLLAMA_PATH, "run", "llama3"],
    input=prompt,
    text=True,
    capture_output=True,
    encoding="utf-8",      
    errors="ignore"        
)
    
    return result.stdout'''
def run_llama(prompt):
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", "llama3"],
            input=prompt,
            text=True,
            capture_output=True,
            encoding="utf-8",
            errors="ignore",
            timeout=20   # ✅ ADD THIS
        )

        return result.stdout

    except Exception as e:
        print("LLM Error:", e)
        return "{}"   # ✅ fallback JSON


def extract_json(text):
    start = text.find("{")
    end = text.rfind("}") + 1
    return text[start:end]


# ----------------------------------------
# AGENT 1: PLANNER
# ----------------------------------------
def planner_agent(user_input):
    prompt = f"""
You are a scientific planner.

Break the user input into structured requirements.

Rules:
- Only JSON
- No explanation

Return JSON:
{{
  "crop": "",
  "environment": "",
  "conditions": [],
  "goals": []
}}

Input:
{user_input}
"""
    output = run_llama(prompt)

    try:
        return json.loads(extract_json(output))
    except:
        return {
            "crop": "unknown",
            "environment": "unknown",
            "conditions": [],
            "goals": []
        }


# ----------------------------------------
# AGENT 2: SCIENTIST
# ----------------------------------------
def scientist_agent(plan, traits):
    prompt = f"""
You are an agricultural scientist.

Input plan:
{plan}

Relevant traits from database:
{traits}

Task:
- Select ONLY traits relevant to the environment
- If climate is cold → choose cold tolerance traits
- Remove irrelevant traits

Return JSON:
{{
  "traits": [],
  "mechanisms": []
}}
"""
    output = run_llama(prompt)

    try:
        return json.loads(extract_json(output))
    except:
        return {
            "traits": traits,
            "mechanisms": []
        }



# ----------------------------------------
# AGENT 4: VALIDATOR (SMART FIXER)
# ----------------------------------------
def validator_agent(data):
    prompt = f"""
Fix this JSON to make it valid and complete.

Rules:
- Return only JSON
- Ensure all fields exist
- No explanation

Input:
{data}
"""
    output = run_llama(prompt)

    try:
        return json.loads(extract_json(output)), True
    except:
        return data, False