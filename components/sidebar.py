"""
components/sidebar.py - Sidebar de navegacao
Dev 4 - Sprint 3
"""
import streamlit as st


def render_sidebar():
    """Renderiza a sidebar com info do usuario e navegacao."""
    with st.sidebar:
        st.markdown("## 🍕 KanBite")
        st.divider()

        if "username" in st.session_state:
            st.success(f"👤 **{st.session_state['username']}**")
            st.page_link("pages/00_home.py",    label="🏠 Home")
            st.page_link("pages/04_board.py",   label="📋 Quadro")
            st.page_link("pages/03_metrics.py", label="📊 Métricas")
            st.divider()
            if st.button("🚪 Sair", use_container_width=True):
                st.session_state.clear()
                st.rerun()
        else:
            st.info("Não autenticado")
            st.page_link("pages/01_login.py",    label="🔐 Login")
            st.page_link("pages/02_register.py", label="📝 Cadastro")