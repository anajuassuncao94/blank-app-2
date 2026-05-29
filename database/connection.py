import os
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import RealDictCursor
import streamlit as st


def _get_database_url() -> str:
    """Lê a URL do banco a partir do Streamlit Secrets ou variável de ambiente."""
    url = os.getenv("DATABASE_URL")

    if not url:
        try:
            url = st.secrets.get("DATABASE_URL")
        except Exception:
            url = None

    if not url:
        raise RuntimeError(
            "DATABASE_URL não configurada. Configure em .streamlit/secrets.toml "
            "ou nos Secrets do Streamlit Cloud."
        )

    # Render PostgreSQL normalmente exige SSL em conexões externas.
    if "sslmode=" not in url:
        separator = "&" if "?" in url else "?"
        url = f"{url}{separator}sslmode=require"

    return url


@contextmanager
def get_connection():
    """Abre conexão com PostgreSQL e fecha automaticamente ao final."""
    conn = psycopg2.connect(_get_database_url(), cursor_factory=RealDictCursor)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
