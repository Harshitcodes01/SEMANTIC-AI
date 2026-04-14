from langgraph.graph import StateGraph
from typing import TypedDict

from llm_parser import parse_prompt
from vector_search import search_traits
from research import fetch_research_insights
from spec_generator import generate_final_spec
from validator import validate_spec
#from research import fetch_research_insights


# ---------------------------
# STATE DEFINITION
# ---------------------------
class State(TypedDict):
    input: str
    parsed: dict
    traits: list
    insights: list
    final: dict
    valid: bool
    retries: int   


# ---------------------------
# RETRY LOGIC FOR PARSING
# ---------------------------
def parse_with_retry(user_input, max_attempts=3):
    for attempt in range(max_attempts):
        result = parse_prompt(user_input)

        if "error" not in result:
            return result

        print(f"Retry parsing... attempt {attempt + 1}")

    return {"error": "failed_after_retries"}


# ---------------------------
# NODES
# ---------------------------
def parse_node(state: State):
    print("Step 1: Parsing prompt...")

    state["parsed"] = parse_with_retry(state["input"])
    return state


def search_node(state: State):
    print("Step 2: Vector searching traits...")

    traits = search_traits(state["input"])

    # Take top 3 traits only
    state["traits"] = traits[:3]

    return state


#from .research import fetch_research

def research_node(state: State):
    print("Step 3: Fetching research...")

    traits = [t["trait"] for t in state.get("traits", [])]

    if not traits:
        state["insights"] = []   # ✅ fallback
        return state

    insights = fetch_research_insights(traits)

    state["insights"] = insights

    return state


def generate_node(state: State):
    print("Step 4: Generating final spec...")

    # Handle case where parsing failed
    if "error" in state["parsed"]:
        state["final"] = {
            "crop": "unknown",
            "location": "unknown",
            "temperature": 0,
            "stress": [],
            "traits": [],
            "scientific_basis": [],
            "confidence": 0.0
        }
        return state

    state["final"] = generate_final_spec(
        state["parsed"],
        state["traits"],
        state.get("insights", [])
    )
    return state


def validate_node(state: State):
    print("Step 5: Validating output...")

    validated, ok = validate_spec(state["final"])

    
    state["final"] = validated

    state["valid"] = ok

    if not ok:
        state["retries"] += 1

        print(f"Validation failed. Retry count: {state['retries']}")

        # ✅ STOP after 3 retries
        if state["retries"] >= 3:
            print("Max retries reached. Using fallback.")

            state["final"] = {
                "crop": "unknown",
                "location": "unknown",
                "temperature": 0,
                "stress": [],
                "traits": [],
                "scientific_basis": state.get("research", []),
                "confidence": 0.0
            }

            state["valid"] = True  # force exit

    return state


# ---------------------------
# ROUTER (RETRY CONTROL)
# ---------------------------
def retry_router(state: State):
    if not state["valid"]:
        return "generate"   # retry generation
    return "end"


# ---------------------------
# BUILD GRAPH
# ---------------------------
def build_graph():
    graph = StateGraph(State)

    # Nodes
    graph.add_node("parse", parse_node)
    graph.add_node("search", search_node)
    graph.add_node("research", research_node)
    graph.add_node("generate", generate_node)
    graph.add_node("validate", validate_node)

    # Entry
    graph.set_entry_point("parse")

    # Flow
    graph.add_edge("parse", "search")
    graph.add_edge("search", "research")
    graph.add_edge("research", "generate")
    graph.add_edge("generate", "validate")

    # Retry loop
    graph.add_conditional_edges(
        "validate",
        retry_router,
        {
            "generate": "generate",
            "end": "__end__"
        }
    )

    return graph.compile()


def run_pipeline(user_input: str):
    graph = build_graph()
    result = graph.invoke({
        "input": user_input,
        "retries": 0
    })
    return result["final"]