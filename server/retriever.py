import os
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore

# ── Load env ───────────────────────────────────
load_dotenv()

# ── Supabase client ────────────────────────────
def get_supabase_client() -> Client:
    return create_client(
        os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
        os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
    )

supabase = get_supabase_client()

# ── Embedding model ────────────────────────────
emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# ── Vector store & retriever ───────────────────
vectorstore = SupabaseVectorStore(
    client=supabase,
    table_name="articles",
    query_name="match_articles",
    embedding=emb,
    # no extra select_columns needed—your RPC only returns `content`
)
retriever = vectorstore.as_retriever()


async def retrieve_relevant_laws(query: str, top_k: int = 5) -> list[dict]:
    """
    Return a list of dicts {"title":..., "content":...}
    so that conversation_handler can do l['title'], l['content'].
    """
    docs = await retriever.aget_relevant_documents(query, k=top_k)
    return [
        {
            "title":   f"Article { d.metadata.get('article_number', idx+1) }",
            "content": d.page_content or ""
        }
        for idx, d in enumerate(docs)
    ]