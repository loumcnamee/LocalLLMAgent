"""
Example 03 — Retrieval-Augmented Generation (RAG) with ChromaDB
----------------------------------------------------------------
Demonstrates a simple local RAG pipeline:
  1. Embed documents using a local Ollama embedding model.
  2. Store embeddings in a persistent ChromaDB collection.
  3. At query time, retrieve the most relevant chunks and pass them
     to the LLM as context.

Prerequisites:
    ollama serve
    ollama pull llama3.2:3b
    ollama pull nomic-embed-text

Run:
    python examples/03_rag_chromadb.py
"""

import os
import chromadb
import ollama
from chromadb.config import Settings


# ── Configuration ──────────────────────────────────────────────────────────────
LLM_MODEL = "llama3.2:3b"
EMBED_MODEL = "nomic-embed-text"
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
COLLECTION_NAME = "local_llm_docs"
N_RESULTS = 3

# ── Sample documents to index ──────────────────────────────────────────────────
DOCUMENTS = [
    {
        "id": "doc1",
        "text": (
            "Ollama is an open-source tool that lets you run large language models "
            "locally on your own hardware. It manages model downloads, quantisation, "
            "and exposes both a native REST API and an OpenAI-compatible /v1 endpoint."
        ),
    },
    {
        "id": "doc2",
        "text": (
            "The NVIDIA Quadro P620 is a Pascal-architecture GPU with 2 GB GDDR5 VRAM. "
            "Because its VRAM is limited, most LLM inference runs on the CPU/RAM. "
            "Partial GPU offloading (a few transformer layers) is possible via llama.cpp."
        ),
    },
    {
        "id": "doc3",
        "text": (
            "Retrieval-Augmented Generation (RAG) is a technique that enhances LLM "
            "responses by first retrieving relevant documents from a knowledge base "
            "and injecting them into the prompt as context."
        ),
    },
    {
        "id": "doc4",
        "text": (
            "ChromaDB is an open-source, embeddable vector database. It can be run "
            "in-process (no server needed) and persists data to disk. It is commonly "
            "used for RAG pipelines in Python applications."
        ),
    },
    {
        "id": "doc5",
        "text": (
            "Quantisation reduces model size and memory usage by representing weights "
            "at lower precision (e.g. 4-bit instead of 16-bit). GGUF is the format used "
            "by llama.cpp and Ollama for quantised models."
        ),
    },
]


# ── Embedding helper ──────────────────────────────────────────────────────────
def embed(text: str) -> list[float]:
    """Embed text using the local Ollama embedding model."""
    response = ollama.embeddings(model=EMBED_MODEL, prompt=text)
    return response.embedding


# ── Build / load vector store ─────────────────────────────────────────────────
def get_or_build_collection() -> chromadb.Collection:
    os.makedirs(DB_PATH, exist_ok=True)
    client = chromadb.PersistentClient(
        path=DB_PATH,
        settings=Settings(anonymized_telemetry=False),
    )

    existing = [c.name for c in client.list_collections()]
    if COLLECTION_NAME in existing:
        print(f"Loading existing collection '{COLLECTION_NAME}' …")
        return client.get_collection(COLLECTION_NAME)

    print(f"Building collection '{COLLECTION_NAME}' …")
    collection = client.create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    embeddings = [embed(doc["text"]) for doc in DOCUMENTS]
    collection.add(
        ids=[doc["id"] for doc in DOCUMENTS],
        embeddings=embeddings,
        documents=[doc["text"] for doc in DOCUMENTS],
    )
    print(f"  Indexed {len(DOCUMENTS)} documents.")
    return collection


# ── RAG query ─────────────────────────────────────────────────────────────────
def rag_query(question: str, collection: chromadb.Collection) -> str:
    """Retrieve relevant chunks, then answer the question with the LLM."""
    query_embedding = embed(question)
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=N_RESULTS,
        include=["documents", "distances"],
    )

    retrieved_chunks = results["documents"][0]
    context = "\n\n".join(
        f"[Chunk {i+1}]\n{chunk}" for i, chunk in enumerate(retrieved_chunks)
    )

    system_prompt = (
        "You are a helpful assistant. Answer the user's question using ONLY "
        "the provided context. If the context does not contain enough information, "
        "say so rather than guessing."
    )
    user_prompt = f"Context:\n{context}\n\nQuestion: {question}"

    response = ollama.chat(
        model=LLM_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return response.message.content


# ── Main ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    collection = get_or_build_collection()

    questions = [
        "What is Ollama and what APIs does it expose?",
        "Why does most LLM inference run on CPU for the Quadro P620?",
        "What file format does Ollama use for quantised models?",
    ]

    for q in questions:
        print(f"\nQ: {q}")
        answer = rag_query(q, collection)
        print(f"A: {answer}")
        print("-" * 60)
