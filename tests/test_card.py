import pytest
import uuid

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base
from database.repos.card_repo import CardRepository
from database.repos.board_repo import BoardRepository

from models.user import User
from models.board import Board
from models.swimlane import Swimlane
from models.card import Card, Coluna, Prioridade

# BANCO DE MEMÓRIA:
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    yield session
    session.close()

# FAKE:
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

@pytest.fixture
def test_board(db_session, test_user):
    repo = BoardRepository(db_session)

    board = repo.create_board(
        name="Projeto Teste",
        owner_id=test_user.id
    )

    return board

# CARD:
def test_create_card(db_session, test_board):
    repo = CardRepository(db_session)

    card = repo.create_card(
        board_id=test_board.id,
        title="Criar API",
        responsible="Gustavo"
    )

    assert card.id is not None
    assert card.title == "Criar API"
    assert card.column == Coluna.A_FAZER
    assert card.priority == Prioridade.MEDIA

# ID:
def test_get_card_by_id(db_session, test_board):
    repo = CardRepository(db_session)

    created = repo.create_card(
        board_id=test_board.id,
        title="Tela Login",
        responsible="Ana"
    )

    card = repo.get_by_id(created.id)

    assert card is not None
    assert card.title == "Tela Login"

# BOARD:
def test_get_cards_by_board(db_session, test_board):
    repo = CardRepository(db_session)

    repo.create_card(
        board_id=test_board.id,
        title="Task 1",
        responsible="A"
    )

    repo.create_card(
        board_id=test_board.id,
        title="Task 2",
        responsible="B"
    )

    cards = repo.get_by_board(test_board.id)

    assert len(cards) == 2

# TÍTULO:
def test_update_card_title(db_session, test_board):
    repo = CardRepository(db_session)

    card = repo.create_card(
        board_id=test_board.id,
        title="Antigo",
        responsible="Dev"
    )

    updated = repo.update_title(card.id, "Novo")

    assert updated.title == "Novo"

# MOVE CARD
def test_move_card(db_session, test_board):
    repo = CardRepository(db_session)

    card = repo.create_card(
        board_id=test_board.id,
        title="Mover Card",
        responsible="Dev"
    )

    moved = repo.move_card(
        card.id,
        Coluna.FAZENDO,
        1
    )

    assert moved.column == Coluna.FAZENDO
    assert moved.position == 1
    assert moved.started_at is not None

# DELETA:
def test_delete_card(db_session, test_board):
    repo = CardRepository(db_session)

    card = repo.create_card(
        board_id=test_board.id,
        title="Excluir",
        responsible="Dev"
    )

    result = repo.delete_card(card.id)

    assert result is True
    assert repo.get_by_id(card.id) is None

# INEXISTENTE:
def test_delete_nonexistent_card(db_session):    
    repo = CardRepository(db_session)    
    
    result = repo.delete_card(999)    
    
    assert result is False