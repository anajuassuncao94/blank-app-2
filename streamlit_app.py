import streamlit as st

from database.init_db import init_db
from services.auth_service import autenticar, cadastrar_usuario
from utils.session import (
    get_usuario_logado,
    mostrar_sidebar_usuario,
    set_usuario_logado,
)

st.set_page_config(
    page_title="OrganizaAí Estudos",
    page_icon="📚",
    layout="wide",
)

try:
    init_db()
except Exception as exc:
    st.error("Não foi possível conectar ou inicializar o banco de dados.")
    st.exception(exc)
    st.stop()

st.title("📚 OrganizaAí Estudos")
st.subheader("Planejamento automático de estudos para universitários")

mostrar_sidebar_usuario()

usuario_logado = get_usuario_logado()

if usuario_logado:
    st.success(f"Bem-vindo(a), {usuario_logado['nome']}!")

    st.markdown(
        """
        Use o menu lateral para acessar:

        - **Disciplinas**: cadastrar, editar e excluir matérias;
        - **Rotina**: cadastrar horários livres por dia da semana;
        - **Atividades**: cadastrar provas, trabalhos e listas;
        - **Cronograma**: gerar, recalcular e exportar o cronograma semanal.
        """
    )

    st.info("Dica: primeiro cadastre disciplinas e horários livres. Depois, gere o cronograma.")
    st.stop()

aba_login, aba_cadastro = st.tabs(["Entrar", "Cadastrar novo usuário"])

with aba_login:
    st.markdown("### Login")

    with st.form("form_login"):
        usuario = st.text_input("Usuário")
        senha = st.text_input("Senha", type="password")
        entrar = st.form_submit_button("Entrar")

    if entrar:
        ok, usuario_db, mensagem = autenticar(usuario, senha)

        if ok:
            set_usuario_logado(usuario_db)
            st.success(mensagem)
            st.rerun()
        else:
            st.error(mensagem)

with aba_cadastro:
    st.markdown("### Cadastro de usuário")

    with st.form("form_cadastro_usuario"):
        nome = st.text_input("Nome completo")
        novo_usuario = st.text_input("Usuário de acesso")
        nova_senha = st.text_input("Senha", type="password")
        confirmar_senha = st.text_input("Confirmar senha", type="password")
        cadastrar = st.form_submit_button("Cadastrar")

    if cadastrar:
        if nova_senha != confirmar_senha:
            st.error("As senhas não conferem.")
        else:
            ok, mensagem = cadastrar_usuario(nome, novo_usuario, nova_senha)
            if ok:
                st.success(mensagem)
            else:
                st.error(mensagem)