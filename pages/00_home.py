"""
pages/00_home.py - Pagina inicial do KanBite
Dev 4 - Sprint 3
"""
import streamlit as st
from components.sidebar import render_sidebar

st.set_page_config(page_title="KanBite", page_icon="🍕")
render_sidebar()
st.title("🍕 KanBite")
st.subheader("Sistema Kanban para Restaurantes Italianos")

if "username" in st.session_state:
    st.success(f"👋 Olá, **{st.session_state['username']}**! Bem-vindo de volta.")
    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/04_board.py",   label="📋 Ir para o Quadro",   use_container_width=True)
    with col2:
        st.page_link("pages/03_metrics.py", label="📊 Ver Métricas",       use_container_width=True)
    if st.button("🚪 Sair"):
        st.session_state.clear()
        st.rerun()
