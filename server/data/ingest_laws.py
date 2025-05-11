import os
from dotenv import load_dotenv
from supabase import create_client
from langchain_community.embeddings import OpenAIEmbeddings
from laws import laws

load_dotenv()  # load .env into os.environ

# — Supabase client —
supabase = create_client(
    os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
    os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
)

# — Embedding model —
emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# — Prepare payloads (one row per article including clauses & related) —
rows = []
for law in laws:
    art_num = law.get("article_number")
    raw_text = law.get("article_text", "")
    clauses = law.get("clauses", [])
    related = law.get("related_articles", "").strip()

    # Normalize article text
    if isinstance(raw_text, list):
        art_text = "\n".join(raw_text)
    else:
        art_text = raw_text

    # Append clauses
    if clauses:
        art_text += "\n\n" + "\n".join(clauses)

    # Append related articles
    if related:
        art_text += "\n\n" + related

    # Embed the combined text
    vector = emb.embed_documents([art_text])[0]

    rows.append({
        "article_number": art_num,
        "article_text":   art_text,
        "embedding":      vector,
    })

# — Insert into `articles` —
resp = supabase.table("articles").insert(rows).execute()
if resp.error:
    print("❌ Insert error:", resp.error)
else:
    print(f"✅ Inserted {len(rows)} articles (with clauses & related)")
