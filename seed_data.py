"""
seed_data.py - Dados de exemplo: Ristorante da Nonna
Dev 5 - Sprint 3

Execute com: python seed_data.py
"""
from database.base import criar_tabelas
from database.engine import get_session
from services.auth_service import registrar
from services.kanban_service import (
    criar_board, criar_card, mover_card, criar_swimlane
)
from models.card import Coluna


def seed():
    print("Iniciando seed do Ristorante da Nonna...")
    criar_tabelas()
    session = get_session()

    # ── Usuário principal ─────────────────────────────────────────────────────
    try:
        nonna = registrar(session, "nonna", "nonna@ristorante.com", "carbonara123")
        print(f"  Usuário criado: {nonna.username}")
    except Exception:
        print("  Usuário 'nonna' já existe. Pulando.")
        from models.user import User
        nonna = session.query(User).filter(User.username == "nonna").first()

    # ── Board principal ───────────────────────────────────────────────────────
    board = criar_board(session, nonna.id, "Ristorante da Nonna", wip_doing=3)
    print(f"  Board criado: {board.name}")

    # ── Swimlanes ─────────────────────────────────────────────────────────────
    sw_cozinha  = criar_swimlane(session, board.id, "Cozinha",   position=0)
    sw_confeit  = criar_swimlane(session, board.id, "Confeitaria", position=1)
    sw_servico  = criar_swimlane(session, board.id, "Serviço",   position=2)
    print("  Swimlanes criadas: Cozinha, Confeitaria, Serviço")

    # ── Pratos (cartões) ─────────────────────────────────────────────────────
    pratos = [
        # (título, responsável, prioridade, descrição, swimlane, coluna_final)
        ("Preparar Carbonara",   "Chef Mario",   "alta",  "Massa, guanciale, ovo, pecorino romano",  sw_cozinha.id,  Coluna.FEITO),
        ("Massa Fresca",         "Chef Luigi",   "alta",  "Farinha 00 e ovos caipira",               sw_cozinha.id,  Coluna.FEITO),
        ("Molho Bolonhesa",      "Chef Mario",   "media", "Carne bovina, tomate San Marzano",        sw_cozinha.id,  Coluna.FAZENDO),
        ("Risotto ai Funghi",    "Chef Mario",   "alta",  "Porcini, arborio, parmesao",              sw_cozinha.id,  Coluna.FAZENDO),
        ("Pizza Margherita",     "Chef Luigi",   "media", "Massa, molho, mussarela, manjericao",     sw_cozinha.id,  Coluna.FAZENDO),
        ("Tiramisu",             "Pastry Ana",   "media", "Mascarpone, savoiardi, cafe",             sw_confeit.id,  Coluna.A_FAZER),
        ("Panna Cotta",          "Pastry Ana",   "baixa", "Creme de leite, baunilha, gelatina",      sw_confeit.id,  Coluna.A_FAZER),
        ("Bruschetta",           "Chef Luigi",   "baixa", "Pao, tomate, manjericao, azeite",         sw_servico.id,  Coluna.A_FAZER),
    ]

    for titulo, resp, prio, desc, sw_id, coluna_final in pratos:
        card = criar_card(session, board.id, titulo, resp,
                          swimlane_id=sw_id, priority=prio, description=desc)
        if coluna_final != Coluna.A_FAZER:
            # Passar por FAZENDO primeiro (para registrar started_at)
            mover_card(session, card.id, Coluna.FAZENDO)
            if coluna_final == Coluna.FEITO:
                mover_card(session, card.id, Coluna.FEITO)
        print(f"  Cartão criado: {titulo} → {coluna_final.value}")

    print("\nSeed concluído com sucesso!")
    print("Execute: streamlit run app.py")
    print("Login: nonna / carbonara123")


if __name__ == "__main__":
    seed()