"""
conftest.py - Configuracao global do pytest
Dev 5 - Sprint 1, Dia 1
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from database.base import Base
except ImportError:
    Base = None


@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    if Base is not None:
        Base.metadata.create_all(engine)
    yield engine
    if Base is not None:
        Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def db_session(test_engine):
    Session = sessionmaker(bind=test_engine)
    session = Session()
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def sample_user_data():
    return {"username": "testuser", "email": "test@kanbite.com", "password": "senha_segura_123"}


@pytest.fixture
def sample_board_data():
    return {"name": "Cozinha Principal", "wip_todo": 10, "wip_doing": 3}
