from workflow import build_graph

if __name__ == "__main__":
    graph = build_graph()

    user_input = input("Enter prompt: ")

    result = graph.invoke({
    "input": user_input,
    "retries": 0   
})

    print("\nFINAL OUTPUT:\n")
    print(result["final"])