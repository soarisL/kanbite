"""
tests/test_auth.py - Testes de autenticacao
Dev 1 - Sprint 1 (estrutura) / Sprint 3 (completo)
"""
import pytest

try:
    from services.auth_service import (
        registrar, autenticar,
        UsuarioJaExisteError, CredenciaisInvalidasError,
    )
    MODULES_READY = True
except ImportError:
    MODULES_READY = False


@pytest.mark.skipif(not MODULES_READY, reason="auth_service nao implementado")
class TestRegistrar:
    def test_registrar_usuario_novo(self, db_session):
        user = registrar(db_session, "mario", "mario@kanbite.com", "senha123")
        assert user.id is not None
        assert user.hashed_password != "senha123"

    def test_registrar_duplicado_levanta_erro(self, db_session):
        registrar(db_session, "mario", "mario@kanbite.com", "senha123")
        with pytest.raises(UsuarioJaExisteError):
            registrar(db_session, "mario", "outro@kanbite.com", "outrasenha")


@pytest.mark.skipif(not MODULES_READY, reason="auth_service nao implementado")
class TestAutenticar:
    def test_credenciais_corretas(self, db_session):
        registrar(db_session, "chef", "chef@kanbite.com", "segredo")
        user = autenticar(db_session, "chef", "segredo")
        assert user.username == "chef"

    def test_senha_errada(self, db_session):
        registrar(db_session, "chef", "chef@kanbite.com", "segredo")
        with pytest.raises(CredenciaisInvalidasError):
            autenticar(db_session, "chef", "senha_errada")

    def test_usuario_inexistente(self, db_session):
        with pytest.raises(CredenciaisInvalidasError):
            autenticar(db_session, "fantasma", "qualquercoisa")
