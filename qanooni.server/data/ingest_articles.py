# ingest.py

import os
from dotenv import load_dotenv
from supabase import create_client
# switch to the new OpenAIEmbeddings import
from langchain_community.embeddings import OpenAIEmbeddings
from laws import laws

load_dotenv()  # loads .env into os.environ

# — Supabase client —
supabase = create_client(
    os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
    os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
)

# — Embedding model —
emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# — Prepare payloads —
article_rows = []
clause_rows  = []

for law in laws:
    n = law["article_number"]

    # 1) normalize & join article_text into one string
    art = law["article_text"]
    if isinstance(art, list):
        full_text = "\n".join(art)
    else:
        full_text = art

    # 2) embed full article
    art_vec = emb.embed_documents([full_text])[0]
    article_rows.append({
        "article_number": n,
        "article_text":   full_text,
        "embedding":      art_vec,
    })

    # 3) embed each clause
    for idx, clause in enumerate(law.get("clauses", [])):
        clause_vec = emb.embed_documents([clause])[0]
        clause_rows.append({
            "article_number": n,
            "clause_index":   idx,
            "clause_text":    clause,
            "embedding":      clause_vec,
        })

# — Insert into `articles` —
resp1 = supabase.table("articles").insert(article_rows).execute()
if resp1.error:
    print("❌ articles insert error:", resp1.error)
else:
    print(f"✅ inserted {len(article_rows)} articles")

# — Insert into `clauses` —
resp2 = supabase.table("clauses").insert(clause_rows).execute()
if resp2.error:
    print("❌ clauses insert error:", resp2.error)
else:
    print(f"✅ inserted {len(clause_rows)} clauses")