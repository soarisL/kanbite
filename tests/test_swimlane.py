# tests/test_swimlane.py

import pytest
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base
from database.repos.board_repo import BoardRepository
from database.repos.swimlane_repo import SwimlaneRepository

from models.user import User
from models.board import Board
from models.swimlane import Swimlane
from models.card import Card

# BANCO TEMPORÁRIO
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    yield session
    session.close()

# USUÁRIO FAKE
@pytest.fixture
def test_user(db_session):
    unique_id = str(uuid.uuid4())[:8]

    user = User(
        username=f"user_{unique_id}",
        email=f"{unique_id}@email.com",
        hashed_password="123456"
    )

    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    return user

# BOARD FAKE
@pytest.fixture
def test_board(db_session, test_user):
    repo = BoardRepository(db_session)

    board = repo.create_board(
        name="Projeto Swimlane",
        owner_id=test_user.id
    )

    return board

# TESTE CREATE
def test_create_swimlane(db_session, test_board):
    repo = SwimlaneRepository(db_session)

    lane = repo.create_swimlane(
        board_id=test_board.id,
        name="Backend",
        position=1
    )

    assert lane.id is not None
    assert lane.name == "Backend"
    assert lane.position == 1

# TESTE GET BY ID
def test_get_swimlane_by_id(db_session, test_board):
    repo = SwimlaneRepository(db_session)

    created = repo.create_swimlane(
        board_id=test_board.id,
        name="Frontend"
    )

    lane = repo.get_by_id(created.id)

    assert lane is not None
    assert lane.name == "Frontend"

# TESTE LISTAR POR BOARD
def test_get_swimlanes_by_board(db_session, test_board):
    repo = SwimlaneRepository(db_session)

    repo.create_swimlane(
        board_id=test_board.id,
        name="UX",
        position=1
    )

    repo.create_swimlane(
        board_id=test_board.id,
        name="QA",
        position=2
    )

    lanes = repo.get_by_board(test_board.id)

    assert len(lanes) == 2

# UPDATE NAME
def test_update_swimlane_name(db_session, test_board):
    repo = SwimlaneRepository(db_session)

    lane = repo.create_swimlane(
        board_id=test_board.id,
        name="Antigo Nome"
    )

    updated = repo.update_name(
        lane.id,
        "Novo Nome"
    )

    assert updated.name == "Novo Nome"

# UPDATE POSITION
def test_update_swimlane_position(db_session, test_board):
    repo = SwimlaneRepository(db_session)

    lane = repo.create_swimlane(
        board_id=test_board.id,
        name="DevOps",
        position=1
    )

    updated = repo.update_position(
        lane.id,
        5
    )

    assert updated.position == 5

# TESTE DELETE
def test_delete_swimlane(db_session, test_board):
    repo = SwimlaneRepository(db_session)

    lane = repo.create_swimlane(
        board_id=test_board.id,
        name="Excluir"
    )

    result = repo.delete_swimlane(lane.id)

    assert result is True
    assert repo.get_by_id(lane.id) is None

# DELETE INEXISTENTE
def test_delete_nonexistent_swimlane(db_session):
    repo = SwimlaneRepository(db_session)

    result = repo.delete_swimlane(999)

    assert result is False