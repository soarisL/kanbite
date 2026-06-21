"""
pages/02_register.py - Tela de Cadastro
Dev 4 - Sprint 3
"""
import streamlit as st
from database.engine import get_session
from services.auth_service import registrar, UsuarioJaExisteError

st.set_page_config(page_title="Cadastro — KanBite", page_icon="📝")

if "user_id" in st.session_state:
    st.info(f"Você já possui uma conta: **{st.session_state['username']}**.")
    st.stop()

st.title("📝 Criar Conta no KanBite")

with st.form("form_registro", clear_on_submit=False):
    username = st.text_input("Usuário", placeholder="ex: chef_mario")
    email    = st.text_input("E-mail",  placeholder="ex: mario@ristorante.com")
    senha    = st.text_input("Senha",           type="password")
    confirma = st.text_input("Confirmar Senha", type="password")
    submitted = st.form_submit_button("Criar Conta", use_container_width=True)

if submitted:
    if not username or not email or not senha:
        st.error("Todos os campos são obrigatórios.")
    elif len(senha) < 6:
        st.error("A senha deve ter pelo menos 6 caracteres.")
    elif senha != confirma:
        st.error("As senhas não coincidem.")
    else:
        try:
            session = get_session()
            user = registrar(session, username, email, senha)
            st.success(f"✅ Conta criada! Olá, **{user.username}**. Faça o login.")
            st.page_link("pages/01_login.py", label="Ir para o Login →")
        except UsuarioJaExisteError:
            st.error("❌ Usuário ou e-mail já cadastrado.")
        except Exception as e:
            st.error(f"Erro inesperado: {e}")

st.divider()
st.caption("Já tem conta? [Faça login aqui](01_login)")