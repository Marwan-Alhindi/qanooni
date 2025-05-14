# Qanooni – AI-Powered Legal Assistant

**Qanooni** is a multilingual, AI-powered legal assistant focused on retrieving accurate answers from Saudi legal documents — starting with **Labor Law** and expanding to other domains like civil, criminal, and personal law.

This system combines **Retrieval-Augmented Generation (RAG)** and **fine-tuned LLMs** to offer high-quality legal Q&A with specific references to law articles and clauses.

---

## Overview

Accessing legal information in Saudi Arabia can be challenging due to scattered sources, legal complexity, and the lack of accessible tools for the general public. Qanooni solves this by offering:

- **Natural language Q&A** over Saudi labor laws  
- **Semantic search** backed by embeddings  
- **Fine-tuned LLMs** for accurate, contextual replies  
- **Web interface** for ease of use  
- **Modular architecture** to easily expand to other legal domains

---

## How It Works

Qanooni uses a hybrid architecture combining:

1. **RAG Pipeline**: Retrieves the most relevant legal text using **Supabase pgvector** and **OpenAI embeddings**.
2. **LLM Response Generator**: Combines retrieved context with a fine-tuned LLM (OpenAI GPT) for precise legal reasoning.
3. **Frontend Interface**: Interactive chat powered by **Next.js (TypeScript + React)**.
4. **Backend Logic**: Managed via **FastAPI**, handling embedding generation, semantic search, and chat processing.

---

## Tech Stack

| Layer       | Tech Used                        |
|-------------|----------------------------------|
| Frontend    | Next.js, TypeScript, React       |
| Backend     | Python, FastAPI                  |
| Database    | Supabase (PostgreSQL + pgvector) |
| Embeddings  | OpenAI `text-embedding-ada-002`  |
| LLM         | OpenAI (fine-tuned GPT model)    |

---

## Directory Structure

```bash
capstone-project-batch3-qanooni/
├── client/         # Next.js frontend with chat UI
├── server/         # FastAPI backend with RAG logic
├── documents/      # Logos, assets, and legal reference files
└── README.md
```

## Installation & Setup
1. Clone the repository
git clone https://github.com/your-org/capstone-project-batch3-qanooni.git
cd capstone-project-batch3-qanooni

2. Frontend Setup (Next.js)
cd client

Create a .env file:
OPENAI_API_KEY=your_openai_key
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

Install dependencies and start the dev server:

npm install
npm run dev

Frontend will be available at: http://localhost:3000

3. Backend Setup (FastAPI)
Open a new terminal, then run:
cd server

Create a .env file inside the server folder:
OPENAI_API_KEY=your_openai_key
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

Set up your Python environment and install dependencies:
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

Run the FastAPI server:
uvicorn main:app --reload

The backend will run on: http://localhost:8000



