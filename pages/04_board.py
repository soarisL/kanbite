"""
pages/04_board.py - Quadro Kanban Visual
Dev 4 - Sprint 3
"""
import streamlit as st
from database.engine import get_session
from services.kanban_service import (
    listar_boards, criar_board,
    listar_cards, criar_card, atualizar_card, deletar_card,
    mover_card, mover_swimlane,
    listar_swimlanes, criar_swimlane,
    WipLimitError, CardNaoEncontradoError,
)
from models.card import Coluna

# ── Autenticação ──────────────────────────────────────────────────────────────
if "user_id" not in st.session_state:
    st.warning("⚠️ Você precisa fazer login para acessar o quadro.")
    st.page_link("pages/01_login.py", label="Ir para o Login →")
    st.stop()

st.set_page_config(page_title="Quadro — KanBite", page_icon="📋", layout="wide")
st.title("📋 Quadro Kanban")

session  = get_session()
user_id  = st.session_state["user_id"]
boards   = listar_boards(session, user_id)

# ── Criar board se não existir ────────────────────────────────────────────────
if not boards:
    st.info("Você ainda não tem nenhum quadro. Crie o primeiro!")
    with st.form("form_criar_board"):
        nome_board = st.text_input("Nome do quadro", placeholder="ex: Cozinha da Nonna")
        wip_limit  = st.number_input("WIP Limit (máx. cartões em FAZENDO)", min_value=1, max_value=20, value=3)
        if st.form_submit_button("🆕 Criar Quadro", use_container_width=True):
            criar_board(session, user_id, nome_board, wip_doing=int(wip_limit))
            st.success("Quadro criado!")
            st.rerun()
    st.stop()

# ── Selecionar board ──────────────────────────────────────────────────────────
nomes_boards = {b.id: b.name for b in boards}
board_id_sel = st.selectbox("Quadro:", options=list(nomes_boards.keys()),
                             format_func=lambda x: nomes_boards[x])
board = next(b for b in boards if b.id == board_id_sel)

st.caption(f"WIP Limit (FAZENDO): **{board.wip_doing}** cartões")
st.divider()

# ── Colunas do Kanban ─────────────────────────────────────────────────────────
COLUNAS    = [Coluna.A_FAZER, Coluna.FAZENDO, Coluna.FEITO]
EMOJIS     = {Coluna.A_FAZER: "📌", Coluna.FAZENDO: "🔄", Coluna.FEITO: "✅"}
PRIORIDADE_COR = {"baixa": "🟢", "media": "🟡", "alta": "🔴"}

col1, col2, col3 = st.columns(3)
colunas_ui = {Coluna.A_FAZER: col1, Coluna.FAZENDO: col2, Coluna.FEITO: col3}

for coluna_enum, col_ui in colunas_ui.items():
    cards_col = listar_cards(session, board.id, coluna_enum)
    with col_ui:
        st.markdown(f"### {EMOJIS[coluna_enum]} {coluna_enum.value} ({len(cards_col)})")
        st.divider()

        for card in cards_col:
            cor = PRIORIDADE_COR.get(card.priority.value, "⚪")
            with st.expander(f"{cor} **{card.title}**", expanded=False):
                st.write(f"👤 **Responsável:** {card.responsible}")
                st.write(f"🎯 **Prioridade:** {card.priority.value.capitalize()}")
                if card.description:
                    st.write(f"📝 **Descrição:** {card.description}")
                if card.due_date:
                    st.write(f"📅 **Prazo:** {card.due_date.strftime('%d/%m/%Y')}")

                # Botões de mover
                outras_colunas = [c for c in COLUNAS if c != coluna_enum]
                btn_cols = st.columns(len(outras_colunas))
                for i, prox_col in enumerate(outras_colunas):
                    with btn_cols[i]:
                        label = f"→ {prox_col.value}"
                        if st.button(label, key=f"mv_{card.id}_{prox_col.value}"):
                            try:
                                mover_card(session, card.id, prox_col)
                                st.success(f"Movido para {prox_col.value}!")
                                st.rerun()
                            except WipLimitError as e:
                                st.error(str(e))

                # Botão deletar
                if st.button("🗑️ Excluir", key=f"del_{card.id}"):
                    deletar_card(session, card.id)
                    st.rerun()

# ── Formulário: Novo cartão ───────────────────────────────────────────────────
st.divider()
with st.expander("➕ Adicionar novo cartão"):
    with st.form("form_novo_card", clear_on_submit=True):
        titulo    = st.text_input("Título *", placeholder="ex: Preparar Carbonara")
        resp      = st.text_input("Responsável *", placeholder="ex: Chef Mario")
        prioridade = st.selectbox("Prioridade", ["baixa", "media", "alta"], index=1)
        descricao = st.text_area("Descrição", placeholder="Detalhes da tarefa...")
        prazo     = st.date_input("Prazo (opcional)", value=None)
        criar_ok  = st.form_submit_button("Criar Cartão", use_container_width=True)

    if criar_ok:
        if not titulo or not resp:
            st.error("Título e responsável são obrigatórios.")
        else:
            from datetime import datetime as dt
            due = dt.combine(prazo, dt.min.time()) if prazo else None
            criar_card(session, board.id, titulo, resp,
                       priority=prioridade, description=descricao, due_date=due)
            st.success(f"✅ Cartão '{titulo}' criado em A FAZER!")
            st.rerun()