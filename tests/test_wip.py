"""
tests/test_wip.py - Testes do WIP Limit
Dev 1 - Sprint 3
"""
import pytest
from services.auth_service import registrar
from services.kanban_service import criar_board, criar_card, mover_card, WipLimitError
from models.card import Coluna


class TestWipLimit:
    def test_wip_limit_bloqueia_ao_atingir(self, db_session):
        """Nao deve permitir mover card para FAZENDO quando WIP limit atingido."""
        user  = registrar(db_session, "wl1", "wl1@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board Limite 1", wip_doing=1)
        c1 = criar_card(db_session, board.id, "Card 1", "Dev")
        c2 = criar_card(db_session, board.id, "Card 2", "Dev")
        mover_card(db_session, c1.id, Coluna.FAZENDO)
        with pytest.raises(WipLimitError):
            mover_card(db_session, c2.id, Coluna.FAZENDO)

    def test_wip_limit_zero_nao_bloqueia(self, db_session):
        """WIP limit 0 significa sem limite."""
        user  = registrar(db_session, "wl2", "wl2@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board Sem Limite", wip_doing=0)
        for i in range(5):
            card = criar_card(db_session, board.id, f"Card {i}", "Dev")
            mover_card(db_session, card.id, Coluna.FAZENDO)  # nao deve levantar erro

    def test_wip_libera_apos_concluir(self, db_session):
        """Apos mover card para FEITO, nova vaga deve abrir."""
        user  = registrar(db_session, "wl3", "wl3@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board Libera", wip_doing=1)
        c1 = criar_card(db_session, board.id, "Card 1", "Dev")
        c2 = criar_card(db_session, board.id, "Card 2", "Dev")
        mover_card(db_session, c1.id, Coluna.FAZENDO)
        mover_card(db_session, c1.id, Coluna.FEITO)      # libera vaga
        mover_card(db_session, c2.id, Coluna.FAZENDO)    # agora deve funcionar
        assert c2.column == Coluna.FAZENDO

    def test_wip_limit_dois_permite_dois(self, db_session):
        """Com WIP limit 2, deve aceitar exatamente 2 cards em FAZENDO."""
        user  = registrar(db_session, "wl4", "wl4@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board Dois", wip_doing=2)
        c1 = criar_card(db_session, board.id, "Card 1", "Dev")
        c2 = criar_card(db_session, board.id, "Card 2", "Dev")
        c3 = criar_card(db_session, board.id, "Card 3", "Dev")
        mover_card(db_session, c1.id, Coluna.FAZENDO)
        mover_card(db_session, c2.id, Coluna.FAZENDO)
        with pytest.raises(WipLimitError):
            mover_card(db_session, c3.id, Coluna.FAZENDO)