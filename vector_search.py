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

collection = None
#collection = client.get_or_create_collection(name="traits")


# --------------------------
# LOAD DATA (RUN ONCE)
# --------------------------
def load_data():
    global collection

    collection = client.get_or_create_collection(name="traits")
    traits_data = [
        {
            "trait": "deep root system",
            "stress": ["drought"],
            "mechanism": "access deeper water from soil",
            "crop_relevance": ["wheat", "rice"]
        },
        {
            "trait": "heat shock protein expression",
            "stress": ["heat"],
            "mechanism": "protects proteins under high temperature",
            "crop_relevance": ["rice", "wheat"]
        },
        {
            "trait": "waxy leaf coating",
            "stress": ["drought"],
            "mechanism": "reduces water loss",
            "crop_relevance": ["wheat"]
        },
        {
            "trait": "salt tolerance",
            "stress": ["salinity"],
            "mechanism": "maintains ion balance",
            "crop_relevance": ["rice"]
        },
        {
            "trait": "cold tolerance proteins",
            "stress": ["cold"],
            "mechanism": "prevents cell damage at low temperature",
            "crop_relevance": ["wheat"]
        }
    ]

    # ✅ CREATE COLLECTION
    collection = client.get_or_create_collection(name="traits")

    # ✅ CLEAR OLD DATA (IMPORTANT)
    try:
        collection.delete(where={})
    except:
        pass

    # ✅ ADD DATA
    for i, item in enumerate(traits_data):
        embedding = model.encode(item["trait"]).tolist()

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[item["trait"]],
            metadatas=[{
                "stress": item["stress"],
                "mechanism": item["mechanism"],
                "crop": item["crop_relevance"]
            }]
        )

    print("✅ Traits DB Loaded")

    # Clear old data (important during dev)
    try:
        client.delete_collection("traits")
    except:
        pass

    collection = client.get_or_create_collection(name="traits")

    for i, item in enumerate(traits_data):
        embedding = model.encode(item["trait"]).tolist()

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[item["trait"]],
            metadatas=[{
                "stress": item["stress"],
                "mechanism": item["mechanism"],
                "crop": item["crop_relevance"]
            }]
        )


# --------------------------
# SEARCH FUNCTION
# --------------------------
def search_traits(query: str, crop=None, stress=None, top_k=5):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    traits = results["documents"][0]
    metadatas = results["metadatas"][0]

    final_results = []

    for i in range(len(traits)):
        meta = metadatas[i]

        score = 0

        # match stress
        if stress:
            for s in stress:
                if s in meta.get("stress", []):
                    score += 2   # higher weight

        # match crop
        if crop and crop.lower() in [c.lower() for c in meta.get("crop", [])]:
            score += 1

        if score > 0:
            final_results.append({
                "trait": traits[i],
                "mechanism": meta.get("mechanism", ""),
                "score": score
            })

    # fallback
    if not final_results:
        final_results = [
            {"trait": t, "mechanism": "", "score": 0.5}
            for t in traits
        ]

    # sort by score
    final_results.sort(key=lambda x: x["score"], reverse=True)

    return final_results

    # Add simple ranking score (placeholder)
    return [
        {"trait": trait, "score": 1.0 - (i * 0.1)}
        for i, trait in enumerate(traits)
    ]