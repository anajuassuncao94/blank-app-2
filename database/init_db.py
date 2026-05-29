from database.connection import get_connection


def init_db() -> None:
    """Cria as tabelas necessárias para o OrganizaAí, caso ainda não existam."""
    commands = [
        """
        CREATE TABLE IF NOT EXISTS usuarios (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(120) NOT NULL,
            usuario VARCHAR(80) NOT NULL UNIQUE,
            senha_hash TEXT NOT NULL,
            criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS disciplinas (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            nome VARCHAR(120) NOT NULL,
            carga_horaria INTEGER,
            dificuldade INTEGER NOT NULL DEFAULT 3 CHECK (dificuldade BETWEEN 1 AND 5),
            criada_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(usuario_id, nome)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS horarios_livres (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            dia_semana VARCHAR(20) NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fim TIME NOT NULL,
            criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            CHECK (hora_fim > hora_inicio)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS atividades (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            disciplina_id INTEGER REFERENCES disciplinas(id) ON DELETE SET NULL,
            titulo VARCHAR(160) NOT NULL,
            tipo VARCHAR(30) NOT NULL,
            data_entrega DATE,
            urgencia INTEGER NOT NULL DEFAULT 3 CHECK (urgencia BETWEEN 1 AND 5),
            dificuldade INTEGER NOT NULL DEFAULT 3 CHECK (dificuldade BETWEEN 1 AND 5),
            duracao_minutos INTEGER NOT NULL DEFAULT 60 CHECK (duracao_minutos > 0),
            concluida BOOLEAN NOT NULL DEFAULT FALSE,
            criada_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS cronogramas (
            id SERIAL PRIMARY KEY,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            data_criacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
            observacao TEXT
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS itens_cronograma (
            id SERIAL PRIMARY KEY,
            cronograma_id INTEGER NOT NULL REFERENCES cronogramas(id) ON DELETE CASCADE,
            usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
            dia_semana VARCHAR(20) NOT NULL,
            hora_inicio TIME NOT NULL,
            hora_fim TIME NOT NULL,
            disciplina_id INTEGER REFERENCES disciplinas(id) ON DELETE SET NULL,
            atividade_id INTEGER REFERENCES atividades(id) ON DELETE SET NULL,
            descricao TEXT NOT NULL,
            criado_em TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
        );
        """,
    ]

    with get_connection() as conn:
        with conn.cursor() as cur:
            for command in commands:
                cur.execute(command)
