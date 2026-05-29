from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle


def gerar_pdf_cronograma(usuario: dict, cronograma: dict, itens: list[dict]) -> bytes:
    """Gera PDF do cronograma semanal."""
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=1.2 * cm,
        leftMargin=1.2 * cm,
        topMargin=1.2 * cm,
        bottomMargin=1.2 * cm,
    )

    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("OrganizaAí Estudos", styles["Title"]))
    story.append(Paragraph("Cronograma Semanal de Estudos", styles["Heading2"]))
    story.append(Paragraph(f"Usuário: {usuario['nome']}", styles["Normal"]))
    story.append(Paragraph(f"Gerado em: {cronograma['data_criacao']}", styles["Normal"]))
    story.append(Spacer(1, 0.4 * cm))

    ordenacao_dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    mapa_dia = {"Terca": "Terça", "Sabado": "Sábado"}
    horarios = []
    tabela_dict: dict[str, dict[str, str]] = {}

    for item in itens:
        horario = f"{str(item['hora_inicio'])[:5]} - {str(item['hora_fim'])[:5]}"
        dia = mapa_dia.get(item["dia_semana"], item["dia_semana"])
        descricao = item["descricao"]

        if horario not in tabela_dict:
            tabela_dict[horario] = {dia: descricao}
        else:
            tabela_dict[horario][dia] = " / ".join(
                [tabela_dict[horario].get(dia, ""), descricao] if tabela_dict[horario].get(dia) else [descricao]
            )

        if horario not in horarios:
            horarios.append(horario)

    dias_presentes = [dia for dia in ordenacao_dias if any(dia in row for row in tabela_dict.values())]
    if not dias_presentes:
        dias_presentes = ordenacao_dias

    dados = [["Dia/Horários"] + dias_presentes]

    for horario in sorted(horarios, key=lambda h: tuple(int(x) for x in h.split(" - ")[0].split(":"))):
        linha = [horario]
        for dia in dias_presentes:
            linha.append(tabela_dict.get(horario, {}).get(dia, ""))
        dados.append(linha)

    total_col_width = 28 * cm
    col_widths = [4.5 * cm] + [(total_col_width - 4.5 * cm) / max(len(dias_presentes), 1)] * len(dias_presentes)

    tabela = Table(dados, colWidths=col_widths)
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
                ("ALIGN", (0, 0), (0, -1), "LEFT"),
                ("ALIGN", (1, 0), (-1, -1), "LEFT"),
            ]
        )
    )

    story.append(tabela)
    doc.build(story)

    buffer.seek(0)
    return buffer.read()
