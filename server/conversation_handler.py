# conversation_handler.py
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from .retriever import retrieve_relevant_laws  # تأكد من مسار الاستيراد الصحيح

# ── تحميل مفاتيح البيئة وتهيئة الـ LLM ─────────────────
load_dotenv()
llm = ChatOpenAI(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    model_name="gpt-4o"
)

# ── سلسلة إعادة صياغة السؤال المستقل ────────────────────
standalone_template = """
بالنظر إلى تاريخ المحادثة (إن وجد) والسؤال المطروح، أعد صياغة السؤال بحيث يكون مفهوماً ومستقلاً بذاته.
تاريخ المحادثة:
{conv_history}
السؤال:
{question}
السؤال المستقل:
"""
standalone_prompt = PromptTemplate(
    template=standalone_template,
    input_variables=["conv_history", "question"]
)
standalone_chain = LLMChain(
    llm=llm,
    prompt=standalone_prompt,
    output_key="standalone_question"
)

# ── سلسلة توليد الإجابة النهائية ──────────────────────
answer_template = """
أنت مساعد قانوني مفيد. بناءً على السياق القانوني المقدم، أجب على سؤال المستخدم.
السياق:
{context}
تاريخ المحادثة:
{conv_history}
السؤال:
{question}
الإجابة:
"""
answer_prompt = PromptTemplate(
    template=answer_template,
    input_variables=["context", "conv_history", "question"]
)
answer_chain = LLMChain(
    llm=llm,
    prompt=answer_prompt,
    output_key="answer"
)

# ── تخزين تاريخ المحادثة في الذاكرة ───────────────────
conv_history: list[str] = []

async def progress_conversation(question: str, top_k: int = 5) -> str:
    """
    تعيد صياغة السؤال، تستدعي القوانين المتعلقة، ثم تولد الإجابة النهائية.
    """
    # 1) دمج تاريخ المحادثة
    formatted_history = "\n".join(conv_history)

    # 2) إعادة صياغة السؤال ليصبح مستقلاً
    standalone_q = await standalone_chain.arun(
        question=question,
        conv_history=formatted_history
    )

    # 3) جلب القوانين ذات الصلة
    laws = await retrieve_relevant_laws(standalone_q, top_k=top_k)

    # 4) بناء السياق والإجابة أو عرض رسالة عدم العثور
    if laws:
        # laws هي قائمة من dict بوجود 'title' و'content'
        ctx = "\n\n".join(f"{l['title']}: {l['content']}" for l in laws)
        response = await answer_chain.arun(
            context=ctx,
            conv_history=formatted_history,
            question=question
        )
    else:
        response = "عذراً، لم أتمكن من العثور على قوانين ذات صلة."

    # 5) تحديث تاريخ المحادثة
    conv_history.append(f"المستخدم: {question}")
    conv_history.append(f"المساعد: {response}")

    return response