import os, sys, asyncio
import streamlit as st

# ── Make sure Python sees your `qanooni` package ──
ROOT = os.path.abspath(os.path.join(__file__, "..", ".."))
sys.path.insert(0, ROOT)

from qanooni.server.conversation_handler import progress_conversation

# ── Streamlit layout ─────────────────────────────
st.set_page_config(page_title="Legal Chatbot")
st.header("📚 Ask About Your Legal Rights")

if "chat" not in st.session_state:
    st.session_state.chat = []  # list of (speaker, text)

query = st.text_input("Your question…", key="input")
if st.button("Send"):
    if not query.strip():
        st.warning("Type something first!")
    else:
        # display user message immediately
        st.session_state.chat.append(("You", query))
        with st.spinner("Thinking…"):
            answer = asyncio.run(progress_conversation(query, top_k=5))
        st.session_state.chat.append(("Assistant", answer))

# Render the chat history
for speaker, text in st.session_state.chat:
    if speaker == "You":
        st.markdown(f"**You:** {text}")
    else:
        st.markdown(f"**Assistant:** {text}")