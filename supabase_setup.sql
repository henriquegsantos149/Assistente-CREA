-- =================================================================================
-- CONFIGURAÇÃO SUPABASE PARA O CRE.IA (BANCO DE DADOS VETORIAL)
-- =================================================================================

-- 1. Habilitar a extensão pgvector (Necessário para buscas semânticas)
create extension if not exists vector;

-- 2. Criar a tabela que guardará as partes dos seus documentos (chunks)
create table if not exists documentos_crea (
  id bigserial primary key,
  content text not null,       -- O pedaço de texto do documento (ex: um artigo da resolução)
  metadata jsonb,              -- Metadados (ex: {"arquivo": "resolucao1073.md"})
  embedding vector(384)        -- Vetor gerado pelo modelo (384 é o padrão do MiniLM-L6-v2)
);

-- 3. Criar um índice HNSW para que a busca seja ultra-rápida mesmo com milhares de documentos
create index on documentos_crea using hnsw (embedding vector_cosine_ops);

-- 4. Criar a Função RPC (Stored Procedure) que nosso Backend vai chamar para buscar respostas
create or replace function match_documentos_crea (
  query_embedding vector(384),
  match_threshold float,
  match_count int
)
returns table (
  id bigint,
  content text,
  metadata jsonb,
  similarity float
)
language sql stable
as $$
  select
    documentos_crea.id,
    documentos_crea.content,
    documentos_crea.metadata,
    1 - (documentos_crea.embedding <=> query_embedding) as similarity
  from documentos_crea
  where 1 - (documentos_crea.embedding <=> query_embedding) > match_threshold
  order by documentos_crea.embedding <=> query_embedding
  limit match_count;
$$;

-- =================================================================================
-- TABELAS PARA OUTROS AGENTES
-- =================================================================================

-- Agente INCRA
create table if not exists documentos_incra (
  id bigserial primary key,
  content text not null,
  metadata jsonb,
  embedding vector(384)
);

create index on documentos_incra using hnsw (embedding vector_cosine_ops);

create or replace function match_documentos_incra (
  query_embedding vector(384),
  match_threshold float,
  match_count int
)
returns table (id bigint, content text, metadata jsonb, similarity float)
language sql stable as $$
  select id, content, metadata, 1 - (embedding <=> query_embedding) as similarity
  from documentos_incra
  where 1 - (embedding <=> query_embedding) > match_threshold
  order by embedding <=> query_embedding
  limit match_count;
$$;

-- Agente ADM
create table if not exists documentos_adm (
  id bigserial primary key,
  content text not null,
  metadata jsonb,
  embedding vector(384)
);

create index on documentos_adm using hnsw (embedding vector_cosine_ops);

create or replace function match_documentos_adm (
  query_embedding vector(384),
  match_threshold float,
  match_count int
)
returns table (id bigint, content text, metadata jsonb, similarity float)
language sql stable as $$
  select id, content, metadata, 1 - (embedding <=> query_embedding) as similarity
  from documentos_adm
  where 1 - (embedding <=> query_embedding) > match_threshold
  order by embedding <=> query_embedding
  limit match_count;
$$;
