"""
database/base.py - Base declarativa SQLAlchemy + inicializacao do schema
Dev 3 - Sprint 1, Dia 8
"""
from sqlalchemy.orm import DeclarativeBase
from database.engine import get_engine


class Base(DeclarativeBase):
    pass


def criar_tabelas() -> None:
    try:
        from models import user, board, swimlane, card  # noqa: F401
    except ImportError as e:
        print(f"[AVISO] Alguns models ainda nao existem: {e}")
    Base.metadata.create_all(get_engine())
    print("Tabelas criadas com sucesso.")


def dropar_tabelas() -> None:
    Base.metadata.drop_all(get_engine())
    print("Todas as tabelas foram removidas.")


if __name__ == "__main__":
    criar_tabelas()
