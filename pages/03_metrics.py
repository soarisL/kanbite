"""
pages/03_metrics.py - Dashboard de Metricas Kanban
Dev 4 - Sprint 3
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from database.engine import get_session
from services.kanban_service import listar_boards
from services.metrics_service import resumo_metricas, cards_por_coluna

if "user_id" not in st.session_state:
    st.warning("⚠️ Você precisa fazer login.")
    st.page_link("pages/01_login.py", label="Ir para o Login →")
    st.stop()

st.set_page_config(page_title="Métricas — KanBite", page_icon="📊", layout="wide")
st.title("📊 Métricas do Projeto")

session = get_session()
boards  = listar_boards(session, st.session_state["user_id"])

if not boards:
    st.info("Crie um quadro primeiro para visualizar as métricas.")
    st.stop()

nomes = {b.id: b.name for b in boards}
board_id = st.selectbox("Quadro:", options=list(nomes.keys()),
                         format_func=lambda x: nomes[x])

metricas = resumo_metricas(session, board_id)
st.divider()

# ── KPIs ──────────────────────────────────────────────────────────────────────
k1, k2, k3, k4 = st.columns(4)

ct = metricas["cycle_time_dias"]
lt = metricas["lead_time_dias"]

k1.metric("⏱ Cycle Time",  f"{ct} dias" if ct else "Sem dados",
          help="Tempo médio de FAZENDO → FEITO")
k2.metric("🗓 Lead Time",   f"{lt} dias" if lt else "Sem dados",
          help="Tempo médio de criação → FEITO")
k3.metric("✅ Throughput",  metricas["throughput"],
          help="Total de cartões concluídos")
k4.metric("🔄 WIP Atual",   metricas["wip_atual"],
          help="Cartões em FAZENDO agora")

st.divider()

# ── Gráfico de distribuição ────────────────────────────────────────────────────
por_coluna = metricas["por_coluna"]
fig_bar = go.Figure(go.Bar(
    x=list(por_coluna.keys()),
    y=list(por_coluna.values()),
    marker_color=["#4e9af1", "#f0a500", "#28a745"],
    text=list(por_coluna.values()),
    textposition="outside",
))
fig_bar.update_layout(
    title="Distribuição de Cartões por Coluna",
    xaxis_title="Coluna",
    yaxis_title="Quantidade de Cartões",
    showlegend=False,
    plot_bgcolor="rgba(0,0,0,0)",
)
st.plotly_chart(fig_bar, use_container_width=True)

# ── Gráfico de pizza ──────────────────────────────────────────────────────────
total = sum(por_coluna.values())
if total > 0:
    fig_pie = px.pie(
        names=list(por_coluna.keys()),
        values=list(por_coluna.values()),
        title="Proporção de Cartões",
        color_discrete_sequence=["#4e9af1", "#f0a500", "#28a745"],
    )
    st.plotly_chart(fig_pie, use_container_width=True)
else:
    st.info("Nenhum cartão criado ainda. Adicione cartões no quadro para ver métricas.")