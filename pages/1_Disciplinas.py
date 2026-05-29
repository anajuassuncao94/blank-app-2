import pandas as pd
import streamlit as st
from psycopg2.errors import UniqueViolation

from database.init_db import init_db
from repositories.disciplinas import (
    atualizar_disciplina,
    criar_disciplina,
    excluir_disciplina,
    listar_disciplinas,
)
from utils.session import mostrar_sidebar_usuario, require_login

st.set_page_config(page_title="Disciplinas", page_icon="📘", layout="wide")

init_db()
usuario = require_login()
mostrar_sidebar_usuario()

st.title("📘 Disciplinas")
st.write("Cadastre as disciplinas que você precisa estudar.")

with st.form("form_nova_disciplina"):
    col1, col2, col3 = st.columns([3, 1, 1])

    with col1:
        nome = st.text_input("Nome da disciplina", placeholder="Ex.: Programação Avançada")
    with col2:
        carga_horaria = st.number_input("Carga horária", min_value=0, step=1, value=60)
    with col3:
        dificuldade = st.slider("Dificuldade", min_value=1, max_value=5, value=3)

    salvar = st.form_submit_button("Cadastrar disciplina")

if salvar:
    if not nome.strip():
        st.error("Informe o nome da disciplina.")
    else:
        try:
            criar_disciplina(
                usuario_id=usuario["id"],
                nome=nome,
                carga_horaria=int(carga_horaria) if carga_horaria else None,
                dificuldade=int(dificuldade),
            )
            st.success("Disciplina cadastrada com sucesso.")
            st.rerun()
        except UniqueViolation:
            st.error("Essa disciplina já foi cadastrada.")
        except Exception as exc:
            st.error(f"Erro ao cadastrar disciplina: {exc}")

disciplinas = listar_disciplinas(usuario["id"])

st.markdown("### Disciplinas cadastradas")

if not disciplinas:
    st.info("Nenhuma disciplina cadastrada ainda.")
    st.stop()

df = pd.DataFrame(disciplinas)
df_exibicao = df[["id", "nome", "carga_horaria", "dificuldade"]].rename(
    columns={
        "id": "ID",
        "nome": "Disciplina",
        "carga_horaria": "Carga horária",
        "dificuldade": "Dificuldade",
    }
)
st.dataframe(df_exibicao, use_container_width=True, hide_index=True)

st.markdown("### Editar ou excluir disciplina")

opcoes = {f"{d['id']} - {d['nome']}": d for d in disciplinas}
selecionada_label = st.selectbox("Selecione a disciplina", list(opcoes.keys()))
selecionada = opcoes[selecionada_label]

with st.form("form_editar_disciplina"):
    novo_nome = st.text_input("Nome", value=selecionada["nome"])
    nova_carga = st.number_input(
        "Carga horária",
        min_value=0,
        step=1,
        value=int(selecionada["carga_horaria"] or 0),
    )
    nova_dificuldade = st.slider(
        "Dificuldade",
        min_value=1,
        max_value=5,
        value=int(selecionada["dificuldade"]),
    )

    col1, col2 = st.columns(2)
    atualizar = col1.form_submit_button("Atualizar")
    excluir = col2.form_submit_button("Excluir")

if atualizar:
    try:
        atualizar_disciplina(
            usuario_id=usuario["id"],
            disciplina_id=selecionada["id"],
            nome=novo_nome,
            carga_horaria=int(nova_carga) if nova_carga else None,
            dificuldade=int(nova_dificuldade),
        )
        st.success("Disciplina atualizada com sucesso.")
        st.rerun()
    except Exception as exc:
        st.error(f"Erro ao atualizar disciplina: {exc}")

if excluir:
    try:
        excluir_disciplina(usuario["id"], selecionada["id"])
        st.success("Disciplina excluída com sucesso.")
        st.rerun()
    except Exception as exc:
        st.error(f"Erro ao excluir disciplina: {exc}")
