from datetime import time

from database.connection import get_connection


def criar_horario(usuario_id: int, dia_semana: str, hora_inicio: time, hora_fim: time) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO horarios_livres (usuario_id, dia_semana, hora_inicio, hora_fim)
                VALUES (%s, %s, %s, %s)
                RETURNING *;
                """,
                (usuario_id, dia_semana, hora_inicio, hora_fim),
            )
            return dict(cur.fetchone())


def listar_horarios(usuario_id: int) -> list[dict]:
    ordem = {
        "Segunda": 1,
        "Terca": 2,
        "Terça": 2,
        "Quarta": 3,
        "Quinta": 4,
        "Sexta": 5,
        "Sabado": 6,
        "Sábado": 6,
        "Domingo": 7,
    }

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, dia_semana, hora_inicio, hora_fim, criado_em
                FROM horarios_livres
                WHERE usuario_id = %s;
                """,
                (usuario_id,),
            )
            rows = [dict(row) for row in cur.fetchall()]

    return sorted(rows, key=lambda h: (ordem.get(h["dia_semana"], 99), h["hora_inicio"]))


def excluir_horario(usuario_id: int, horario_id: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM horarios_livres
                WHERE id = %s AND usuario_id = %s;
                """,
                (horario_id, usuario_id),
            )
