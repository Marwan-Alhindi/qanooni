-- 1) enable pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- 2) articles table: one row per article
CREATE TABLE public.articles (
  article_number   INTEGER      PRIMARY KEY,
  article_text     TEXT         NOT NULL,
  embedding        VECTOR(1536) NOT NULL
);

-- fast vector search on articles
CREATE INDEX ON public.articles
  USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- 3) clauses table: one row per clause
CREATE TABLE public.clauses (
  article_number   INTEGER      NOT NULL
    REFERENCES public.articles(article_number),
  clause_index     INTEGER      NOT NULL,
  clause_text      TEXT         NOT NULL,
  embedding        VECTOR(1536) NOT NULL,
  PRIMARY KEY     (article_number, clause_index)
);

-- fast vector search on clauses
CREATE INDEX ON public.clauses
  USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);