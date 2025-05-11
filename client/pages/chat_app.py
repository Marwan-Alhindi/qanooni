import os
import sys
import asyncio
import time
import streamlit as st
from PIL import Image

# 0) Lock in the multipage query param so we never jump away
st.query_params["page"] = "chat_app"

# 1) Ensure project root is on the path
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from server.conversation_handler import progress_conversation

# 2) Load logo for header & favicon
logo_path = os.path.join(ROOT, "logo.png")
logo_img = Image.open(logo_path) if os.path.exists(logo_path) else None

# 3) Page config (will only apply once)
st.set_page_config(
    page_title="Qanooni Legal Assistant",
    page_icon=logo_img,
    layout="wide",
)

# 4) Header: logo + title
col_logo, col_title = st.columns([1, 9], gap="small")
with col_logo:
    if logo_img:
        st.image(logo_img, width=800)
with col_title:
    st.markdown(
        """
        <div style="padding-left:8px;">
          <h1 style="margin:0; line-height:1.2;">Qanooni Legal Assistant</h1>
          <hr style="border-color:#444; width:60%;">
        </div>
        """,
        unsafe_allow_html=True,
    )

# 5) Rerun helper (new + old Streamlit)
def rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        from streamlit.runtime.scriptrunner import RerunData, RerunException
        raise RerunException(RerunData())

# 6) Initialize chat state
if "history" not in st.session_state:
    st.session_state.history = []
if "show_recs" not in st.session_state:
    st.session_state.show_recs = True
if "rec_selected" not in st.session_state:
    st.session_state.rec_selected = False


# 7) Show recommended prompts on first load
recommendations = [
    "When can I deserve a vacation?",
    "What are my leave entitlements?",
    "How do I file a grievance?",
    "Explain company remote-work policy"
]
if st.session_state.show_recs:
    st.subheader("💡 Try one of these questions:")
    _, col_l, col_r, _ = st.columns([1, 2, 2, 1], gap="small")
    for idx, q in enumerate(recommendations):
        col = col_l if idx % 2 == 0 else col_r
        if col.button(q, key=f"rec_{idx}", use_container_width=True):
            # Append the question to the history
            st.session_state.history.append({"role": "user", "content": q})
            # Hide recommendations and set the selected flag
            st.session_state.show_recs = False
            st.session_state.rec_selected = True

# 8) Render chat history
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# 9) Typing effect
def typewriter(text: str):
    placeholder = st.empty()
    out = ""
    for word in text.split():
        out += word + " "
        placeholder.write(out)
        time.sleep(0.03)

# 10) Render assistant reply + optional link-button
def display_assistant_reply(reply):
    """
    reply can be:
      - str
      - dict with: content (str), link_url (str), optional link_text (str)
    """
    st.chat_message("assistant")
    if isinstance(reply, dict):
        typewriter(reply["content"])
        url = reply.get("link_url")
        label = reply.get("link_text", "Open link")
        if url:
            st.markdown(
                f"""
                <div style="margin-top:1rem;">
                  <a href="{url}" target="_blank" style="text-decoration:none;">
                    <button style="
                      padding:0.5rem 1rem;
                      background-color:#0078d4;
                      color:white;
                      border:none;
                      border-radius:0.25rem;
                      cursor:pointer;
                      text-align: right;

                    ">
                      🔗 {label}
                    </button>
                  </a>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        typewriter(reply)
# 11) If a recommended question was clicked
if st.session_state.rec_selected:
    question = st.session_state.history[-1]["content"]
    with st.chat_message("assistant"):
        placeholder = st.empty()  # Create a placeholder
        placeholder.write("⏳ Thinking…")  # Display the "Thinking..." message
        reply = asyncio.run(progress_conversation(question))
        placeholder.empty()  # Clear the placeholder

        # Use the typewriter effect to display the response word by word
        response_text = ""  # Initialize an empty string to build the response
        for word in (reply["content"] if isinstance(reply, dict) else reply).split():
            response_text += word + " "  # Append the next word
            placeholder.write(response_text)  # Update the placeholder with the new text
            time.sleep(0.1)  # Adjust the delay for typing effect

    st.session_state.history.append({
        "role": "assistant",
        "content": (reply["content"] if isinstance(reply, dict) else reply)
    })
    st.session_state.rec_selected = False

# 12) Otherwise handle new user input
elif prompt := st.chat_input("Type your legal question…"):
    st.session_state.history.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()  # Create a placeholder
        placeholder.write("⏳ Thinking…")  # Display the "Thinking..." message
        time.sleep(0)  # Wait for 3 seconds
        reply = asyncio.run(progress_conversation(prompt))
        placeholder.empty()  # Clear the placeholder

        # Use the typewriter effect to display the response word by word
        response_text = ""  # Initialize an empty string to build the response
        for word in (reply["content"] if isinstance(reply, dict) else reply).split():
            response_text += word + " "  # Append the next word
            placeholder.write(response_text)  # Update the placeholder with the new text
            time.sleep(0.01)  # Adjust the delay for typing effect

    st.session_state.history.append({
        "role": "assistant",
        "content": (reply["content"] if isinstance(reply, dict) else reply)
    })

# 13) Sidebar control to clear
with st.sidebar:
    st.header("Controls")
    if st.button("🗑️ Clear conversation"):
        st.session_state.history = []
        st.session_state.show_recs = True
        st.session_state.rec_selected = False
        rerun()
