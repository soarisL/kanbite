"""
services/kanban_service.py - Servico Kanban
Dev 1 - Sprint 4 (refatorado para usar os Repos)

Esta camada concentra as REGRAS DE NEGOCIO (ex: WIP limit) e delega
o acesso a dados para database/repos/*. As funcoes fazem commit()
no final porque representam uma unidade de trabalho completa.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from database.repos.board_repo import BoardRepo
from database.repos.card_repo import CardRepo
from database.repos.swimlane_repo import SwimlaneRepo
from models.board import Board
from models.card import Card, Coluna
from models.swimlane import Swimlane


# ─────────────────────────────────────────
#  EXCEÇÕES
# ─────────────────────────────────────────

class WipLimitError(Exception):
    pass


class CardNaoEncontradoError(Exception):
    pass


# ─────────────────────────────────────────
#  BOARDS
# ─────────────────────────────────────────

def criar_board(session: Session, owner_id: int, name: str,
                wip_todo: int = 0, wip_doing: int = 3) -> Board:
    board = BoardRepo(session).criar(owner_id, name, wip_todo=wip_todo, wip_doing=wip_doing)
    session.commit()
    session.refresh(board)
    return board


def listar_boards(session: Session, user_id: int) -> list[Board]:
    return BoardRepo(session).listar_por_usuario(user_id)


def buscar_board(session: Session, board_id: int) -> Board | None:
    return BoardRepo(session).buscar_por_id(board_id)


def atualizar_board(session: Session, board_id: int,
                    name: str | None = None,
                    wip_doing: int | None = None) -> Board | None:
    repo = BoardRepo(session)
    board = repo.buscar_por_id(board_id)
    if not board:
        return None
    if name is not None:
        repo.atualizar_nome(board_id, name)
    if wip_doing is not None:
        repo.atualizar_wip(board_id, wip_doing)
    session.commit()
    session.refresh(board)
    return board


def deletar_board(session: Session, board_id: int) -> bool:
    resultado = BoardRepo(session).deletar(board_id)
    session.commit()
    return resultado


# ─────────────────────────────────────────
#  SWIMLANES
# ─────────────────────────────────────────

def criar_swimlane(session: Session, board_id: int,
                   name: str, position: int = 0) -> Swimlane:
    swimlane = SwimlaneRepo(session).criar(board_id, name, position=position)
    session.commit()
    session.refresh(swimlane)
    return swimlane


def listar_swimlanes(session: Session, board_id: int) -> list[Swimlane]:
    return SwimlaneRepo(session).listar_por_board(board_id)


def deletar_swimlane(session: Session, swimlane_id: int) -> bool:
    resultado = SwimlaneRepo(session).deletar(swimlane_id)
    session.commit()
    return resultado


# ─────────────────────────────────────────
#  CARDS
# ─────────────────────────────────────────

def criar_card(session: Session, board_id: int, title: str,
               responsible: str, swimlane_id: int | None = None,
               priority: str = "media", description: str | None = None,
               due_date: datetime | None = None) -> Card:
    card = CardRepo(session).criar(
        board_id, title, responsible,
        swimlane_id=swimlane_id, priority=priority,
        description=description, due_date=due_date,
    )
    session.commit()
    session.refresh(card)
    return card


def listar_cards(session: Session, board_id: int,
                 coluna: Coluna | None = None) -> list[Card]:
    return CardRepo(session).listar_por_board(board_id, coluna=coluna)


def buscar_card(session: Session, card_id: int) -> Card | None:
    return CardRepo(session).buscar_por_id(card_id)


def atualizar_card(session: Session, card_id: int,
                   title: str | None = None,
                   responsible: str | None = None,
                   description: str | None = None,
                   priority: str | None = None,
                   due_date: datetime | None = None) -> Card | None:
    card = CardRepo(session).atualizar(
        card_id, title=title, responsible=responsible,
        description=description, priority=priority, due_date=due_date,
    )
    if not card:
        return None
    session.commit()
    session.refresh(card)
    return card


def mover_card(session: Session, card_id: int, nova_coluna: Coluna) -> Card:
    """
    Move um card para outra coluna.
    A regra de WIP limit fica aqui no service (e' regra de negocio).
    A persistencia e os timestamps ficam no CardRepo.mover_coluna.
    """
    card_repo = CardRepo(session)
    card = card_repo.buscar_por_id(card_id)
    if not card:
        raise CardNaoEncontradoError(f"Card {card_id} nao encontrado.")

    board = BoardRepo(session).buscar_por_id(card.board_id)

    if nova_coluna == Coluna.FAZENDO and board.wip_doing > 0:
        total_fazendo = card_repo.contar_por_coluna(card.board_id, Coluna.FAZENDO)
        if total_fazendo >= board.wip_doing:
            raise WipLimitError(
                f"WIP limit atingido: maximo {board.wip_doing} cartoes em FAZENDO. "
                f"Conclua um cartao antes de iniciar outro."
            )

    card_atualizado = card_repo.mover_coluna(card_id, nova_coluna)
    session.commit()
    session.refresh(card_atualizado)
    return card_atualizado


def mover_swimlane(session: Session, card_id: int,
                   nova_swimlane_id: int | None) -> Card:
    card = CardRepo(session).mover_swimlane(card_id, nova_swimlane_id)
    if not card:
        raise CardNaoEncontradoError(f"Card {card_id} nao encontrado.")
    session.commit()
    session.refresh(card)
    return card


def deletar_card(session: Session, card_id: int) -> bool:
    resultado = CardRepo(session).deletar(card_id)
    session.commit()
    return resultado
