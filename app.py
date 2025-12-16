import numpy as np
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables first
load_dotenv()

import fitz
from file_extractor import get_text_from_file
from embedder import get_chunks, store_in_faiss
from chat_engine import retrieve_similar_chunks, generate_response
from sentence_transformers import SentenceTransformer

st.set_page_config(page_title="Chat with Your Files", layout="wide")
st.title("📄 Chat with Your File")

# Initialize session state
if 'history' not in st.session_state:
    st.session_state.history = []
if 'processed' not in st.session_state:
    st.session_state.processed = False

uploaded_file = st.file_uploader("Upload any document or image", 
                type=['pdf', 'docx', 'txt', 'xlsx', 'csv', 'png', 'jpg', 'jpeg'])

if uploaded_file and not st.session_state.processed:
    with st.spinner("Processing your file..."):
        try:
            text = get_text_from_file(uploaded_file)
            if not text:
                st.error("No text could be extracted from the file")
                st.session_state.processed = False
                st.stop()
                
            chunks = get_chunks(text)
            embedder = SentenceTransformer('BAAI/bge-small-en-v1.5')
            embeddings = embedder.encode(chunks)
            index, stored_chunks = store_in_faiss(chunks, np.array(embeddings))
            
            # Store in session state
            st.session_state.index = index
            st.session_state.stored_chunks = stored_chunks
            st.session_state.embedder = embedder
            st.session_state.processed = True
            
            st.success("📥 File processed successfully! Ready for questions.")
        except Exception as e:
            st.error(f"Processing failed: {str(e)}")
            st.session_state.processed = False

# Chat interface
if st.session_state.processed:
    query = st.chat_input("💬 Ask something about your file:")
    if query:
        st.session_state.history.append(("user", query))
        
        with st.spinner("Analyzing..."):
            try:
                top_chunks = retrieve_similar_chunks(
                    query, 
                    st.session_state.index, 
                    st.session_state.stored_chunks, 
                    st.session_state.embedder
                )
                context = "\n".join(top_chunks)
                
                # Include last 2 interactions for context
                if len(st.session_state.history) > 1:
                    context += f"\n\nPrevious conversation:\n" + "\n".join(
                        [f"{role}: {msg}" for role, msg in st.session_state.history[-2:]]
                    )
                
                response = generate_response(query, context)
                st.session_state.history.append(("assistant", response))
                
            except Exception as e:
                response = f"Error processing request: {str(e)}"
                st.session_state.history.append(("assistant", response))

        # Display conversation
        for role, msg in st.session_state.history:
            with st.chat_message(role):
                st.write(msg)