# import os
# from fastapi import FastAPI, HTTPException
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from supabase import create_client, Client
# from langchain.embeddings.openai import OpenAIEmbeddings
# from langchain.vectorstores import SupabaseVectorStore
# from langchain.chat_models import ChatOpenAI
# from langchain.prompts import PromptTemplate
# from langchain.chains import LLMChain

# # ── Load environment variables ─────────────────────────────
# load_dotenv()

# # ── Initialize FastAPI app ─────────────────────────────────
# app = FastAPI(title="Legal Assistant API")

# # ── Supabase client & retriever setup ───────────────────────

# def get_supabase_client() -> Client:
#     return create_client(
#         os.getenv("NEXT_PUBLIC_SUPABASE_URL"),
#         os.getenv("NEXT_PUBLIC_SUPABASE_ANON_KEY"),
#     )

# supabase = get_supabase_client()
# emb = OpenAIEmbeddings(openai_api_key=os.getenv("OPENAI_API_KEY"))

# vectorstore = SupabaseVectorStore(
#     client=supabase,
#     table_name="articles",
#     query_name="match_articles",
#     embedding=emb,
# )
# retriever = vectorstore.as_retriever()

# async def retrieve_relevant_laws(query: str, top_k: int = 5) -> list[dict]:
#     docs = await retriever.aget_relevant_documents(query, k=top_k)
#     return [
#         {
#             "title": f"Article {d.metadata.get('article_number', idx+1)}",
#             "content": d.page_content or ""
#         }
#         for idx, d in enumerate(docs)
#     ]

# # ── LLM initialization ─────────────────────────────────────
# llm = ChatOpenAI(
#     openai_api_key=os.getenv("OPENAI_API_KEY"),
#     model_name="gpt-4o"
# )

# # ── Prompt templates & chains ──────────────────────────────
# standalone_template = """
# بالنظر إلى تاريخ المحادثة (إن وجد) والسؤال المطروح، أعد صياغة السؤال بحيث يكون مفهوماً ومستقلاً بذاته.
# تاريخ المحادثة:
# {conv_history}
# السؤال:
# {question}
# السؤال المستقل:
# """
# standalone_prompt = PromptTemplate(
#     template=standalone_template,
#     input_variables=["conv_history", "question"]
# )
# standalone_chain = LLMChain(
#     llm=llm,
#     prompt=standalone_prompt,
#     output_key="standalone_question"
# )

# answer_template = """
# أنت مساعد قانوني مفيد. بناءً على السياق القانوني المقدم، أجب على سؤال المستخدم.
# السياق:
# {context}
# تاريخ المحادثة:
# {conv_history}
# السؤال:
# {question}
# الإجابة:
# """
# answer_prompt = PromptTemplate(
#     template=answer_template,
#     input_variables=["context", "conv_history", "question"]
# )
# answer_chain = LLMChain(
#     llm=llm,
#     prompt=answer_prompt,
#     output_key="answer"
# )

# # ── Conversation memory (in-memory) ─────────────────────────
# conv_history: list[str] = []

# async def progress_conversation(question: str, top_k: int = 5) -> str:
#     # Combine conversation history
#     formatted_history = "\n".join(conv_history)

#     # Standalone question
#     standalone_q = await standalone_chain.arun(
#         question=question,
#         conv_history=formatted_history
#     )

#     # Retrieve relevant laws
#     laws = await retrieve_relevant_laws(standalone_q, top_k=top_k)

#     # Generate answer or fallback
#     if laws:
#         ctx = "\n\n".join(f"{l['title']}: {l['content']}" for l in laws)
#         response = await answer_chain.arun(
#             context=ctx,
#             conv_history=formatted_history,
#             question=question
#         )
#     else:
#         response = "عذراً، لم أتمكن من العثور على قوانين ذات صلة."

#     # Update conversation history
#     conv_history.append(f"المستخدم: {question}")
#     conv_history.append(f"المساعد: {response}")

#     return response

# # ── Pydantic models ─────────────────────────────────────────
# class ChatRequest(BaseModel):
#     question: str

# class ChatResponse(BaseModel):
#     answer: str

# # ── API endpoints ───────────────────────────────────────────
# @app.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(req: ChatRequest):
#     try:
#         answer = await progress_conversation(req.question)
#         return ChatResponse(answer=answer)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))
    
# class ContextResponse(BaseModel):
#     system: str
#     message: dict  # e.g. {"role": "user", "content": "…"} or however you want to format

# @app.get("/context", response_model=ContextResponse)
# async def get_context():
#     # 1) Fetch or compute whatever context you need here
#     extra_system = "هذا نص النظام الإضافي من Context API."
#     extra_message = {
#         "role": "user",
#         "content": "هذا هو النص الإضافي المرسَل من Context API."
#     }
#     return ContextResponse(system=extra_system, message=extra_message)


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
        laws = [
            {
                "title": f"Article {d.metadata.get('article_number', idx+1)}",
                "content": d.page_content or "",
            }
            for idx, d in enumerate(docs)
        ]

        return ContextResponse(
            system=extra_system,
            message=extra_message,
            laws=laws,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))