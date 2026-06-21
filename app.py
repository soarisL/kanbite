"""
app.py - Entry point do KanBite (Streamlit multi-page)
Dev 4 - Sprint 3 (final)
"""
import streamlit as st

st.set_page_config(
    page_title="KanBite",
    page_icon="🍕",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Carregar CSS customizado
import os
css_path = os.path.join(os.path.dirname(__file__), "assets", "style.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

st.title("🍕 KanBite")
st.caption("Sistema Kanban para restaurantes italianos")

if "username" in st.session_state:
    st.info(f"👋 Olá, **{st.session_state['username']}**! Use o menu lateral para navegar.")
else:
    st.info("Navegue pelas páginas no menu lateral para fazer login ou se cadastrar.")