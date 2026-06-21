"""
database/repos/card_repo.py - Repositorio de Card (CRUD + movimentacao)
Dev 2 - Sprint 3

Responsabilidade: acesso a dados da tabela 'cards'.
Esta camada NAO implementa regras de negocio como WIP limit —
essas ficam no kanban_service. O repo apenas persiste os dados.
"""
from datetime import datetime
from sqlalchemy.orm import Session
from models.card import Card, Coluna, Prioridade


class CardRepo:
    """Repositorio responsavel pelo CRUD de cartoes Kanban."""

    def __init__(self, session: Session):
        self.session = session

    # ── CREATE ──────────────────────────────────────────────────────────────

    def criar(self, board_id: int, title: str, responsible: str,
              swimlane_id: int | None = None,
              priority: str = "media",
              description: str | None = None,
              due_date: datetime | None = None) -> Card:
        """
        Cria um novo cartao de atividade na coluna A FAZER.
        O card nasce sempre em A FAZER — mover e responsabilidade do service.
        """
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
        self.session.add(card)
        self.session.flush()
        return card

    # ── READ ────────────────────────────────────────────────────────────────

    def buscar_por_id(self, card_id: int) -> Card | None:
        """Retorna o Card com o ID informado, ou None."""
        return self.session.get(Card, card_id)

    def listar_por_board(self, board_id: int,
                          coluna: Coluna | None = None) -> list[Card]:
        """
        Lista todos os cards de um board.
        Se coluna for informada, filtra apenas cards dessa coluna.
        Ordenado por position e depois por id.
        """
        q = self.session.query(Card).filter(Card.board_id == board_id)
        if coluna is not None:
            q = q.filter(Card.column == coluna)
        return q.order_by(Card.position, Card.id).all()

    def listar_por_swimlane(self, swimlane_id: int) -> list[Card]:
        """Lista todos os cards de uma swimlane especifica."""
        return (self.session.query(Card)
                .filter(Card.swimlane_id == swimlane_id)
                .order_by(Card.position)
                .all())

    def contar_por_coluna(self, board_id: int, coluna: Coluna) -> int:
        """
        Conta quantos cards existem em determinada coluna de um board.
        Usado pelo service para verificar WIP limit.
        """
        return (self.session.query(Card)
                .filter(
                    Card.board_id == board_id,
                    Card.column == coluna,
                ).count())

    # ── UPDATE ──────────────────────────────────────────────────────────────

    def atualizar(self, card_id: int,
                  title: str | None = None,
                  responsible: str | None = None,
                  description: str | None = None,
                  priority: str | None = None,
                  due_date: datetime | None = None) -> Card | None:
        """
        Atualiza campos editaveis de um card.
        Apenas os campos nao-None serao atualizados.
        """
        card = self.buscar_por_id(card_id)
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
        self.session.flush()
        return card

    def mover_coluna(self, card_id: int, nova_coluna: Coluna) -> Card | None:
        """
        Move o card para uma nova coluna e registra os timestamps:
          - started_at: preenchido na primeira vez que vai para FAZENDO
          - finished_at: preenchido na primeira vez que vai para FEITO

        ATENCAO: esta funcao NAO verifica WIP limit.
        A verificacao de WIP limit e responsabilidade do kanban_service.
        """
        card = self.buscar_por_id(card_id)
        if not card:
            return None

        # Registrar inicio ao entrar em FAZENDO
        if nova_coluna == Coluna.FAZENDO and card.started_at is None:
            card.started_at = datetime.utcnow()

        # Registrar conclusao ao entrar em FEITO
        if nova_coluna == Coluna.FEITO and card.finished_at is None:
            card.finished_at = datetime.utcnow()
            # Garantir que started_at esteja preenchido
            if card.started_at is None:
                card.started_at = datetime.utcnow()

        card.column = nova_coluna
        self.session.flush()
        return card

    def mover_swimlane(self, card_id: int,
                       nova_swimlane_id: int | None) -> Card | None:
        """
        Move o card para outra swimlane.
        Passar None remove o card da swimlane atual.
        """
        card = self.buscar_por_id(card_id)
        if not card:
            return None
        card.swimlane_id = nova_swimlane_id
        self.session.flush()
        return card

    def atualizar_posicao(self, card_id: int, nova_posicao: int) -> Card | None:
        """Atualiza a posicao de ordenacao de um card dentro da coluna."""
        card = self.buscar_por_id(card_id)
        if not card:
            return None
        card.position = nova_posicao
        self.session.flush()
        return card

    # ── DELETE ──────────────────────────────────────────────────────────────

    def deletar(self, card_id: int) -> bool:
        """
        Remove permanentemente um card.
        Retorna True se deletou, False se nao encontrou.
        """
        card = self.buscar_por_id(card_id)
        if not card:
            return False
        self.session.delete(card)
        self.session.flush()
        return True
