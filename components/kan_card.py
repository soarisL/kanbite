"""
components/kan_card.py - Componente visual de cartao Kanban
Dev 4 - Sprint 3
"""
import streamlit as st
from models.card import Card

CORES_PRIORIDADE = {
    "baixa": "🟢",
    "media": "🟡",
    "alta":  "🔴",
}


def render_card(card: Card, show_actions: bool = False):
    """
    Renderiza um cartao Kanban de forma compacta.
    show_actions: se True, exibe botoes de acao.
    """
    icone = CORES_PRIORIDADE.get(card.priority.value, "⚪")
    prazo = card.due_date.strftime("%d/%m/%Y") if card.due_date else "—"

    st.markdown(f"""
    **{icone} {card.title}**
    👤 {card.responsible} · 📅 {prazo}
    """)

    if card.description:
        st.caption(card.description[:80] + ("..." if len(card.description or "") > 80 else ""))