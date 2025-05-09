# client/pages/chat_app.py
import os, sys
import asyncio
import time
import streamlit as st
from PIL import Image

# ─────────────────────────────────────────────────────────────────────────────
# 1) Compute project root so we can find logo.png & qanooni package
ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__),   "..")
)
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# 2) Load your logo (make sure logo.png lives in the project root)
logo_path = os.path.join(ROOT, "logo.png")
if not os.path.exists(logo_path):
    st.error(f"⚠️ logo.png not found at {logo_path}")
    logo_img = None
else:
    logo_img = Image.open(logo_path)

# 3) Now set page config *with* the logo as the tab icon
st.set_page_config(
    page_title="Qanooni Legal Assistant",
    page_icon=logo_img,        # ← uses your PNG as favicon
    layout="wide",
)

# ─────────────────────────────────────────────────────────────────────────────
# 4) Render header with two columns: logo on the left, title on the right
col_logo, col_title = st.columns([1, 9], gap="small")
with col_logo:
    if logo_img:
        st.image(logo_img, width=128)  # adjust size to your taste
with col_title:
    st.markdown(
        """
        <div style="padding-left:8px;">
          <h1 style="margin:0; line-height:1.2;">
            Qanooni Legal Assistant
          </h1>
          <hr style="border-color:#444; width:60%;">
        </div>
        """,
        unsafe_allow_html=True,
    )
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 4) Rerun helper for different Streamlit versions
def rerun():
    try:
        st.experimental_rerun()
    except AttributeError:
        from streamlit.runtime.scriptrunner import RerunData, RerunException
        raise RerunException(RerunData())
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 5) Initialize state for chat history and recommendations
if "history" not in st.session_state:
    st.session_state.history = []  # list of {role, content}
if "show_recs" not in st.session_state:
    st.session_state.show_recs = True
if "rec_selected" not in st.session_state:
    st.session_state.rec_selected = False
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 6) Recommended questions on first visit
recommendations = [
    "When can I deserve a vacation?",
    "What are my leave entitlements?",
    "How do I file a grievance?",
    "Explain company remote-work policy"
]
if st.session_state.show_recs:
    st.subheader("💡 Try one of these questions:")
    outer1, col_left, col_right, outer2 = st.columns([1, 2, 2, 1], gap="small")
    if col_left.button(recommendations[0], key="rec_0", use_container_width=True):
        st.session_state.history.append({"role": "user", "content": recommendations[0]})
        st.session_state.show_recs = False
        st.session_state.rec_selected = True
        rerun()
    if col_left.button(recommendations[2], key="rec_2", use_container_width=True):
        st.session_state.history.append({"role": "user", "content": recommendations[2]})
        st.session_state.show_recs = False
        st.session_state.rec_selected = True
        rerun()
    if col_right.button(recommendations[1], key="rec_1", use_container_width=True):
        st.session_state.history.append({"role": "user", "content": recommendations[1]})
        st.session_state.show_recs = False
        st.session_state.rec_selected = True
        rerun()
    if col_right.button(recommendations[3], key="rec_3", use_container_width=True):
        st.session_state.history.append({"role": "user", "content": recommendations[3]})
        st.session_state.show_recs = False
        st.session_state.rec_selected = True
        rerun()
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 7) Render the conversation so far
for msg in st.session_state.history:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 8) Typewriter effect helper
def typewriter(message_text):
    placeholder = st.empty()
    text = ""
    for word in message_text.split():
        text += word + " "
        placeholder.write(text)
        time.sleep(0.05)
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 9) Handle new prompts or selected recommendation
if st.session_state.rec_selected:
    question = st.session_state.history[-1]["content"]
    with st.chat_message("assistant"):
        st.write("⏳ Thinking…")
        reply = asyncio.run(progress_conversation(question))
        typewriter(reply)
        st.session_state.history.append({"role": "assistant", "content": reply})
    st.session_state.rec_selected = False

else:
    if prompt := st.chat_input("Type your legal question…"):
        st.session_state.history.append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        with st.chat_message("assistant"):
            st.write("⏳ Thinking…")
            reply = asyncio.run(progress_conversation(prompt))
            typewriter(reply)
            st.session_state.history.append({"role": "assistant", "content": reply})
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 10) Sidebar: clear history and reset
with st.sidebar:
    st.header("Controls")
    if st.button("🗑️ Clear conversation"):
        st.session_state.history = []
        st.session_state.show_recs = True
        st.session_state.rec_selected = False
        rerun()
# ─────────────────────────────────────────────────────────────────────────────
