"""
models/board.py - Modelo de Quadro Kanban
Dev 2 - Sprint 1, Dia 8
"""
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base


class Board(Base):
    __tablename__ = "boards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    wip_todo: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    wip_doing: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    owner: Mapped["User"] = relationship("User", back_populates="boards")  # noqa: F821
    swimlanes: Mapped[list["Swimlane"]] = relationship(  # noqa: F821
        "Swimlane", back_populates="board", cascade="all, delete-orphan",
        order_by="Swimlane.position"
    )
    cards: Mapped[list["Card"]] = relationship(  # noqa: F821
        "Card", back_populates="board", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Board id={self.id} name={self.name!r}>"
