"""
services/auth_service.py - Autenticacao
Dev 1 - Sprint 1 (estrutura) / Sprint 3 (completo)
"""
import bcrypt
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models.user import User


class UsuarioJaExisteError(Exception): pass
class CredenciaisInvalidasError(Exception): pass
class UsuarioInativoError(Exception): pass


def _hash_senha(senha: str) -> str:
    return bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def _verificar_senha(senha: str, hashed: str) -> bool:
    return bcrypt.checkpw(senha.encode("utf-8"), hashed.encode("utf-8"))


def registrar(session: Session, username: str, email: str, senha: str) -> User:
    existente = session.query(User).filter(
        (User.username == username) | (User.email == email)
    ).first()
    if existente:
        raise UsuarioJaExisteError(f"Username ou email ja existe.")
    try:
        usuario = User(username=username, email=email, hashed_password=_hash_senha(senha))
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario
    except IntegrityError:
        session.rollback()
        raise UsuarioJaExisteError("Error de integridade: Username ou email ja cadastrado.")

def autenticar(session: Session, username: str, senha: str) -> User:
    usuario = session.query(User).filter(User.username == username).first()
    if not usuario or not _verificar_senha(senha, usuario.hashed_password):
        raise CredenciaisInvalidasError("Username ou senha invalidos.")
    if not usuario.is_active:
        raise UsuarioInativoError("Esta conta esta desativada.")
    return usuario


def buscar_por_id(session: Session, user_id: int) -> User | None:
    return session.get(User, user_id)
