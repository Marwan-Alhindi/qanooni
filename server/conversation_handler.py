# conversation_handler.py

import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from retriever import retrieve_relevant_laws

# Load environment variables
load_dotenv()

# Initialize LLM
openai_key = os.getenv("NEXT_PUBLIC_OPENAI_API_KEY")
llm = ChatOpenAI(openai_api_key=openai_key, model_name="gpt-4o")

# Prompt templates
standalone_template = '''
Given the conversation history (if any) and a question, rewrite the question as a standalone question.
conversation history: {conv_history}
question: {question}
standalone question:
'''
standalone_prompt = PromptTemplate(
    template=standalone_template,
    input_variables=["conv_history", "question"]
)
standalone_chain = LLMChain(
    llm=llm,
    prompt=standalone_prompt,
    output_key="standalone_question"
)

answer_template = '''
You are a helpful legal assistant. Based on the provided legal context, answer the user's question.
context: {context}
conversation history: {conv_history}
question: {question}
answer:
'''
answer_prompt = PromptTemplate(
    template=answer_template,
    input_variables=["context", "conv_history", "question"]
)
answer_chain = LLMChain(
    llm=llm,
    prompt=answer_prompt,
    output_key="answer"
)

# In-memory conversation history
conv_history: list[str] = []

async def progress_conversation(question: str, user_id: str) -> str:
    """
    Handle a user question: rewrite it standalone, retrieve relevant laws, and answer.
    """
    # 1) Format history
    formatted_history = "\n".join(conv_history)

    # 2) Generate standalone question
    standalone_q = await standalone_chain.arun(
        question=question,
        conv_history=formatted_history
    )

    # 3) Retrieve relevant laws
    laws = await retrieve_relevant_laws(standalone_q, user_id)
    if not laws:
        response = "No relevant laws found for your query."
    else:
        # Build context from retrieved laws
        context = "\n\n".join([f"{law['title']}: {law['content']}" for law in laws])
        # 4) Generate final answer
        response = await answer_chain.arun(
            context=context,
            conv_history=formatted_history,
            question=question
        )

    # 5) Update history
    conv_history.append(question)
    conv_history.append(response)

    return response