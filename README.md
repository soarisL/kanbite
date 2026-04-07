# KanBite

> Sistema Kanban para gestao de tarefas em restaurantes italianos.

## Stack
- **Frontend:** Streamlit
- **Backend:** Python 3.11 + SQLAlchemy
- **Banco:** SQLite
- **Testes:** pytest
- **Auth:** bcrypt

## Como rodar

```bash
python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
python -c "from database.base import criar_tabelas; criar_tabelas()"
streamlit run app.py
pytest
```

## Branch Strategy

| Branch | Uso |
|--------|-----|
| `main` | Protegida - apenas via PR aprovado |
| `develop` | Branch de integracao |
| `feature/<nome>` | Desenvolvimento individual |

## Equipe

| Dev | Papel | Responsabilidade |
|-----|-------|-----------------|
| Dev 1 | Auth & Backend | models/user, auth_service, login/registro |
| Dev 2 | Kanban Core | models/board+card+swimlane, kanban_service |
| Dev 3 | Banco & Metricas | database/, metrics_service |
| Dev 4 | UI & Frontend | app.py, pages/, components/, CSS |
| Dev 5 | Docs & QA | Artefatos, pytest, seed_data, entrega |
