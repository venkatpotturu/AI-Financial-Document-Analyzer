from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

model = SentenceTransformer('BAAI/bge-small-en-v1.5')

def get_chunks(text, chunk_size=1000):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def store_in_faiss(chunks, embeddings):
    try:
        dim = embeddings.shape[1]
        index = faiss.IndexFlatL2(dim)
        index.add(embeddings.astype(np.float32))
        return index, chunks
    except Exception as e:
        raise RuntimeError(f"FAISS storage error: {str(e)}")