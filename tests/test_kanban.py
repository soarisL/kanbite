"""
tests/test_kanban.py - Testes do nucleo Kanban
Dev 2 - Sprint 1 (estrutura) / Sprint 3 (completo)
"""
import pytest

try:
    from services.kanban_service import criar_board, listar_boards, criar_card, mover_card
    from models.card import Coluna
    MODULES_READY = True
except ImportError:
    MODULES_READY = False


@pytest.mark.skipif(not MODULES_READY, reason="kanban_service nao implementado")
class TestBoard:
    def test_criar_board(self, db_session, sample_board_data):
        board = criar_board(db_session, owner_id=1, **sample_board_data)
        assert board.id is not None

    def test_listar_boards_usuario(self, db_session):
        criar_board(db_session, owner_id=1, name="Board A", wip_todo=5, wip_doing=3)
        boards = listar_boards(db_session, user_id=1)
        assert all(b.owner_id == 1 for b in boards)


@pytest.mark.skipif(not MODULES_READY, reason="kanban_service nao implementado")
class TestCard:
    def test_criar_card(self, db_session):
        board = criar_board(db_session, owner_id=1, name="Board Card", wip_todo=5, wip_doing=3)
        card = criar_card(db_session, board_id=board.id, title="Preparar Carbonara", responsible="Chef Mario")
        assert card.column == Coluna.A_FAZER
        assert card.started_at is None

    def test_mover_para_fazendo(self, db_session):
        board = criar_board(db_session, owner_id=1, name="Board Mover", wip_todo=5, wip_doing=3)
        card = criar_card(db_session, board_id=board.id, title="Teste", responsible="Dev")
        card = mover_card(db_session, card.id, Coluna.FAZENDO)
        assert card.started_at is not None
