from datetime import date, datetime, time, timedelta

from repositories.atividades import listar_atividades
from repositories.cronogramas import criar_cronograma, inserir_item
from repositories.disciplinas import listar_disciplinas
from repositories.horarios import listar_horarios

ORDEM_DIAS = {
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


def _minutos_entre(inicio: time, fim: time) -> int:
    data_base = date(2000, 1, 1)
    dt_inicio = datetime.combine(data_base, inicio)
    dt_fim = datetime.combine(data_base, fim)
    return int((dt_fim - dt_inicio).total_seconds() / 60)


def _somar_minutos(hora: time, minutos: int) -> time:
    data_base = date(2000, 1, 1)
    return (datetime.combine(data_base, hora) + timedelta(minutes=minutos)).time()


def _quebrar_horarios_em_blocos(horarios: list[dict], tamanho_bloco: int = 60) -> list[dict]:
    """Transforma janelas de horários livres em blocos menores de estudo."""
    blocos = []

    for horario in horarios:
        atual = horario["hora_inicio"]
        fim = horario["hora_fim"]

        while _minutos_entre(atual, fim) > 0:
            duracao = min(tamanho_bloco, _minutos_entre(atual, fim))
            proximo = _somar_minutos(atual, duracao)

            blocos.append(
                {
                    "dia_semana": horario["dia_semana"],
                    "hora_inicio": atual,
                    "hora_fim": proximo,
                    "duracao": duracao,
                }
            )

            atual = proximo

    return sorted(blocos, key=lambda b: (ORDEM_DIAS.get(b["dia_semana"], 99), b["hora_inicio"]))


def _pontuar_atividade(atividade: dict) -> int:
    """Calcula prioridade usando urgência, dificuldade e proximidade da data."""
    urgencia = int(atividade.get("urgencia") or 1)
    dificuldade = int(atividade.get("dificuldade") or 1)

    pontos_data = 0
    data_entrega = atividade.get("data_entrega")
    if data_entrega:
        dias_restantes = (data_entrega - date.today()).days
        if dias_restantes <= 0:
            pontos_data = 30
        else:
            pontos_data = max(0, 30 - dias_restantes)

    return urgencia * 5 + dificuldade * 3 + pontos_data


def _preparar_fila_atividades(atividades: list[dict]) -> list[dict]:
    fila = []
    for atividade in atividades:
        item = dict(atividade)
        item["restante_minutos"] = int(item.get("duracao_minutos") or 60)
        item["pontuacao"] = _pontuar_atividade(item)
        fila.append(item)

    return sorted(
        fila,
        key=lambda a: (
            -a["pontuacao"],
            a.get("data_entrega") or date(2999, 12, 31),
            a.get("titulo", ""),
        ),
    )


def _selecionar_proxima_atividade(fila: list[dict]) -> dict | None:
    for atividade in fila:
        if atividade["restante_minutos"] > 0:
            return atividade
    return None


def gerar_cronograma_automatico(usuario_id: int) -> tuple[bool, str, dict | None]:
    """Gera e salva um cronograma semanal com base nos horários, disciplinas e atividades."""
    horarios = listar_horarios(usuario_id)
    disciplinas = listar_disciplinas(usuario_id)
    atividades = listar_atividades(usuario_id, incluir_concluidas=False)

    if not horarios:
        return False, "Cadastre pelo menos um horário livre antes de gerar o cronograma.", None

    if not disciplinas and not atividades:
        return False, "Cadastre pelo menos uma disciplina ou atividade antes de gerar o cronograma.", None

    blocos = _quebrar_horarios_em_blocos(horarios)
    fila_atividades = _preparar_fila_atividades(atividades)

    cronograma = criar_cronograma(
        usuario_id,
        "Cronograma gerado automaticamente com base em horários livres, disciplinas e atividades.",
    )

    indice_disciplina = 0

    for bloco in blocos:
        atividade = _selecionar_proxima_atividade(fila_atividades)

        if atividade:
            disciplina_nome = atividade.get("disciplina_nome") or "Sem disciplina"
            descricao = f"{disciplina_nome}: {atividade['titulo']} ({atividade['tipo']})"
            disciplina_id = atividade.get("disciplina_id")
            atividade_id = atividade.get("id")
            atividade["restante_minutos"] -= bloco["duracao"]
        else:
            disciplina = disciplinas[indice_disciplina % len(disciplinas)] if disciplinas else None
            if disciplina:
                descricao = f"Estudar {disciplina['nome']}"
                disciplina_id = disciplina["id"]
                atividade_id = None
                indice_disciplina += 1
            else:
                descricao = "Estudo livre"
                disciplina_id = None
                atividade_id = None

        inserir_item(
            cronograma_id=cronograma["id"],
            usuario_id=usuario_id,
            dia_semana=bloco["dia_semana"],
            hora_inicio=bloco["hora_inicio"],
            hora_fim=bloco["hora_fim"],
            descricao=descricao,
            disciplina_id=disciplina_id,
            atividade_id=atividade_id,
        )

    return True, "Cronograma gerado com sucesso.", cronograma
