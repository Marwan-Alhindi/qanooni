# backend/main.py
import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import SupabaseVectorStore

load_dotenv()
app = FastAPI(title="Legal Assistant API")

def get_supabase_client() -> Client:
    return create_client(
        os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
        os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
    )

supabase = get_supabase_client()
emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))
vectorstore = SupabaseVectorStore(
    client=supabase,
    table_name="articles",
    query_name="match_articles",
    embedding=emb,
)
retriever = vectorstore.as_retriever()

class ContextRequest(BaseModel):
    question: str

class Law(BaseModel):
    title: str
    content: str
    url: str  # ✅ include the URL in the Pydantic model

class ContextResponse(BaseModel):
    system: str
    message: dict
    laws: list[Law]

@app.post("/context", response_model=ContextResponse)
async def context_endpoint(req: ContextRequest):
    try:
        # your extra “system” instruction in Arabic
        extra_system = "أنت مساعد قانوني متخصص. استخدم المعلومات التالية بدقة عند الإجابة."
        # an extra “user” message you want appended
        extra_message = {"role": "user", "content": "هذا سياق إضافي للاستعلام القانوني."}

        # retrieve top-5 laws
        docs = await retriever.aget_relevant_documents(req.question, k=5)
        laws = []
        for idx, d in enumerate(docs):
            article_number = d.metadata.get("article_number", idx + 1)
            title = f"Article {article_number}"
            url = f"https://nezams.com/نظام-العمل/#subject-{article_number}"
            laws.append({
                "title": title,
                "content": d.page_content or "",
                "url": url
            })
        return ContextResponse(
            system=extra_system,
            message=extra_message,
            laws=laws,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
from openai import AsyncOpenAI

openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.post("/finetuned")
async def call_finetuned_model(req: ContextRequest):
    try:
        # 🧠 This calls your fine-tuned model
        response = await openai_client.chat.completions.create(
            model="ft:gpt-4o-2024-08-06:ganony::BWRC6EJW",  # your fine-tuned model ID
            messages=[
                {"role": "system", "content": "أنت مساعد قانوني متخصص."},
                {"role": "user", "content": req.question}
            ],
            # temperature=0.3,
        )
        return {
            "answer": response.choices[0].message.content
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))