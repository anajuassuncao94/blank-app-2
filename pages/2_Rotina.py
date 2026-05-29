from datetime import time

import pandas as pd
import streamlit as st

from database.init_db import init_db
from repositories.horarios import criar_horario, excluir_horario, listar_horarios
from utils.session import mostrar_sidebar_usuario, require_login
from utils.validators import horario_valido

st.set_page_config(page_title="Rotina", page_icon="🕒", layout="wide")

init_db()
usuario = require_login()
mostrar_sidebar_usuario()

st.title("🕒 Rotina de estudos")
st.write("Cadastre os horários livres por dia da semana.")

DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]

with st.form("form_horario"):
    col1, col2, col3 = st.columns(3)

    with col1:
        dia_semana = st.selectbox("Dia da semana", DIAS)
    with col2:
        hora_inicio = st.time_input("Hora de início", value=time(18, 0))
    with col3:
        hora_fim = st.time_input("Hora de fim", value=time(19, 0))

    salvar = st.form_submit_button("Cadastrar horário livre")

if salvar:
    if not horario_valido(hora_inicio, hora_fim):
        st.error("A hora final deve ser maior que a hora inicial.")
    else:
        try:
            criar_horario(usuario["id"], dia_semana, hora_inicio, hora_fim)
            st.success("Horário livre cadastrado com sucesso.")
            st.rerun()
        except Exception as exc:
            st.error(f"Erro ao cadastrar horário: {exc}")

horarios = listar_horarios(usuario["id"])

st.markdown("### Horários cadastrados")

if not horarios:
    st.info("Nenhum horário livre cadastrado ainda.")
    st.stop()

df = pd.DataFrame(horarios)
df["hora_inicio"] = df["hora_inicio"].astype(str).str.slice(0, 5)
df["hora_fim"] = df["hora_fim"].astype(str).str.slice(0, 5)

st.dataframe(
    df[["id", "dia_semana", "hora_inicio", "hora_fim"]].rename(
        columns={
            "id": "ID",
            "dia_semana": "Dia",
            "hora_inicio": "Início",
            "hora_fim": "Fim",
        }
    ),
    use_container_width=True,
    hide_index=True,
)

st.markdown("### Excluir horário")

opcoes = {
    f"{h['id']} - {h['dia_semana']} {str(h['hora_inicio'])[:5]} às {str(h['hora_fim'])[:5]}": h
    for h in horarios
}
selecionado_label = st.selectbox("Selecione o horário", list(opcoes.keys()))
selecionado = opcoes[selecionado_label]

if st.button("Excluir horário selecionado"):
    try:
        excluir_horario(usuario["id"], selecionado["id"])
        st.success("Horário excluído com sucesso.")
        st.rerun()
    except Exception as exc:
        st.error(f"Erro ao excluir horário: {exc}")
