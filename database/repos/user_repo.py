"""
database/repos/user_repo.py - Repositorio de User
Dev 1 - Sprint 1, Dia 7
"""
from sqlalchemy.orm import Session
from models.user import User


class UserRepo:
    def __init__(self, session: Session):
        self.session = session

    def criar(self, username: str, email: str, hashed_password: str) -> User:
        usuario = User(username=username, email=email, hashed_password=hashed_password)
        self.session.add(usuario)
        self.session.flush()
        return usuario

    def buscar_por_id(self, user_id: int) -> User | None:
        return self.session.get(User, user_id)

    def buscar_por_username(self, username: str) -> User | None:
        return self.session.query(User).filter(User.username == username).first()

    def buscar_por_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).first()

    def existe(self, username: str, email: str) -> bool:
        return self.session.query(User).filter(
            (User.username == username) | (User.email == email)
        ).first() is not None

    def desativar(self, user_id: int) -> bool:
        usuario = self.buscar_por_id(user_id)
        if usuario:
            usuario.is_active = False
            self.session.flush()
            return True
        return False
