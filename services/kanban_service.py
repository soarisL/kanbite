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

# ─────────────────────────────────────────
#  EXCEÇÕES
# ─────────────────────────────────────────

class WipLimitError(Exception):
    pass


class CardNaoEncontradoError(Exception):
    pass


# ─────────────────────────────────────────
#  CARDS
# ─────────────────────────────────────────

def criar_card(session: Session, board_id: int, title: str,
               responsible: str, swimlane_id: int | None = None,
               priority: str = "media", description: str | None = None,
               due_date: datetime | None = None) -> Card:
    from models.card import Prioridade
    card = Card(
        board_id=board_id,
        swimlane_id=swimlane_id,
        title=title,
        responsible=responsible,
        priority=Prioridade(priority),
        description=description,
        due_date=due_date,
        column=Coluna.A_FAZER,
        position=0,
    )
    session.add(card)
    session.commit()
    session.refresh(card)
    return card


def listar_cards(session: Session, board_id: int,
                 coluna: Coluna | None = None) -> list[Card]:
    q = session.query(Card).filter(Card.board_id == board_id)
    if coluna is not None:
        q = q.filter(Card.column == coluna)
    return q.order_by(Card.position, Card.id).all()


def buscar_card(session: Session, card_id: int) -> Card | None:
    return session.get(Card, card_id)


def atualizar_card(session: Session, card_id: int,
                   title: str | None = None,
                   responsible: str | None = None,
                   description: str | None = None,
                   priority: str | None = None,
                   due_date: datetime | None = None) -> Card | None:
    from models.card import Prioridade
    card = session.get(Card, card_id)
    if not card:
        return None
    if title is not None:
        card.title = title
    if responsible is not None:
        card.responsible = responsible
    if description is not None:
        card.description = description
    if priority is not None:
        card.priority = Prioridade(priority)
    if due_date is not None:
        card.due_date = due_date
    session.commit()
    session.refresh(card)
    return card


def mover_card(session: Session, card_id: int, nova_coluna: Coluna) -> Card:
    card = session.get(Card, card_id)
    if not card:
        raise CardNaoEncontradoError(f"Card {card_id} nao encontrado.")

    board = session.get(Board, card.board_id)

    if nova_coluna == Coluna.FAZENDO and board.wip_doing > 0:
        total_fazendo = session.query(Card).filter(
            Card.board_id == card.board_id,
            Card.column == Coluna.FAZENDO,
        ).count()
        if total_fazendo >= board.wip_doing:
            raise WipLimitError(
                f"WIP limit atingido: maximo {board.wip_doing} cartoes em FAZENDO. "
                f"Conclua um cartao antes de iniciar outro."
            )

    if nova_coluna == Coluna.FAZENDO and card.started_at is None:
        card.started_at = datetime.utcnow()
    if nova_coluna == Coluna.FEITO and card.finished_at is None:
        card.finished_at = datetime.utcnow()
        if card.started_at is None:
            card.started_at = datetime.utcnow()

    card.column = nova_coluna
    session.commit()
    session.refresh(card)
    return card


def mover_swimlane(session: Session, card_id: int,
                   nova_swimlane_id: int | None) -> Card:
    card = session.get(Card, card_id)
    if not card:
        raise CardNaoEncontradoError(f"Card {card_id} nao encontrado.")
    card.swimlane_id = nova_swimlane_id
    session.commit()
    session.refresh(card)
    return card


def deletar_card(session: Session, card_id: int) -> bool:
    card = session.get(Card, card_id)
    if card:
        session.delete(card)
        session.commit()
        return True
    return False