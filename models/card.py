"""
models/card.py - Modelo de Cartao Kanban com todos os campos obrigatorios
Dev 2 - Sprint 1, Dia 8
"""
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, Text, DateTime, Enum, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base


class Coluna(str, PyEnum):
    A_FAZER = "A FAZER"
    FAZENDO = "FAZENDO"
    FEITO   = "FEITO"


class Prioridade(str, PyEnum):
    BAIXA = "baixa"
    MEDIA = "media"
    ALTA  = "alta"


class Card(Base):
    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"), nullable=False)
    swimlane_id: Mapped[int | None] = mapped_column(ForeignKey("swimlanes.id"), nullable=True)

    title: Mapped[str] = mapped_column(String(200), nullable=False)
    responsible: Mapped[str] = mapped_column(String(100), nullable=False)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    priority: Mapped[Prioridade] = mapped_column(Enum(Prioridade), default=Prioridade.MEDIA, nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    column: Mapped[Coluna] = mapped_column(Enum(Coluna), default=Coluna.A_FAZER, nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    board: Mapped["Board"] = relationship("Board", back_populates="cards")  # noqa: F821
    swimlane: Mapped["Swimlane | None"] = relationship("Swimlane", back_populates="cards")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Card id={self.id} title={self.title!r} column={self.column.value}>"
