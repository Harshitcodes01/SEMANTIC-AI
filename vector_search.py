from sentence_transformers import SentenceTransformer
import chromadb

# --------------------------
# LOAD MODEL
# --------------------------
model = SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------
# INIT DB
# --------------------------
client = chromadb.Client()
collection = client.get_or_create_collection(name="traits")


# --------------------------
# LOAD DATA (RUN ONCE)
# --------------------------
def load_data():
    traits_data = [
        "deep root system",
        "heat shock protein expression",
        "waxy leaf coating",
        "drought tolerance",
        "low water requirement",
        "high yield efficiency",
        "salt tolerance"
    ]

    # Clear old data (important during dev)
    try:
        client.delete_collection("traits")
    except:
        pass

    global collection
    collection = client.get_or_create_collection(name="traits")

    for i, trait in enumerate(traits_data):
        embedding = model.encode(trait).tolist()

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[trait]
        )


# --------------------------
# SEARCH FUNCTION
# --------------------------
def search_traits(query: str, top_k=5):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    traits = results["documents"][0]

    # Add simple ranking score (placeholder)
    return [
        {"trait": trait, "score": 1.0 - (i * 0.1)}
        for i, trait in enumerate(traits)
    ]