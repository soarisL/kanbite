"""
services/metrics_service.py - Metricas Kanban
Dev 3 - Sprint 3
"""
from datetime import datetime
from sqlalchemy.orm import Session
from models.card import Card, Coluna


def calcular_cycle_time(session: Session, board_id: int) -> float | None:
    cards = (session.query(Card)
             .filter(
                 Card.board_id == board_id,
                 Card.started_at.isnot(None),
                 Card.finished_at.isnot(None),
             ).all())
    if not cards:
        return None
    deltas = [(c.finished_at - c.started_at).total_seconds() / 86400 for c in cards]
    return round(sum(deltas) / len(deltas), 2)


def calcular_lead_time(session: Session, board_id: int) -> float | None:
    cards = (session.query(Card)
             .filter(
                 Card.board_id == board_id,
                 Card.finished_at.isnot(None),
             ).all())
    if not cards:
        return None
    deltas = [(c.finished_at - c.created_at).total_seconds() / 86400 for c in cards]
    return round(sum(deltas) / len(deltas), 2)


def calcular_throughput(session: Session, board_id: int) -> int:
    return (session.query(Card)
            .filter(
                Card.board_id == board_id,
                Card.column == Coluna.FEITO,
            ).count())


def calcular_wip(session: Session, board_id: int) -> int:
    return (session.query(Card)
            .filter(
                Card.board_id == board_id,
                Card.column == Coluna.FAZENDO,
            ).count())


def cards_por_coluna(session: Session, board_id: int) -> dict[str, int]:
    resultado = {}
    for coluna in Coluna:
        count = (session.query(Card)
                 .filter(
                     Card.board_id == board_id,
                     Card.column == coluna,
                 ).count())
        resultado[coluna.value] = count
    return resultado


def resumo_metricas(session: Session, board_id: int) -> dict:
    return {
        "cycle_time_dias": calcular_cycle_time(session, board_id),
        "lead_time_dias":  calcular_lead_time(session, board_id),
        "throughput":      calcular_throughput(session, board_id),
        "wip_atual":       calcular_wip(session, board_id),
        "por_coluna":      cards_por_coluna(session, board_id),
    }