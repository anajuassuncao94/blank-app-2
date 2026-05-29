from database.connection import get_connection


def criar_usuario(nome: str, usuario: str, senha_hash: str) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO usuarios (nome, usuario, senha_hash)
                VALUES (%s, %s, %s)
                RETURNING id, nome, usuario, criado_em;
                """,
                (nome.strip(), usuario.strip().lower(), senha_hash),
            )
            return dict(cur.fetchone())


def buscar_por_usuario(usuario: str) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nome, usuario, senha_hash, criado_em
                FROM usuarios
                WHERE usuario = %s;
                """,
                (usuario.strip().lower(),),
            )
            row = cur.fetchone()
            return dict(row) if row else None
