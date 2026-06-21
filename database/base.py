"""
database/base.py - Base declarativa SQLAlchemy + inicializacao do schema
Dev 3 - Sprint 1, Dia 8
"""
from sqlalchemy.orm import DeclarativeBase
from database.engine import get_engine


class Base(DeclarativeBase):
    pass


# Importar TODOS os models aqui, no nivel do modulo, para que o
# SQLAlchemy registre as classes antes de qualquer mapper ser
# configurado. Sem isso, relationship() que referencia outra
# classe por string (ex: relationship("Board", ...)) falha com
# "expression Board failed to locate a name" caso essa classe
# ainda nao tenha sido importada em nenhum lugar do programa.
from models import user, board, swimlane, card  # noqa: F401,E402


def criar_tabelas() -> None:
    Base.metadata.create_all(get_engine())
    print("Tabelas criadas com sucesso.")


def dropar_tabelas() -> None:
    Base.metadata.drop_all(get_engine())
    print("Todas as tabelas foram removidas.")


if __name__ == "__main__":
    criar_tabelas()
