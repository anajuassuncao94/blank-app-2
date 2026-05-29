from datetime import date

from database.connection import get_connection


def criar_atividade(
    usuario_id: int,
    disciplina_id: int | None,
    titulo: str,
    tipo: str,
    data_entrega: date | None,
    urgencia: int,
    dificuldade: int,
    duracao_minutos: int,
) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO atividades (
                    usuario_id, disciplina_id, titulo, tipo, data_entrega,
                    urgencia, dificuldade, duracao_minutos
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (
                    usuario_id,
                    disciplina_id,
                    titulo.strip(),
                    tipo,
                    data_entrega,
                    urgencia,
                    dificuldade,
                    duracao_minutos,
                ),
            )
            return dict(cur.fetchone())


def listar_atividades(usuario_id: int, incluir_concluidas: bool = True) -> list[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            if incluir_concluidas:
                cur.execute(
                    """
                    SELECT a.*, d.nome AS disciplina_nome
                    FROM atividades a
                    LEFT JOIN disciplinas d ON d.id = a.disciplina_id
                    WHERE a.usuario_id = %s
                    ORDER BY a.concluida, a.data_entrega NULLS LAST, a.urgencia DESC, a.dificuldade DESC;
                    """,
                    (usuario_id,),
                )
            else:
                cur.execute(
                    """
                    SELECT a.*, d.nome AS disciplina_nome
                    FROM atividades a
                    LEFT JOIN disciplinas d ON d.id = a.disciplina_id
                    WHERE a.usuario_id = %s AND a.concluida = FALSE
                    ORDER BY a.data_entrega NULLS LAST, a.urgencia DESC, a.dificuldade DESC;
                    """,
                    (usuario_id,),
                )

            return [dict(row) for row in cur.fetchall()]


def marcar_concluida(usuario_id: int, atividade_id: int, concluida: bool) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE atividades
                SET concluida = %s
                WHERE id = %s AND usuario_id = %s;
                """,
                (concluida, atividade_id, usuario_id),
            )


def excluir_atividade(usuario_id: int, atividade_id: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM atividades
                WHERE id = %s AND usuario_id = %s;
                """,
                (atividade_id, usuario_id),
            )
