"""
Camada de abstração de banco de dados — CRE.IA
===============================================
Suporta dois backends configuráveis via variável de ambiente:

  DATABASE_BACKEND=sqlite    → SQLite local (padrão, zero configuração)
  DATABASE_BACKEND=supabase  → API REST do Supabase

Outras alternativas que podem ser adicionadas no futuro:
  - MongoDB (pymongo)
  - Firebase Firestore (google-cloud-firestore)
  - PostgreSQL direto (psycopg2 / asyncpg)
  - Neon (PostgreSQL serverless, similar ao Supabase sem o BaaS)
  - PlanetScale (MySQL serverless)

Configuração do SQLite:
  SQLITE_DB_PATH=/caminho/para/sessions.db  (opcional, padrão: data/sessions.db)

Configuração do Supabase:
  SUPABASE_URL=https://xxxx.supabase.co
  SUPABASE_KEY=sua-chave-aqui
"""
import os
import uuid
import json
import sqlite3
import logging
import threading
import requests
from pathlib import Path

logger = logging.getLogger(__name__)

# ─────────────────────────────────────────────
#  SQLITE BACKEND
# ─────────────────────────────────────────────
_thread_local = threading.local()
_schema_initialized = False
_schema_lock = threading.Lock()


def _get_sqlite_path() -> str:
    """Retorna o caminho do banco SQLite, criando a pasta 'data/' se necessário."""
    db_path = os.environ.get("SQLITE_DB_PATH")
    if not db_path:
        root = Path(__file__).parent.parent.parent
        data_dir = root / "data"
        data_dir.mkdir(exist_ok=True)
        db_path = str(data_dir / "sessions.db")
    return db_path


def _get_sqlite_conn() -> sqlite3.Connection:
    """Retorna uma conexão SQLite thread-local, criando-a se necessário."""
    if not hasattr(_thread_local, "conn") or _thread_local.conn is None:
        _thread_local.conn = sqlite3.connect(
            _get_sqlite_path(),
            check_same_thread=False,
            detect_types=sqlite3.PARSE_DECLTYPES,
        )
        _thread_local.conn.row_factory = sqlite3.Row
    return _thread_local.conn


def _ensure_sqlite_schema():
    """Cria as tabelas SQLite se ainda não existirem (executado uma vez)."""
    global _schema_initialized
    if _schema_initialized:
        return
    with _schema_lock:
        if _schema_initialized:
            return
        conn = _get_sqlite_conn()
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS sessoes (
                id          TEXT PRIMARY KEY,
                agente_id   TEXT NOT NULL,
                user_nome   TEXT,
                metadata    TEXT DEFAULT '{}',
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS mensagens (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                sessao_id   TEXT NOT NULL,
                sender      TEXT NOT NULL,
                content     TEXT,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sessao_id) REFERENCES sessoes(id)
            );
        """)
        conn.commit()
        _schema_initialized = True
        logger.info("[DB SQLite] Schema inicializado em: %s", _get_sqlite_path())


def _sqlite_criar_ou_carregar_sessao(sessao_id, agente_id, user_nome, metadata) -> dict | None:
    _ensure_sqlite_schema()
    conn = _get_sqlite_conn()
    try:
        if sessao_id:
            cur = conn.execute(
                """UPDATE sessoes
                   SET user_nome=?, metadata=?, updated_at=CURRENT_TIMESTAMP
                   WHERE id=?""",
                (user_nome, json.dumps(metadata), sessao_id),
            )
            conn.commit()
            if cur.rowcount > 0:
                row = conn.execute("SELECT * FROM sessoes WHERE id=?", (sessao_id,)).fetchone()
                return dict(row) if row else None

        # Cria nova sessão
        new_id = str(uuid.uuid4())
        conn.execute(
            "INSERT INTO sessoes (id, agente_id, user_nome, metadata) VALUES (?, ?, ?, ?)",
            (new_id, agente_id, user_nome, json.dumps(metadata)),
        )
        conn.commit()
        row = conn.execute("SELECT * FROM sessoes WHERE id=?", (new_id,)).fetchone()
        return dict(row) if row else None
    except Exception as exc:
        logger.error("[DB SQLite] Erro ao criar/carregar sessão: %s", exc)
        return None


def _sqlite_persistir_mensagem(sessao_id, sender, content) -> bool:
    _ensure_sqlite_schema()
    conn = _get_sqlite_conn()
    try:
        conn.execute(
            "INSERT INTO mensagens (sessao_id, sender, content) VALUES (?, ?, ?)",
            (sessao_id, sender, content),
        )
        conn.commit()
        return True
    except Exception as exc:
        logger.error("[DB SQLite] Erro ao persistir mensagem: %s", exc)
        return False


def _sqlite_obter_todas_mensagens() -> list:
    _ensure_sqlite_schema()
    conn = _get_sqlite_conn()
    try:
        # Pega as mensagens com os nomes dos usuários da sessão
        rows = conn.execute('''
            SELECT m.created_at as timestamp, s.user_nome, m.sender as role, m.content, m.sessao_id as session_id
            FROM mensagens m
            JOIN sessoes s ON m.sessao_id = s.id
            ORDER BY m.created_at DESC
            LIMIT 500
        ''').fetchall()
        return [dict(row) for row in rows]
    except Exception as exc:
        logger.error("[DB SQLite] Erro ao obter mensagens: %s", exc)
        return []


# ─────────────────────────────────────────────
#  SUPABASE BACKEND
# ─────────────────────────────────────────────
def _is_supabase_configured() -> bool:
    return bool(os.environ.get("SUPABASE_URL") and os.environ.get("SUPABASE_KEY"))


def _get_supabase_headers() -> dict:
    key = os.environ.get("SUPABASE_KEY", "")
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }


def _supabase_criar_ou_carregar_sessao(sessao_id, agente_id, user_nome, metadata) -> dict | None:
    if not _is_supabase_configured():
        logger.warning("[DB Supabase] Credenciais ausentes. Ignorando persistência.")
        return None

    url = f"{os.environ.get('SUPABASE_URL')}/rest/v1/sessoes"
    payload = {"agente_id": agente_id, "user_nome": user_nome, "metadata": metadata}

    try:
        if sessao_id:
            payload["id"] = sessao_id
            res = requests.post(
                f"{url}?on_conflict=id", json=payload,
                headers=_get_supabase_headers(), timeout=10,
            )
        else:
            res = requests.post(url, json=payload, headers=_get_supabase_headers(), timeout=10)

        if res.status_code in (200, 201):
            data = res.json()
            return data[0] if data else None

        logger.error("[DB Supabase] Falha ao salvar sessão (HTTP %s): %s", res.status_code, res.text)
    except Exception as exc:
        logger.error("[DB Supabase] Erro de rede: %s", exc)
    return None


def _supabase_persistir_mensagem(sessao_id, sender, content) -> bool:
    if not _is_supabase_configured() or not sessao_id:
        return False

    url = f"{os.environ.get('SUPABASE_URL')}/rest/v1/mensagens"
    payload = {"sessao_id": sessao_id, "sender": sender, "content": content}

    try:
        res = requests.post(url, json=payload, headers=_get_supabase_headers(), timeout=10)
        if res.status_code in (200, 201):
            return True
        logger.error("[DB Supabase] Falha ao persistir mensagem (HTTP %s): %s", res.status_code, res.text)
    except Exception as exc:
        logger.error("[DB Supabase] Erro ao gravar mensagem: %s", exc)
    return False


# ─────────────────────────────────────────────
#  SELEÇÃO AUTOMÁTICA DE BACKEND
# ─────────────────────────────────────────────
def _get_active_backend() -> str:
    """
    Retorna o backend ativo com base nas variáveis de ambiente.
    Padrão: 'sqlite' (sem configuração necessária).
    """
    backend = os.environ.get("DATABASE_BACKEND", "sqlite").lower()
    if backend == "supabase" and not _is_supabase_configured():
        logger.warning(
            "[DB] Backend 'supabase' solicitado mas SUPABASE_URL/SUPABASE_KEY ausentes. "
            "Usando SQLite como fallback."
        )
        return "sqlite"
    return backend


# ─────────────────────────────────────────────
#  INTERFACE PÚBLICA
# ─────────────────────────────────────────────
def criar_ou_carregar_sessao(sessao_id, agente_id, user_nome, metadata) -> dict | None:
    """
    Cria uma nova sessão de chat ou atualiza os metadados de uma existente.
    Retorna o dicionário da sessão ou None em caso de falha.

    Compatível com:
      - SQLite  (DATABASE_BACKEND=sqlite  — padrão)
      - Supabase (DATABASE_BACKEND=supabase)
    """
    backend = _get_active_backend()
    if backend == "supabase":
        return _supabase_criar_ou_carregar_sessao(sessao_id, agente_id, user_nome, metadata)
    return _sqlite_criar_ou_carregar_sessao(sessao_id, agente_id, user_nome, metadata)


def persistir_mensagem(sessao_id, sender, content) -> bool:
    """
    Registra uma mensagem no histórico vinculado à sessão.
    Retorna True se persistido com sucesso, False caso contrário.
    """
    backend = _get_active_backend()
    if backend == "supabase":
        return _supabase_persistir_mensagem(sessao_id, sender, content)
    return _sqlite_persistir_mensagem(sessao_id, sender, content)


def obter_todas_mensagens() -> list:
    """
    Retorna as últimas 500 mensagens para o Dashboard Administrativo.
    Formato: [{'created_at': '...', 'user_nome': '...', 'sender': '...', 'content': '...'}]
    """
    backend = _get_active_backend()
    if backend == "supabase":
        # Placeholder para Supabase (requer RPC ou select nas duas tabelas via REST)
        return []
    return _sqlite_obter_todas_mensagens()
