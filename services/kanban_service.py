"""
services/kanban_service.py - Servico Kanban
Dev 1 - Sprint 3
"""
from datetime import datetime
from sqlalchemy.orm import Session
from models.board import Board
from models.card import Card, Coluna
from models.swimlane import Swimlane


# ─────────────────────────────────────────
#  BOARDS
# ─────────────────────────────────────────

def criar_board(session: Session, owner_id: int, name: str,
                wip_todo: int = 0, wip_doing: int = 3) -> Board:
    board = Board(owner_id=owner_id, name=name, wip_todo=wip_todo, wip_doing=wip_doing)
    session.add(board)
    session.commit()
    session.refresh(board)
    return board


def listar_boards(session: Session, user_id: int) -> list[Board]:
    return session.query(Board).filter(Board.owner_id == user_id).all()


def buscar_board(session: Session, board_id: int) -> Board | None:
    return session.get(Board, board_id)


def atualizar_board(session: Session, board_id: int,
                    name: str | None = None,
                    wip_doing: int | None = None) -> Board | None:
    board = session.get(Board, board_id)
    if not board:
        return None
    if name is not None:
        board.name = name
    if wip_doing is not None:
        board.wip_doing = wip_doing
    session.commit()
    session.refresh(board)
    return board


def deletar_board(session: Session, board_id: int) -> bool:
    board = session.get(Board, board_id)
    if board:
        session.delete(board)
        session.commit()
        return True
    return False


# ─────────────────────────────────────────
#  SWIMLANES
# ─────────────────────────────────────────

def criar_swimlane(session: Session, board_id: int,
                   name: str, position: int = 0) -> Swimlane:
    swimlane = Swimlane(board_id=board_id, name=name, position=position)
    session.add(swimlane)
    session.commit()
    session.refresh(swimlane)
    return swimlane


def listar_swimlanes(session: Session, board_id: int) -> list[Swimlane]:
    return (session.query(Swimlane)
            .filter(Swimlane.board_id == board_id)
            .order_by(Swimlane.position)
            .all())


def deletar_swimlane(session: Session, swimlane_id: int) -> bool:
    swimlane = session.get(Swimlane, swimlane_id)
    if swimlane:
        session.delete(swimlane)
        session.commit()
        return True
    return False