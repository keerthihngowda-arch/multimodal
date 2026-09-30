from Backend.Rag_Pipeline.index import search

def get_context(query):
    results = search(query, top_k=3)
    return "\n".join(results)