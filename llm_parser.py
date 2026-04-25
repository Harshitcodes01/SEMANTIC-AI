import json
import re
from functools import lru_cache
from llm import run_llama


# ------------------------
# LLM CALL (CACHED)
# ------------------------
@lru_cache(maxsize=100)
def cached_call(prompt):
    return run_llama(prompt)


# ------------------------
# SAFE JSON EXTRACTION
# ------------------------
def clean_json(text):
    if not text:
        return ""

    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0)

    return ""


# ------------------------
# SMART FALLBACK PARSER
# ------------------------
def smart_fallback_parser(user_input: str):
    text = user_input.lower()

    # -------- intent --------
    if any(w in text for w in ["buy", "purchase"]):
        intent = "buy"
    elif any(w in text for w in ["learn", "study", "notes"]):
        intent = "learn"
    elif any(w in text for w in ["build", "make", "create"]):
        intent = "create"
    elif any(w in text for w in ["find", "search", "best"]):
        intent = "find"
    else:
        intent = "general"

    # -------- entities --------
    entities = {}

    # languages
    for lang in ["java", "python", "c++", "javascript"]:
        if lang in text:
            entities["language"] = lang

    # topics
    for topic in ["oops", "ai", "machine learning", "data structures"]:
        if topic in text:
            entities["topic"] = topic

    # objects
    if "laptop" in text:
        entities["product"] = "laptop"
    if "engine" in text:
        entities["object"] = "engine"

    # -------- constraints --------
    constraints = {}

    budget_match = re.search(r"\d+", text)
    if budget_match:
        constraints["budget"] = int(budget_match.group())

    # -------- context --------
    if "java" in text or "programming" in text:
        context = "education"
    elif "buy" in text:
        context = "shopping"
    elif "engine" in text:
        context = "engineering"
    else:
        context = "general"

    # goal
    if intent == "learn":
        goal = "understand concepts"
    elif intent == "buy":
        goal = "find best option"
    elif intent == "create":
        goal = "build solution"
    else:
        goal = "unknown"

    return {
        "intent": intent,
        "entities": entities,
        "constraints": constraints,
        "context": context,
        "goal": goal
    }


# ------------------------
# MAIN PARSER
# ------------------------
def parse_prompt(user_input: str):
    prompt = f"""
You are a universal AI parser.

Return ONLY valid JSON.

Format:
{{
  "intent": "",
  "entities": {{}},
  "constraints": {{}},
  "context": "",
  "goal": ""
}}

Input:
{user_input}
"""

    raw = cached_call(prompt)
    cleaned = clean_json(raw)

    print("RAW:", raw)
    print("CLEANED:", cleaned)

    # -------- try LLM --------
    if cleaned and cleaned != "{}":
        try:
            parsed = json.loads(cleaned)

            if isinstance(parsed, dict) and parsed.get("intent"):
                return parsed

        except:
            pass

    # -------- fallback --------
    print("⚠️ Using smart fallback parser")
    return smart_fallback_parser(user_input)