"""
tests/test_repos.py - Testes dos repositorios de banco de dados
Dev 2 - Sprint 3

Testa o CRUD de Board, Card e Swimlane de forma isolada,
sem depender dos services. Usa banco SQLite em memoria.
"""
import pytest
from database.repos.board_repo import BoardRepo
from database.repos.card_repo import CardRepo
from database.repos.swimlane_repo import SwimlaneRepo
from models.card import Coluna


# ═══════════════════════════════════════════════════════════════
#  FIXTURES LOCAIS
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def board_repo(db_session):
    return BoardRepo(db_session)


@pytest.fixture
def card_repo(db_session):
    return CardRepo(db_session)


@pytest.fixture
def swimlane_repo(db_session):
    return SwimlaneRepo(db_session)


@pytest.fixture
def board_criado(board_repo, db_session):
    """Cria um board de teste e commita para uso nos testes de card."""
    board = board_repo.criar(owner_id=99, name="Board de Teste", wip_doing=3)
    db_session.commit()
    return board


# ═══════════════════════════════════════════════════════════════
#  TESTES DO BOARD REPO
# ═══════════════════════════════════════════════════════════════

class TestBoardRepo:

    def test_criar_board_retorna_objeto(self, board_repo, db_session):
        board = board_repo.criar(owner_id=1, name="Cozinha")
        db_session.commit()
        assert board.id is not None
        assert board.name == "Cozinha"

    def test_criar_board_com_wip_personalizado(self, board_repo, db_session):
        board = board_repo.criar(owner_id=1, name="Board WIP", wip_doing=5)
        db_session.commit()
        assert board.wip_doing == 5

    def test_buscar_por_id_existente(self, board_repo, db_session):
        board = board_repo.criar(owner_id=2, name="Busca")
        db_session.commit()
        encontrado = board_repo.buscar_por_id(board.id)
        assert encontrado is not None
        assert encontrado.id == board.id

    def test_buscar_por_id_inexistente_retorna_none(self, board_repo):
        resultado = board_repo.buscar_por_id(99999)
        assert resultado is None

    def test_listar_por_usuario_retorna_apenas_do_usuario(self, board_repo, db_session):
        board_repo.criar(owner_id=10, name="Board User 10")
        board_repo.criar(owner_id=10, name="Board User 10 B")
        board_repo.criar(owner_id=11, name="Board User 11")
        db_session.commit()
        boards = board_repo.listar_por_usuario(user_id=10)
        assert len(boards) == 2
        assert all(b.owner_id == 10 for b in boards)

    def test_listar_por_usuario_sem_boards_retorna_lista_vazia(self, board_repo):
        resultado = board_repo.listar_por_usuario(user_id=99999)
        assert resultado == []

    def test_existe_retorna_true_para_board_existente(self, board_repo, db_session):
        board = board_repo.criar(owner_id=3, name="Existe")
        db_session.commit()
        assert board_repo.existe(board.id) is True

    def test_existe_retorna_false_para_id_invalido(self, board_repo):
        assert board_repo.existe(99999) is False

    def test_atualizar_nome(self, board_repo, db_session):
        board = board_repo.criar(owner_id=4, name="Nome Antigo")
        db_session.commit()
        atualizado = board_repo.atualizar_nome(board.id, "Nome Novo")
        db_session.commit()
        assert atualizado.name == "Nome Novo"

    def test_atualizar_nome_id_invalido_retorna_none(self, board_repo):
        resultado = board_repo.atualizar_nome(99999, "Nome")
        assert resultado is None

    def test_atualizar_wip(self, board_repo, db_session):
        board = board_repo.criar(owner_id=5, name="WIP Update", wip_doing=3)
        db_session.commit()
        board_repo.atualizar_wip(board.id, 7)
        db_session.commit()
        atualizado = board_repo.buscar_por_id(board.id)
        assert atualizado.wip_doing == 7

    def test_deletar_board_existente(self, board_repo, db_session):
        board = board_repo.criar(owner_id=6, name="Deletar")
        db_session.commit()
        resultado = board_repo.deletar(board.id)
        db_session.commit()
        assert resultado is True
        assert board_repo.buscar_por_id(board.id) is None

    def test_deletar_board_inexistente_retorna_false(self, board_repo):
        resultado = board_repo.deletar(99999)
        assert resultado is False


# ═══════════════════════════════════════════════════════════════
#  TESTES DO CARD REPO
# ═══════════════════════════════════════════════════════════════

class TestCardRepo:

    def test_criar_card_nasce_em_a_fazer(self, card_repo, board_criado, db_session):
        card = card_repo.criar(board_criado.id, "Carbonara", "Chef Mario")
        db_session.commit()
        assert card.id is not None
        assert card.column == Coluna.A_FAZER

    def test_criar_card_sem_started_at(self, card_repo, board_criado, db_session):
        card = card_repo.criar(board_criado.id, "Risotto", "Chef")
        db_session.commit()
        assert card.started_at is None
        assert card.finished_at is None

    def test_buscar_por_id_existente(self, card_repo, board_criado, db_session):
        card = card_repo.criar(board_criado.id, "Pizza", "Chef Luigi")
        db_session.commit()
        encontrado = card_repo.buscar_por_id(card.id)
        assert encontrado is not None
        assert encontrado.title == "Pizza"

    def test_buscar_por_id_inexistente_retorna_none(self, card_repo):
        assert card_repo.buscar_por_id(99999) is None

    def test_listar_por_board_retorna_todos(self, card_repo, board_criado, db_session):
        card_repo.criar(board_criado.id, "Card A", "Dev")
        card_repo.criar(board_criado.id, "Card B", "Dev")
        card_repo.criar(board_criado.id, "Card C", "Dev")
        db_session.commit()
        cards = card_repo.listar_por_board(board_criado.id)
        assert len(cards) >= 3

    def test_listar_por_board_filtra_por_coluna(self, card_repo, board_criado, db_session):
        c1 = card_repo.criar(board_criado.id, "Card Fazer", "Dev")
        c2 = card_repo.criar(board_criado.id, "Card Fazendo", "Dev")
        db_session.commit()
        card_repo.mover_coluna(c2.id, Coluna.FAZENDO)
        db_session.commit()

        a_fazer = card_repo.listar_por_board(board_criado.id, Coluna.A_FAZER)
        fazendo = card_repo.listar_por_board(board_criado.id, Coluna.FAZENDO)

        assert all(c.column == Coluna.A_FAZER for c in a_fazer)
        assert all(c.column == Coluna.FAZENDO for c in fazendo)

    def test_contar_por_coluna(self, card_repo, board_criado, db_session):
        c1 = card_repo.criar(board_criado.id, "Contar A", "Dev")
        c2 = card_repo.criar(board_criado.id, "Contar B", "Dev")
        db_session.commit()
        card_repo.mover_coluna(c1.id, Coluna.FAZENDO)
        card_repo.mover_coluna(c2.id, Coluna.FAZENDO)
        db_session.commit()
        total = card_repo.contar_por_coluna(board_criado.id, Coluna.FAZENDO)
        assert total >= 2

    def test_mover_para_fazendo_registra_started_at(self, card_repo, board_criado, db_session):
        card = card_repo.criar(board_criado.id, "Mover Fazendo", "Dev")
        db_session.commit()
        card_repo.mover_coluna(card.id, Coluna.FAZENDO)
        db_session.commit()
        atualizado = card_repo.buscar_por_id(card.id)
        assert atualizado.started_at is not None
        assert atualizado.column == Coluna.FAZENDO

    def test_mover_para_feito_registra_finished_at(self, card_repo, board_criado, db_session):
        card = card_repo.criar(board_criado.id, "Mover Feito", "Dev")
        db_session.commit()
        card_repo.mover_coluna(card.id, Coluna.FAZENDO)
        card_repo.mover_coluna(card.id, Coluna.FEITO)
        db_session.commit()
        atualizado = card_repo.buscar_por_id(card.id)
        assert atualizado.finished_at is not None
        assert atualizado.column == Coluna.FEITO

    def test_started_at_nao_sobrescreve_em_segunda_movimentacao(self, card_repo, board_criado, db_session):
        card = card_repo.criar(board_criado.id, "Timestamp", "Dev")
        db_session.commit()
        card_repo.mover_coluna(card.id, Coluna.FAZENDO)
        db_session.commit()
        primeiro_started = card_repo.buscar_por_id(card.id).started_at

        # Voltar para A_FAZER e mover para FAZENDO de novo
        card_repo.mover_coluna(card.id, Coluna.A_FAZER)
        db_session.commit()
        card_repo.mover_coluna(card.id, Coluna.FAZENDO)
        db_session.commit()
        segundo_started = card_repo.buscar_por_id(card.id).started_at

        # started_at nao deve mudar na segunda vez
        assert primeiro_started == segundo_started

    def test_atualizar_titulo_e_responsavel(self, card_repo, board_criado, db_session):
        card = card_repo.criar(board_criado.id, "Titulo Antigo", "Dev Antigo")
        db_session.commit()
        card_repo.atualizar(card.id, title="Titulo Novo", responsible="Dev Novo")
        db_session.commit()
        atualizado = card_repo.buscar_por_id(card.id)
        assert atualizado.title == "Titulo Novo"
        assert atualizado.responsible == "Dev Novo"

    def test_atualizar_prioridade(self, card_repo, board_criado, db_session):
        from models.card import Prioridade
        card = card_repo.criar(board_criado.id, "Prioridade", "Dev", priority="baixa")
        db_session.commit()
        card_repo.atualizar(card.id, priority="alta")
        db_session.commit()
        atualizado = card_repo.buscar_por_id(card.id)
        assert atualizado.priority == Prioridade.ALTA

    def test_mover_swimlane(self, card_repo, swimlane_repo, board_criado, db_session):
        swimlane = swimlane_repo.criar(board_criado.id, "Cozinha")
        db_session.commit()
        card = card_repo.criar(board_criado.id, "Card Swimlane", "Dev")
        db_session.commit()
        card_repo.mover_swimlane(card.id, swimlane.id)
        db_session.commit()
        atualizado = card_repo.buscar_por_id(card.id)
        assert atualizado.swimlane_id == swimlane.id

    def test_mover_swimlane_para_none_remove_raia(self, card_repo, swimlane_repo, board_criado, db_session):
        swimlane = swimlane_repo.criar(board_criado.id, "Servico")
        db_session.commit()
        card = card_repo.criar(board_criado.id, "Card Sem Raia", "Dev",
                                swimlane_id=swimlane.id)
        db_session.commit()
        card_repo.mover_swimlane(card.id, None)
        db_session.commit()
        atualizado = card_repo.buscar_por_id(card.id)
        assert atualizado.swimlane_id is None

    def test_deletar_card(self, card_repo, board_criado, db_session):
        card = card_repo.criar(board_criado.id, "Deletar Card", "Dev")
        db_session.commit()
        resultado = card_repo.deletar(card.id)
        db_session.commit()
        assert resultado is True
        assert card_repo.buscar_por_id(card.id) is None

    def test_deletar_card_inexistente_retorna_false(self, card_repo):
        assert card_repo.deletar(99999) is False


# ═══════════════════════════════════════════════════════════════
#  TESTES DO SWIMLANE REPO
# ═══════════════════════════════════════════════════════════════

class TestSwimlaneRepo:

    def test_criar_swimlane(self, swimlane_repo, board_criado, db_session):
        sw = swimlane_repo.criar(board_criado.id, "Cozinha", position=0)
        db_session.commit()
        assert sw.id is not None
        assert sw.name == "Cozinha"
        assert sw.position == 0

    def test_listar_por_board_ordem_position(self, swimlane_repo, board_criado, db_session):
        swimlane_repo.criar(board_criado.id, "Z Ultima",   position=2)
        swimlane_repo.criar(board_criado.id, "A Primeira", position=0)
        swimlane_repo.criar(board_criado.id, "M Meio",     position=1)
        db_session.commit()
        lista = swimlane_repo.listar_por_board(board_criado.id)
        posicoes = [sw.position for sw in lista]
        assert posicoes == sorted(posicoes)

    def test_atualizar_nome_swimlane(self, swimlane_repo, board_criado, db_session):
        sw = swimlane_repo.criar(board_criado.id, "Nome Antigo")
        db_session.commit()
        swimlane_repo.atualizar_nome(sw.id, "Nome Novo")
        db_session.commit()
        atualizado = swimlane_repo.buscar_por_id(sw.id)
        assert atualizado.name == "Nome Novo"

    def test_atualizar_posicao(self, swimlane_repo, board_criado, db_session):
        sw = swimlane_repo.criar(board_criado.id, "Posicao", position=0)
        db_session.commit()
        swimlane_repo.atualizar_posicao(sw.id, 5)
        db_session.commit()
        atualizado = swimlane_repo.buscar_por_id(sw.id)
        assert atualizado.position == 5

    def test_deletar_swimlane(self, swimlane_repo, board_criado, db_session):
        sw = swimlane_repo.criar(board_criado.id, "Deletar")
        db_session.commit()
        resultado = swimlane_repo.deletar(sw.id)
        db_session.commit()
        assert resultado is True
        assert swimlane_repo.buscar_por_id(sw.id) is None

    def test_deletar_swimlane_inexistente_retorna_false(self, swimlane_repo):
        assert swimlane_repo.deletar(99999) is False