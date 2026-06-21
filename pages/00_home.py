"""
pages/00_home.py - Pagina inicial do KanBite
Dev 4 - Sprint 3
"""
import streamlit as st

st.set_page_config(page_title="KanBite", page_icon="🍕")
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
else:
    col1, col2 = st.columns(2)
    with col1:
        st.page_link("pages/01_login.py",   label="🔐 Login",    use_container_width=True)
    with col2:
        st.page_link("pages/02_register.py", label="📝 Cadastro", use_container_width=True)

st.divider()
st.markdown("""
**KanBite** é um sistema de gestão de tarefas baseado no método Kanban,
desenvolvido para restaurantes italianos.

| Funcionalidade | Descrição |
|---|---|
| 📋 Quadro Kanban | Organize tarefas em A FAZER → FAZENDO → FEITO |
| 🔄 WIP Limit | Controle quantas tarefas podem estar em andamento simultaneamente |
| 🏊 Swimlanes | Agrupe tarefas por categoria ou responsável |
| 📊 Métricas | Acompanhe Cycle Time, Lead Time, Throughput e WIP |
| 🔐 Autenticação | Cada usuário acessa apenas seus próprios quadros |
""")