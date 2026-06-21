import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.base import Base 
from database.repos.user_repo import User
from database.repos.board_repo import Board
from database.repos.swimlane_repo import Swimlane
from database.repos.card_repo import Card

@pytest.fixture(scope="session")
def test_engine():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    return engine
        
@pytest.fixture(scope="function")
def db_session(test_engine):
    if Base is not None:
        Base.metadata.drop_all(bind=test_engine)
        Base.metadata.create_all(bind=test_engine)
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = SessionLocal()
    
    yield session
    
    session.close()