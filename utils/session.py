import streamlit as st


def set_usuario_logado(usuario: dict) -> None:
    st.session_state["usuario_logado"] = usuario


def get_usuario_logado() -> dict | None:
    return st.session_state.get("usuario_logado")


def usuario_esta_logado() -> bool:
    return get_usuario_logado() is not None


def logout() -> None:
    st.session_state.pop("usuario_logado", None)


def require_login() -> dict:
    usuario = get_usuario_logado()

    if not usuario:
        st.warning("Você precisa fazer login para acessar esta página.")
        st.stop()

    return usuario


def mostrar_sidebar_usuario() -> None:
    usuario = get_usuario_logado()
    if usuario:
        st.sidebar.success(f"Logado como: {usuario['nome']}")
        if st.sidebar.button("Sair"):
            logout()
            st.rerun()
