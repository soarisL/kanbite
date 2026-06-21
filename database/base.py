"""
database/base.py - Base declarativa SQLAlchemy + inicializacao do schema
Dev 3 - Sprint 1, Dia 8
"""
from sqlalchemy.orm import DeclarativeBase
from database.engine import get_engine


class Base(DeclarativeBase):
    pass


def criar_tabelas() -> None:
    Base.metadata.create_all(get_engine())
    print("Tabelas criadas com sucesso.")


def dropar_tabelas() -> None:
    Base.metadata.drop_all(get_engine())
    print("Todas as tabelas foram removidas.")


# Importar o pacote 'models' AQUI EMBAIXO, depois que 'Base' ja esta
# totalmente definida acima. Isso garante que todas as classes de
# model (User, Board, Swimlane, Card) sejam registradas no mapper
# do SQLAlchemy assim que 'database.base' for importado por qualquer
# parte do programa -- independente de qual modulo importa primeiro.
#
# O import fica no final (e nao no topo do arquivo) de proposito:
# como models/*.py faz 'from database.base import Base', colocar
# este import no topo criaria um ciclo em que 'database.base' tenta
# se reimportar antes de terminar de definir 'Base'. Import no final
# evita o ciclo, pois 'Base' ja existe no momento em que os models
# pedem por ela de volta.
import models  # noqa: F401,E402


if __name__ == "__main__":
    criar_tabelas()
