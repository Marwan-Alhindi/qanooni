# client/app.py

import os
import sys
import streamlit as st
from PIL import Image

# ─────────────────────────────────────────────────────────────────────────────
# 1) Ensure your project root is on the path
ROOT = os.path.abspath(os.path.join(__file__, "..", ".."))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 2) Load the logo
logo_path = os.path.join(ROOT, "logo.png")
if os.path.exists(logo_path):
    logo_img = Image.open(logo_path)
else:
    st.error(f"⚠️ logo.png not found at {logo_path}")
    logo_img = None
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 3) Centered header: only logo + "Qanooni"
col1, col2, col3 = st.columns([1, 12, 1], gap="medium")
with col2:
    logo_col, title_col = st.columns([2, 6], gap="small")
    with logo_col:
        if logo_img:
            st.image(logo_img, width=800)
    with title_col:
        st.markdown(
            "<h1 style='margin:0; padding-top:0.5rem;'>Qanooni</h1>",
            unsafe_allow_html=True,
        )
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 4) Main subtitle underneath
st.markdown("## Welcome to your Legal Assistant")
st.markdown("---")
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 5) Intro text
st.markdown(
    """
**Qanooni** brings you a set of streamlined legal-tech tools to:

1. **Quickly retrieve** the exact laws and articles you need.  
2. **Chat** in natural language to clarify, deep-dive, or get follow-ups.  

---

## 🚀 Our Projects

- **Law Retrieval**  
  Search by plain-English queries and instantly get the most relevant statutes and articles.

- **Legal Chatbot**  
  Click the button below to open our chat interface—your conversation will stay saved during this session!

---

### 🔍 How It Helps You

- **Time-saver:** No more sifting through volumes of text.  
- **On-demand guidance:** Get assistance 24/7.  
- **Better access:** Democratizes legal research for non-experts.

_We’re constantly adding features—document summarization, citation generation, and more!_
    """
)
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 6) HTML Button to jump to the Chat App page
st.markdown(
    """
<div style="text-align:center; margin:2rem 0;">
  <a href="chat_app" style="text-decoration:none;">
    <button style="
      padding: 0.75rem 1.5rem;
      font-size: 1rem;
      background-color: #0078d4;
      color: white;
      border: none;
      border-radius: 0.25rem;
      cursor: pointer;
    ">
      💬 Open Chat App
    </button>
  </a>
</div>
""",
    unsafe_allow_html=True,
)
# ─────────────────────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# 7) Sidebar hint
st.sidebar.success(
    "Use the top menu to navigate:\n"
    "- **Home** (this page)\n"
    "- **Chat App** (your chatbot)"
)
# ─────────────────────────────────────────────────────────────────────────────
