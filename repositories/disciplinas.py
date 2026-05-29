from database.connection import get_connection


def criar_disciplina(usuario_id: int, nome: str, carga_horaria: int | None, dificuldade: int) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO disciplinas (usuario_id, nome, carga_horaria, dificuldade)
                VALUES (%s, %s, %s, %s)
                RETURNING *;
                """,
                (usuario_id, nome.strip(), carga_horaria, dificuldade),
            )
            return dict(cur.fetchone())


def listar_disciplinas(usuario_id: int) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, nome, carga_horaria, dificuldade, criada_em
                FROM disciplinas
                WHERE usuario_id = %s
                ORDER BY nome;
                """,
                (usuario_id,),
            )
            return [dict(row) for row in cur.fetchall()]


def atualizar_disciplina(
    usuario_id: int,
    disciplina_id: int,
    nome: str,
    carga_horaria: int | None,
    dificuldade: int,
) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE disciplinas
                SET nome = %s, carga_horaria = %s, dificuldade = %s
                WHERE id = %s AND usuario_id = %s;
                """,
                (nome.strip(), carga_horaria, dificuldade, disciplina_id, usuario_id),
            )


def excluir_disciplina(usuario_id: int, disciplina_id: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM disciplinas
                WHERE id = %s AND usuario_id = %s;
                """,
                (disciplina_id, usuario_id),
            )
