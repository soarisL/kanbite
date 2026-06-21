"""
database/repos/board_repo.py - Repositorio de Board (CRUD)
Dev 2 - Sprint 3

Responsabilidade: acesso a dados da tabela 'boards'.
Todas as operacoes usam flush() ao inves de commit() para que
a camada de servico controle as transacoes.
"""
from sqlalchemy.orm import Session
from models.board import Board


class BoardRepo:
    """Repositorio responsavel pelo CRUD de quadros Kanban."""

    def __init__(self, session: Session):
        self.session = session

    # ── CREATE ──────────────────────────────────────────────────────────────

    def criar(self, owner_id: int, name: str,
              wip_todo: int = 0, wip_doing: int = 3) -> Board:
        """
        Cria um novo Board e persiste na sessao.
        Nao faz commit — a transacao fica aberta para o chamador encerrar.
        """
        board = Board(
            owner_id=owner_id,
            name=name,
            wip_todo=wip_todo,
            wip_doing=wip_doing,
        )
        self.session.add(board)
        self.session.flush()   # gera o ID sem commitar
        return board

    # ── READ ────────────────────────────────────────────────────────────────

    def buscar_por_id(self, board_id: int) -> Board | None:
        """Retorna o Board com o ID informado, ou None se nao existir."""
        return self.session.get(Board, board_id)

    def listar_por_usuario(self, user_id: int) -> list[Board]:
        """Retorna todos os boards de um usuario, ordenados por data de criacao."""
        return (self.session.query(Board)
                .filter(Board.owner_id == user_id)
                .order_by(Board.created_at)
                .all())

    def existe(self, board_id: int) -> bool:
        """Verifica se um board com o ID existe."""
        return self.buscar_por_id(board_id) is not None

    # ── UPDATE ──────────────────────────────────────────────────────────────

    def atualizar_nome(self, board_id: int, novo_nome: str) -> Board | None:
        """
        Atualiza o nome de um Board.
        Retorna o Board atualizado, ou None se nao encontrado.
        """
        board = self.buscar_por_id(board_id)
        if not board:
            return None
        board.name = novo_nome
        self.session.flush()
        return board

    def atualizar_wip(self, board_id: int, wip_doing: int) -> Board | None:
        """
        Atualiza o WIP limit da coluna FAZENDO.
        wip_doing = 0 significa sem limite.
        """
        board = self.buscar_por_id(board_id)
        if not board:
            return None
        board.wip_doing = wip_doing
        self.session.flush()
        return board

    # ── DELETE ──────────────────────────────────────────────────────────────

    def deletar(self, board_id: int) -> bool:
        """
        Remove um Board e todos os seus cards/swimlanes (cascade no model).
        Retorna True se deletou, False se nao encontrou.
        """
        board = self.buscar_por_id(board_id)
        if not board:
            return False
        self.session.delete(board)
        self.session.flush()
        return True