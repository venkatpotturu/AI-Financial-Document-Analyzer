from groq import Groq
import os
import numpy as np

def retrieve_similar_chunks(query, index, chunks, embedder):
    try:
        query_embedding = embedder.encode([query])
        D, I = index.search(np.array(query_embedding).astype(np.float32), k=5)
        return [chunks[i] for i in I[0] if i < len(chunks)]
    except Exception as e:
        raise RuntimeError(f"Retrieval error: {str(e)}")

# chat_engine.py - UPDATED
from groq import Groq
import os

def generate_response(query, context):
    try:
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        
        response = client.chat.completions.create(
            messages=[{
                "role": "system",
                "content": f"""Analyze this CONTEXT from document/image:
                {context}
                Answer ONLY using provided information"""
            },{
                "role": "user",
                "content": query
            }],
            model="llama3-70b-8192",  # Verified working model
            temperature=0.1,
            max_tokens=512
        )
        return response.choices[0].message.content
    except Exception as e:
        return "Unable to process request currently"