# app.py

import os, sys, asyncio
import streamlit as st

ROOT = os.path.abspath(os.path.join(__file__, "..", ".."))
sys.path.insert(0, ROOT)

from qanooni.server.retriever import retrieve_relevant_laws

st.set_page_config(page_title="Law Retrieval Tester")
st.title("📚 Law Retrieval")

query = st.text_input("Enter your legal query", "")

if st.button("🔍 Retrieve Laws"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Fetching…"):
            articles = asyncio.run(retrieve_relevant_laws(query, top_k=5))
            if articles:
                for i, text in enumerate(articles, start=1):
                    st.subheader(f"{i}.")
                    st.write(text)
            else:
                st.info("No matching laws found.")