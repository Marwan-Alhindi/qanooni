# retriever.py
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore

# Load environment variables
load_dotenv()

# Initialize Supabase client
def get_supabase_client() -> Client:
    url = os.getenv("NEXT_PUBLIC_SUPABASE_URL")
    key = os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY")
    return create_client(url, key)

supabase = get_supabase_client()

# Initialize embedding model
embedding_model = OpenAIEmbeddings(openai_api_key=os.getenv("NEXT_PUBLIC_OPENAI_API_KEY"))

# Create vector store and retriever
vectorstore = SupabaseVectorStore(
    client=supabase,
    table_name="laws",        # table with legal documents
    query_name="match_laws",  # RPC for cosine similarity
    embedding=embedding_model,
)
retriever = vectorstore.as_retriever()

async def retrieve_relevant_laws(
    query: str,
    user_id: str,
    top_k: int = 5
) -> list[dict]:
    """
    Retrieve up to top_k relevant laws for a given user query.
    Filters results by user_id metadata.
    Returns list of dicts with title and content.
    """
    docs = await retriever.aget_relevant_documents(query, k=top_k)
    # Filter by metadata.user_id
    user_docs = [
        {"title": d.metadata.get("title"), "content": d.page_content}
        for d in docs
        if d.metadata.get("user_id") == user_id
    ]
    return user_docs
