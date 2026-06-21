"""
models/swimlane.py - Modelo de Swimlane
Dev 2 - Sprint 1, Dia 8
"""
from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base


class Swimlane(Base):
    __tablename__ = "swimlanes"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    board_id: Mapped[int] = mapped_column(ForeignKey("boards.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    position: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    board: Mapped["Board"] = relationship("Board", back_populates="swimlanes")  # noqa: F821
    cards: Mapped[list["Card"]] = relationship(  # noqa: F821
        "Card", back_populates="swimlane", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Swimlane id={self.id} name={self.name!r} pos={self.position}>"
