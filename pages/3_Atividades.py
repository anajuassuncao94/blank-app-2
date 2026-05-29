from datetime import date, timedelta

import pandas as pd
import streamlit as st

from database.init_db import init_db
from repositories.atividades import (
    criar_atividade,
    excluir_atividade,
    listar_atividades,
    marcar_concluida,
)
from repositories.disciplinas import listar_disciplinas
from utils.session import mostrar_sidebar_usuario, require_login

st.set_page_config(page_title="Atividades", page_icon="📝", layout="wide")

init_db()
usuario = require_login()
mostrar_sidebar_usuario()

st.title("📝 Atividades acadêmicas")
st.write("Cadastre provas, trabalhos, listas e revisões para que o sistema priorize o cronograma.")

disciplinas = listar_disciplinas(usuario["id"])
disciplina_opcoes = {"Sem disciplina específica": None}
disciplina_opcoes.update({d["nome"]: d["id"] for d in disciplinas})

with st.form("form_atividade"):
    col1, col2 = st.columns([2, 1])

    with col1:
        titulo = st.text_input("Título da atividade", placeholder="Ex.: Lista de exercícios 1")
        disciplina_label = st.selectbox("Disciplina", list(disciplina_opcoes.keys()))
        tipo = st.selectbox("Tipo", ["Prova", "Trabalho", "Lista", "Revisao", "Estudo"])

    with col2:
        data_entrega = st.date_input("Data de entrega/prova", value=date.today() + timedelta(days=7))
        duracao_minutos = st.number_input("Tempo estimado em minutos", min_value=30, step=30, value=60)
        urgencia = st.slider("Urgência", min_value=1, max_value=5, value=3)
        dificuldade = st.slider("Dificuldade", min_value=1, max_value=5, value=3)

    salvar = st.form_submit_button("Cadastrar atividade")

if salvar:
    if not titulo.strip():
        st.error("Informe o título da atividade.")
    else:
        try:
            criar_atividade(
                usuario_id=usuario["id"],
                disciplina_id=disciplina_opcoes[disciplina_label],
                titulo=titulo,
                tipo=tipo,
                data_entrega=data_entrega,
                urgencia=int(urgencia),
                dificuldade=int(dificuldade),
                duracao_minutos=int(duracao_minutos),
            )
            st.success("Atividade cadastrada com sucesso.")
            st.rerun()
        except Exception as exc:
            st.error(f"Erro ao cadastrar atividade: {exc}")

atividades = listar_atividades(usuario["id"], incluir_concluidas=True)

st.markdown("### Atividades cadastradas")

if not atividades:
    st.info("Nenhuma atividade cadastrada ainda.")
    st.stop()

df = pd.DataFrame(atividades)
colunas = [
    "id",
    "titulo",
    "tipo",
    "disciplina_nome",
    "data_entrega",
    "urgencia",
    "dificuldade",
    "duracao_minutos",
    "concluida",
]
df_exibicao = df[colunas].rename(
    columns={
        "id": "ID",
        "titulo": "Título",
        "tipo": "Tipo",
        "disciplina_nome": "Disciplina",
        "data_entrega": "Data",
        "urgencia": "Urgência",
        "dificuldade": "Dificuldade",
        "duracao_minutos": "Duração",
        "concluida": "Concluída",
    }
)
st.dataframe(df_exibicao, use_container_width=True, hide_index=True)

st.markdown("### Atualizar atividade")

opcoes = {f"{a['id']} - {a['titulo']}": a for a in atividades}
selecionada_label = st.selectbox("Selecione a atividade", list(opcoes.keys()))
selecionada = opcoes[selecionada_label]

col1, col2 = st.columns(2)

with col1:
    novo_status = st.checkbox("Concluída", value=bool(selecionada["concluida"]))
    if st.button("Salvar status"):
        try:
            marcar_concluida(usuario["id"], selecionada["id"], novo_status)
            st.success("Status atualizado com sucesso.")
            st.rerun()
        except Exception as exc:
            st.error(f"Erro ao atualizar status: {exc}")

with col2:
    st.warning("Excluir uma atividade remove ela do banco.")
    if st.button("Excluir atividade"):
        try:
            excluir_atividade(usuario["id"], selecionada["id"])
            st.success("Atividade excluída com sucesso.")
            st.rerun()
        except Exception as exc:
            st.error(f"Erro ao excluir atividade: {exc}")
