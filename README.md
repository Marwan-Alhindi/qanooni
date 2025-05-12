# Qanooni – Legal Assistant Chatbot

Qanooni is a Streamlit-based legal assistant chatbot designed to help users navigate and query the Saudi Labor Law ("نظام العمل"). It leverages a document ingestion pipeline, a retrieval engine, and a user-friendly chat interface to deliver accurate, context-aware answers.

---

## 🧩 Problem & Solution

### The Problem
Accessing and understanding the Saudi Labor Law is difficult — especially for individuals — due to complex language, scattered sources, and lack of accessible legal tools.

### Our Solution
**Qanooni** simplifies legal access by offering:
- Natural-language Q&A grounded in official law
- Smart retrieval using semantic search
- Clear references to specific articles
- Easy access through a user-friendly chat interface
- A focused scope on Saudi Labor Law for high accuracy

---

## 🚀 Features

- **Intuitive Chat Interface:** Natural-language Q\&A over Labor Law chapters and articles.
- **Document Ingestion:** Scripts to parse and load articles & clauses into the knowledge base.
- **Retrieval Engine:** Fast search and retrieval of relevant legal provisions.
- **Modular Structure:** Clear separation between client UI, data processing, and backend logic.


---

## 🧠 Why Qanooni?

Qanooni isn’t just another legal chatbot — it’s built with precision and depth in mind:

1. **Direct Legal References:** All responses are grounded in the official Saudi Labor Law, with clear referencing to the specific article or clause.
2. **Intelligent Retrieval:** We use **cosine similarity** over semantic embeddings to retrieve the most relevant law text, ensuring contextual accuracy.
3. **Legal Reasoning:** The system draws logical links between user queries and legal provisions, enabling more insightful responses beyond keyword matching.
4. **Focused Domain Expertise:** By specializing only in **Saudi Labor Law**, we ensure deep, high-fidelity answers — unlike general legal bots that risk ambiguity across multiple fields.


---

## 🛠️ Prerequisites

- **Python 3.9+** installed on your machine
- **pip** for package management
- (Optional) A virtual environment tool such as venv or conda

---

## ⚡ Installation

1. **Clone the repository**

   
bash
   git clone https://github.com/your-org/qanooni.git
   cd qanooni


2. **Install dependencies**

   
bash
   pip install -r requirements.txt


3. **Environment variables**

   - Create a .env file in the root (or in env/) with any required keys, for example:

     
dotenv
     OPENAI_API_KEY=your_openai_api_key
     MONGO_URI=your_mongodb_connection_string


---

## 📂 Project Structure

plaintext
qanooni/
├── client/                  # Streamlit front-end application
│   ├── app.py               # Main entry point for the web app
│   ├── pages/               # Additional Streamlit pages
│   │   └── chat_app.py      # Chat interface page
│   ├── components/          # Reusable UI components (buttons, cards, etc.)
│   └── .gitignore           # Ignore rules for the client folder
│
├── server/                  # (Optional) Back-end APIs or microservices
│   └── ...                  # (Provide details if applicable)
│
├── data/                    # Data ingestion & retrieval logic
│   ├── ingest_articles.py   # Script to parse and load articles into DB
│   ├── ingest_clauses.py    # Script to parse and load clauses into DB
│   ├── laws.py              # Loader for raw law documents
│   ├── retriever.py         # Search and retrieval engine implementation
│   ├── conversation_handler.py  # Orchestrates Q&A pipeline
│   └── sql.sql              # Database schema (if using SQL storage)
│
├── styles/                  # Static assets & styling
│   ├── logo.png             # Project logo shown in the header
│   └── .gitignore
│
├── env/                     # Environment file templates / examples
│   └── .env.example         # Example environment variables
│
├── requirements.txt         # Python dependencies
└── README.md                # This documentation file


---

## ▶️ Usage

### 1. Run the Streamlit App

From the project root, execute:

bash
streamlit run client/app.py


This will launch the web UI at http://localhost:8501 by default. Use the sidebar or top navigation to switch between pages (e.g., the chat interface chat_app.py).

### 2. Data Ingestion

If you update the source PDFs or raw law files, re-run the ingestion scripts:

bash
python data/ingest_articles.py
python data/ingest_clauses.py


This populates or refreshes your database with the latest content.

### 3. Customization

- **Environment Variables:** Adjust keys in your .env file.
- **UI Components:** Modify or extend in client/components/.
- **Retrieval Logic:** Tweak search settings in data/retriever.py.

---

## 📖 Manual Structure

The Labor Law document follows a structured, book-like format:

1. **Articles** (مادة)
   Numbered entries within each chapter. Each Article has:

   - A **title**
   - The **full text** of the provision

2. **Clauses**
   Sub-points inside an Article, labeled (a), (b), (c), … to break down complex rules.

3. **Appendices**
   Supplementary tables or definitions (e.g., salary scales, leave entitlements) that some Articles reference.

When you reference or quote the law in your README or other docs, use these headings and numbering conventions to match the official structure.

---

# 🔍 Supabase Embeddings & Retrieval Overview

Supabase provides a PostgreSQL-based stack with support for **vector embeddings**, search, and retrieval using the `pgvector` extension. This allows developers to build semantic search systems using their own embedding models and integrate it directly with the database.

---

## 🧠 How Supabase Handles Embeddings

### 1. **Embedding Generation**
- Supabase does **not** generate embeddings itself — you need to use external models such as:
  - OpenAI (`text-embedding-ada-002`)
  - Hugging Face Transformers
  - Cohere, etc.

You run embedding generation *client-side* or in your server, and then store the resulting vectors in a `vector` column in PostgreSQL.

### 2. **Storing in PostgreSQL (with `pgvector`)**
- Supabase enables the `pgvector` extension, which allows storing and querying high-dimensional vectors.
- You define a column of type `vector(1536)` (e.g., for OpenAI embeddings).
  
Example:
```sql
CREATE TABLE law_articles (
  id serial PRIMARY KEY,
  title text,
  content text,
  embedding vector(1536)
);
```

## 📝 Contributing

Contributions are welcome! Please open issues or pull requests for any bugs, feature requests, or improvements. Follow the standard GitHub workflow:

1. Fork the repository
2. Create a feature branch (git checkout -b feature/YourFeature)
3. Commit your changes (git commit -m "Add some feature")
4. Push to your branch (git push origin feature/YourFeature)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

> _Questions? Feel free to ask for any additional files or clarifications!_
