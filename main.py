from workflow import build_graph
from vector_search import load_data

# ---------------------------
# INIT SYSTEM (RUN ONCE)
# ---------------------------
print("Initializing system...")

load_data()          # ✅ Load vector DB once
graph = build_graph()  # ✅ Build graph once


# ---------------------------
# PIPELINE FUNCTION
# ---------------------------
def run_pipeline(user_input):
    result = graph.invoke({
        "input": user_input,
        "retries": 0
    })
    return result["final"]


# ---------------------------
# CLI LOOP
# ---------------------------
if __name__ == "__main__":
    while True:
        user_input = input("\nEnter prompt: ")

        result = run_pipeline(user_input)

        print("\nFINAL OUTPUT:\n")
        print(result)