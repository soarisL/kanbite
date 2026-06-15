from datetime import datetime
from sqlalchemy.orm import Session
from models.card import Card, Coluna, Prioridade


class CardRepository:

    def __init__(self, db: Session):
        self.db = db

    def create_card(
        self,
        board_id: int,
        title: str,
        responsible: str,
        swimlane_id: int | None = None,
        due_date: datetime | None = None,
        priority: Prioridade = Prioridade.MEDIA,
        description: str | None = None,
        column: Coluna = Coluna.A_FAZER,
        position: int = 0
    ) -> Card:

        card = Card(
            board_id=board_id,
            swimlane_id=swimlane_id,
            title=title,
            responsible=responsible,
            due_date=due_date,
            priority=priority,
            description=description,
            column=column,
            position=position
        )

        self.db.add(card)
        self.db.commit()
        self.db.refresh(card)

        return card
    
# ID:
    def get_by_id(self, card_id: int) -> Card | None:
        return self.db.query(Card).filter(Card.id == card_id).first()
    
# BOARD:
    def get_by_board(self, board_id: int) -> list[Card]:
        return self.db.query(Card).filter(Card.board_id == board_id).all()

# COLUNA:
    def get_by_column(self, board_id: int, column: Coluna) -> list[Card]:
        return (
            self.db.query(Card)
            .filter(Card.board_id == board_id, Card.column == column)
            .order_by(Card.position)
            .all()
        )
    
# TITLE:
    def update_title(self, card_id: int, new_title: str) -> Card | None:
        card = self.get_by_id(card_id)

        if not card:
            return None

        card.title = new_title
        self.db.commit()
        self.db.refresh(card)

        return card
    
# CARD:
    def move_card(
        self,
        card_id: int,
        new_column: Coluna,
        new_position: int
    ) -> Card | None:

        card = self.get_by_id(card_id)

        if not card:
            return None

        card.column = new_column
        card.position = new_position

        if new_column == Coluna.FAZENDO and card.started_at is None:
            card.started_at = datetime.utcnow()

        if new_column == Coluna.FEITO:
            card.finished_at = datetime.utcnow()

        self.db.commit()
        self.db.refresh(card)

        return card
    
# DELETE:
    def delete_card(self, card_id: int) -> bool:
        card = self.get_by_id(card_id)

        if not card:
            return False

        self.db.delete(card)
        self.db.commit()

        return True