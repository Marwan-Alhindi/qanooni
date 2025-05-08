# app.py
import streamlit as st
import asyncio

from retriever import retrieve_relevant_laws

st.set_page_config(page_title="Law Retrieval Tester")
st.title("📚 Law Retrieval")

# — Inputs —
user_id = st.text_input("User ID", value="user123")
query   = st.text_input("Enter your legal query", "")

if st.button("🔍 Retrieve Laws"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Fetching…"):
            # call your async function
            docs = asyncio.run(retrieve_relevant_laws(query, user_id, top_k=5))
            if docs:
                for i, doc in enumerate(docs, start=1):
                    st.subheader(f"{i}. {doc['title']}")
                    st.write(doc["content"])
            else:
                st.info("No matching laws found for that user.")