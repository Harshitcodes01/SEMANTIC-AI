from workflow import build_graph
from vector_search import load_data
from llm_parser import parse_prompt

print("Initializing system...")

load_data()
graph = build_graph()


def run_pipeline(user_input):
    result = graph.invoke({
        "input": user_input,
        "retries": 0
    })
    return result["final"]


if __name__ == "__main__":
    while True:
        user_input = input("\nEnter prompt: ")

        parsed = parse_prompt(user_input)

        if parsed.get("context") == "agriculture":
            result = run_pipeline(user_input)
        else:
            result = {
                "mode": "universal_parser",
                "parsed_output": parsed
            }

        print("\nOUTPUT:\n")
        print(result)