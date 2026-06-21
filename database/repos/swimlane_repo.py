
"""
database/repos/swimlane_repo.py - Repositorio de Swimlane (CRUD)
Dev 2 - Sprint 3

Responsabilidade: acesso a dados da tabela 'swimlanes'.
Swimlanes sao raias horizontais do quadro Kanban que permitem
agrupar cards por categoria, responsavel ou qualquer criterio.
"""

from sqlalchemy.orm import Session
from models.swimlane import Swimlane


class SwimlaneRepo:
    """Repositorio responsavel pelo CRUD de swimlanes (raias)."""

    def __init__(self, session: Session):
        self.session = session

    # ── CREATE ──────────────────────────────────────────────────────────────

    def criar(self, board_id: int, name: str, position: int = 0) -> Swimlane:
        """
        Cria uma nova swimlane em um board.
        position define a ordem de exibicao (0 = primeira).
        """
        swimlane = Swimlane(
            board_id=board_id,
            name=name,
            position=position,
        )
        self.session.add(swimlane)
        self.session.flush()
        return swimlane

    # ── READ ────────────────────────────────────────────────────────────────

    def buscar_por_id(self, swimlane_id: int) -> Swimlane | None:
        """Retorna a Swimlane com o ID informado, ou None."""
        return self.session.get(Swimlane, swimlane_id)

    def listar_por_board(self, board_id: int) -> list[Swimlane]:
        """
        Retorna todas as swimlanes de um board,
        ordenadas por position (crescente).
        """
        return (self.session.query(Swimlane)
                .filter(Swimlane.board_id == board_id)
                .order_by(Swimlane.position)
                .all())

    # ── UPDATE ──────────────────────────────────────────────────────────────

    def atualizar_nome(self, swimlane_id: int, novo_nome: str) -> Swimlane | None:
        """Atualiza o nome de uma swimlane."""
        swimlane = self.buscar_por_id(swimlane_id)
        if not swimlane:
            return None
        swimlane.name = novo_nome
        self.session.flush()
        return swimlane

    def atualizar_posicao(self, swimlane_id: int,
                          nova_posicao: int) -> Swimlane | None:
        """Atualiza a posicao de ordenacao de uma swimlane."""
        swimlane = self.buscar_por_id(swimlane_id)
        if not swimlane:
            return None
        swimlane.position = nova_posicao
        self.session.flush()
        return swimlane

    # ── DELETE ──────────────────────────────────────────────────────────────

    def deletar(self, swimlane_id: int) -> bool:
        """
        Remove uma swimlane e todos os seus cards (cascade no model).
        Retorna True se deletou, False se nao encontrou.
        """
        swimlane = self.buscar_por_id(swimlane_id)
        if not swimlane:
            return False
        self.session.delete(swimlane)
        self.session.flush()
        return True
