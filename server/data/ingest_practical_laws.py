# ingest_practical.py

import os
from dotenv import load_dotenv
from supabase import create_client
from langchain_community.embeddings import OpenAIEmbeddings
from practical_laws import practical_laws

load_dotenv()  # load .env into os.environ

# — Supabase client —
supabase = create_client(
    os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
    os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
)

# — Embedding model —
emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# — Prepare payloads for `practical_laws` table —
practical_rows = []
for law in practical_laws:
    art_num = law.get("article_number")
    text = law.get("article_text", "")
    clauses = law.get("clauses", [])

    # Normalize article text
    if isinstance(text, list):
        art_text = "\n".join(text)
    else:
        art_text = text

    # Append clauses
    if clauses:
        art_text += "\n\n" + "\n".join(clauses)

    # Embed combined text
    vector = emb.embed_documents([art_text])[0]

    practical_rows.append({
        "article_number": art_num,
        "article_text":   art_text,
        "embedding":      vector,
    })

# — Insert into `practical_laws` —
resp2 = supabase.table("practical_laws").insert(practical_rows).execute()
if resp2.error:
    print("❌ Practical laws insert error:", resp2.error)
else:
    print(f"✅ Inserted {len(practical_rows)} practical laws")
