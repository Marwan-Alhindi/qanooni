# ingest_clauses.py

import os
from dotenv import load_dotenv
from supabase import create_client
from langchain_community.embeddings import OpenAIEmbeddings
from laws import laws

# load .env
load_dotenv()

# supabase client
supabase = create_client(
    os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
    os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
)

# embedding model
emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# prepare clause payloads
clause_rows = []
for law in laws:
    n = law["article_number"]
    for idx, clause in enumerate(law.get("clauses", [])):
        vec = emb.embed_documents([clause])[0]
        clause_rows.append({
            "article_number": n,
            "clause_index":   idx,
            "clause_text":    clause,
            "embedding":      vec
        })

# insert into clauses table
resp = supabase.table("clauses").insert(clause_rows).execute()
if resp.error:
    print("❌ Clauses insert error:", resp.error)
else:
    print(f"✅ Inserted {len(clause_rows)} clauses")