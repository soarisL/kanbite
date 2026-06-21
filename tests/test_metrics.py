"""
tests/test_metrics.py - Testes das metricas Kanban
Dev 1 - Sprint 3
"""
import pytest
from services.auth_service import registrar
from services.kanban_service import criar_board, criar_card, mover_card
from services.metrics_service import (
    calcular_throughput, calcular_wip,
    calcular_cycle_time, calcular_lead_time, resumo_metricas,
)
from models.card import Coluna


class TestThroughput:
    def test_throughput_inicial_zero(self, db_session):
        user  = registrar(db_session, "met1", "met1@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board Metrics 1")
        assert calcular_throughput(db_session, board.id) == 0

    def test_throughput_aumenta_ao_concluir(self, db_session):
        user  = registrar(db_session, "met2", "met2@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board Metrics 2", wip_doing=5)
        card  = criar_card(db_session, board.id, "Tarefa", "Dev")
        mover_card(db_session, card.id, Coluna.FAZENDO)
        mover_card(db_session, card.id, Coluna.FEITO)
        assert calcular_throughput(db_session, board.id) == 1


class TestWip:
    def test_wip_zero_inicialmente(self, db_session):
        user  = registrar(db_session, "wip1", "wip1@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board WIP 1")
        assert calcular_wip(db_session, board.id) == 0

    def test_wip_aumenta_ao_mover_para_fazendo(self, db_session):
        user  = registrar(db_session, "wip2", "wip2@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board WIP 2", wip_doing=5)
        card  = criar_card(db_session, board.id, "Tarefa", "Dev")
        mover_card(db_session, card.id, Coluna.FAZENDO)
        assert calcular_wip(db_session, board.id) == 1

    def test_wip_diminui_ao_concluir(self, db_session):
        user  = registrar(db_session, "wip3", "wip3@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board WIP 3", wip_doing=5)
        card  = criar_card(db_session, board.id, "Tarefa", "Dev")
        mover_card(db_session, card.id, Coluna.FAZENDO)
        mover_card(db_session, card.id, Coluna.FEITO)
        assert calcular_wip(db_session, board.id) == 0


class TestCycleLeadTime:
    def test_cycle_time_none_sem_dados(self, db_session):
        user  = registrar(db_session, "ct1", "ct1@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board CT")
        assert calcular_cycle_time(db_session, board.id) is None

    def test_lead_time_none_sem_concluidos(self, db_session):
        user  = registrar(db_session, "lt1", "lt1@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board LT")
        assert calcular_lead_time(db_session, board.id) is None

    def test_resumo_retorna_todas_metricas(self, db_session):
        user  = registrar(db_session, "res1", "res1@k.com", "senha123")
        board = criar_board(db_session, user.id, "Board Resumo", wip_doing=5)
        resumo = resumo_metricas(db_session, board.id)
        assert "cycle_time_dias" in resumo
        assert "lead_time_dias"  in resumo
        assert "throughput"      in resumo
        assert "wip_atual"       in resumo
        assert "por_coluna"      in resumo