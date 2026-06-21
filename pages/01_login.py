"""
pages/01_login.py - Tela de Login
Dev 4 - Sprint 3
"""
import streamlit as st
from database.engine import get_session
from services.auth_service import (
    autenticar,
    CredenciaisInvalidasError,
    UsuarioInativoError,
)

st.set_page_config(page_title="Login — KanBite", page_icon="🔐")
from components.sidebar import render_sidebar
render_sidebar()

if "user_id" in st.session_state:
    st.success(f"Você já está logado como **{st.session_state['username']}**.")
    st.page_link("pages/00_home.py", label="Ir para a Home →")
    st.stop()

st.title("🔐 Entrar no KanBite")

with st.form("form_login", clear_on_submit=False):
    username = st.text_input("Usuário", placeholder="ex: chef_mario")
    senha    = st.text_input("Senha", type="password", placeholder="••••••••")
    submitted = st.form_submit_button("Entrar", use_container_width=True)

if submitted:
    if not username or not senha:
        st.error("Preencha usuário e senha.")
    else:
        try:
            session = get_session()
            user = autenticar(session, username, senha)
            st.session_state["user_id"]  = user.id
            st.session_state["username"] = user.username
            st.success(f"✅ Bem-vindo, **{user.username}**!")
            st.balloons()
            st.switch_page("pages/00_home.py")
        except CredenciaisInvalidasError:
            st.error("❌ Usuário ou senha incorretos.")
        except UsuarioInativoError:
            st.error("❌ Esta conta está desativada.")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")

