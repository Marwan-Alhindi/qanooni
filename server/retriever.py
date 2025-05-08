# retriever.py

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore

# Load .env
load_dotenv()

# Supabase client
def get_supabase_client() -> Client:
    return create_client(
        os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
        os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
    )

supabase = get_supabase_client()

# Embedding model
emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# Vector store pointed at your new, single-column RPC
vectorstore = SupabaseVectorStore(
    client=supabase,
    table_name="articles",         # still needed so LangChain knows where to apply vector ops
    query_name="match_articles",   # must match the RPC above
    embedding=emb,
    # no select_columns or metadata_columns needed
)
retriever = vectorstore.as_retriever()

async def retrieve_relevant_laws(query: str, top_k: int = 5) -> list[str]:
    """
    Returns the top_k raw article texts most similar to query.
    """
    docs = await retriever.aget_relevant_documents(query, k=top_k)
    # each `d.page_content` is one article_text from the RPC
    return [d.page_content for d in docs]