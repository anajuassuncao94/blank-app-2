from database.connection import get_connection


def criar_cronograma(usuario_id: int, observacao: str | None = None) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO cronogramas (usuario_id, observacao)
                VALUES (%s, %s)
                RETURNING *;
                """,
                (usuario_id, observacao),
            )
            return dict(cur.fetchone())


def inserir_item(
    cronograma_id: int,
    usuario_id: int,
    dia_semana: str,
    hora_inicio,
    hora_fim,
    descricao: str,
    disciplina_id: int | None = None,
    atividade_id: int | None = None,
) -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO itens_cronograma (
                    cronograma_id, usuario_id, dia_semana, hora_inicio, hora_fim,
                    disciplina_id, atividade_id, descricao
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
                """,
                (
                    cronograma_id,
                    usuario_id,
                    dia_semana,
                    hora_inicio,
                    hora_fim,
                    disciplina_id,
                    atividade_id,
                    descricao,
                ),
            )
            return dict(cur.fetchone())


def buscar_ultimo_cronograma(usuario_id: int) -> dict | None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT *
                FROM cronogramas
                WHERE usuario_id = %s
                ORDER BY data_criacao DESC
                LIMIT 1;
                """,
                (usuario_id,),
            )
            row = cur.fetchone()
            return dict(row) if row else None


def listar_itens_cronograma(usuario_id: int, cronograma_id: int) -> list[dict]:
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
                SELECT i.*, d.nome AS disciplina_nome, a.titulo AS atividade_titulo
                FROM itens_cronograma i
                LEFT JOIN disciplinas d ON d.id = i.disciplina_id
                LEFT JOIN atividades a ON a.id = i.atividade_id
                WHERE i.usuario_id = %s AND i.cronograma_id = %s;
                """,
                (usuario_id, cronograma_id),
            )
            rows = [dict(row) for row in cur.fetchall()]

    return sorted(rows, key=lambda item: (ordem.get(item["dia_semana"], 99), item["hora_inicio"]))


def excluir_cronograma(usuario_id: int, cronograma_id: int) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                DELETE FROM cronogramas
                WHERE id = %s AND usuario_id = %s;
                """,
                (cronograma_id, usuario_id),
            )
