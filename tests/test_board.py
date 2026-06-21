import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base
from database.repos.board_repo import BoardRepo
from models.user import User


# CONFIGURAÇÃO DO BANCO DE TESTE
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)
    
    from models.user import User
    from models.board import Board
    from models.swimlane import Swimlane
    from models.card import Card

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    yield session
    session.close()


# USUÁRIO FAKE
@pytest.fixture
def test_user(db_session):
    unique_id = str(uuid.uuid4())[:8]

    user = User(
        username=f"Gustavo_{unique_id}",
        email=f"gustavo_{unique_id}@email.com",
        hashed_password="123456"
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user


# CREATE BOARD
def test_create_board(db_session, test_user):
    repo = BoardRepo(db_session)

    board = repo.criar(
        name="Meu Kanban",
        owner_id=test_user.id
    )

    assert board.id is not None
    assert board.name == "Meu Kanban"
    assert board.owner_id == test_user.id
    assert board.wip_todo == 0
    assert board.wip_doing == 3


# BUSCAR POR ID
def test_get_board_by_id(db_session, test_user):
    repo = BoardRepo(db_session)

    created = repo.criar(
        name="Projeto XPTO",
        owner_id=test_user.id
    )

    board = repo.buscar_por_id(created.id)

    assert board is not None
    assert board.name == "Projeto XPTO"


# BUSCAR POR USUÁRIO
def test_get_board_by_owner(db_session, test_user):
    repo = BoardRepo(db_session)

    repo.criar(name="Board 1", owner_id=test_user.id)
    repo.criar(name="Board 2", owner_id=test_user.id)

    boards = repo.listar_por_usuario(test_user.id)

    assert len(boards) == 2


# ATUALIZAR NOME
def test_update_board_name(db_session, test_user):
    repo = BoardRepo(db_session)

    board = repo.criar(
        name="Antigo Nome",
        owner_id=test_user.id
    )

    updated = repo.atualizar_nome(board.id, "Novo Nome")

    assert updated.name == "Novo Nome"


# DELETAR BOARD
def test_delete_board(db_session, test_user):
    repo = BoardRepo(db_session)

    board = repo.criar(
        name="Excluir",
        owner_id=test_user.id
    )

    result = repo.deletar(board.id)

    assert result is True
    assert repo.buscar_por_id(board.id) is None


# DELETAR INEXISTENTE
def test_delete_nonexistent_board(db_session):
    repo = BoardRepo(db_session)

    result = repo.deletar(999)

    assert result is False