import os
from chromadb import PersistentClient # type: ignore
from sentence_transformers import SentenceTransformer # type: ignore
from Backend.Rag_Pipeline.embed import load_data # type: ignore

# =========================
# 🔹 PATH SETUP
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "Rag_Pipeline", "chroma_db")

# =========================
# 🔹 CHROMA CLIENT (FINAL)
# =========================
client = PersistentClient(path=DB_PATH)

# =========================
# 🔹 COLLECTION
# =========================
collection = client.get_or_create_collection(name="ecommerce")

# =========================
# 🔹 EMBEDDING MODEL
# =========================
model = SentenceTransformer("all-MiniLM-L6-v2")


# =========================
# 🔹 BUILD INDEX (RUN ONCE)
# =========================
def build_index():
    docs = load_data()

    print(f"Building ChromaDB for {len(docs)} documents...")

    # 🔁 Reset collection (important for clean runs)
    try:
        client.delete_collection("ecommerce")
    except:
        pass

    global collection
    collection = client.get_or_create_collection(name="ecommerce")

    for i, doc in enumerate(docs):
        embedding = model.encode(doc).tolist()

        collection.add(
            documents=[doc],
            embeddings=[embedding],
            ids=[f"id_{i}"]
        )

    print("✅ ChromaDB persisted at:", DB_PATH)


# =========================
# 🔹 SEARCH
# =========================
def search(query, top_k=3):
    query_embedding = model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results["documents"][0]


# =========================
# 🔹 MAIN
# =========================
if __name__ == "__main__":
    build_index()