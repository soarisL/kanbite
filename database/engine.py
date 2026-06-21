"""
database/engine.py - Conexao SQLite + fabrica de sessoes
Dev 3 - Sprint 1, Dia 7
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///kanbite.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session() -> Session:
    return SessionLocal()


def get_engine():
    return engine
