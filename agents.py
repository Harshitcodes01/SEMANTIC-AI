import subprocess
import json

# ----------------------------------------
# OLLAMA PATH (IMPORTANT)
# ----------------------------------------
OLLAMA_PATH = r"C:\Users\Harshit\AppData\Local\Programs\Ollama\ollama.exe"


# ----------------------------------------
# BASE FUNCTIONS
# ----------------------------------------
def run_llama(prompt):
    result = subprocess.run(
    [OLLAMA_PATH, "run", "llama3"],
    input=prompt,
    text=True,
    capture_output=True,
    encoding="utf-8",      
    errors="ignore"        
)
    
    return result.stdout


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
def scientist_agent(plan):
    prompt = f"""
You are a domain scientist.

Given this plan:
{plan}

Suggest scientific traits and mechanisms.

Rules:
- Only JSON
- No explanation

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
            "traits": [],
            "mechanisms": []
        }


# ----------------------------------------
# AGENT 3: GENERATOR
# ----------------------------------------
def generator_agent(plan, science):
    prompt = f"""
You are a STRICT JSON generator.

Your job:
Combine plan + science into valid structured JSON.

DO NOT FAIL.

Rules:
- ONLY JSON (no explanation)
- ALL fields must exist
- temperature must be number
- traits must be list
- scientific_basis must be list
- confidence must be between 0 and 1

Plan:
{plan}

Science:
{science}

Return EXACTLY this schema:
{{
  "crop": "",
  "location": "",
  "temperature": 0,
  "stress": [],
  "traits": [],
  "scientific_basis": [],
  "confidence": 0.8
}}
"""
    output = run_llama(prompt)

    try:
        return json.loads(extract_json(output))
    except:
        return {
            "crop": "unknown",
            "location": "unknown",
            "temperature": 0,
            "stress": [],
            "traits": [],
            "scientific_basis": [],
            "confidence": 0.0
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