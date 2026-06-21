# 🍕 KanBite

> Sistema web de gestão de fluxo de trabalho baseado no método Kanban, voltado para cozinhas de restaurantes italianos.

**Stack:** Python 3.11 · Streamlit · SQLAlchemy · SQLite · bcrypt · Plotly · pytest

---

## Sumário

1. [Pré-requisitos](#1-pré-requisitos)
2. [Instalação e Execução](#2-instalação-e-execução)
3. [Estrutura do Projeto](#3-estrutura-do-projeto)
4. [Funcionalidades — Passo a Passo](#4-funcionalidades--passo-a-passo)
   - [Criar conta](#41-criar-conta)
   - [Fazer login](#42-fazer-login)
   - [Criar quadro Kanban](#43-criar-quadro-kanban)
   - [Criar swimlane](#44-criar-swimlane)
   - [Criar cartão](#45-criar-cartão)
   - [Mover cartão entre colunas](#46-mover-cartão-entre-colunas)
   - [Mover cartão entre swimlanes](#47-mover-cartão-entre-swimlanes)
   - [Editar cartão](#48-editar-cartão)
   - [Excluir cartão](#49-excluir-cartão)
   - [Editar quadro](#410-editar-quadro)
   - [Excluir quadro](#411-excluir-quadro)
   - [Excluir swimlane](#412-excluir-swimlane)
   - [WIP Limit](#413-wip-limit)
   - [Dashboard de métricas](#414-dashboard-de-métricas)
   - [Logout](#415-logout)
5. [Rodando os Testes](#5-rodando-os-testes)
6. [Dados de Exemplo (Seed)](#6-dados-de-exemplo-seed)
7. [Variáveis de Ambiente](#7-variáveis-de-ambiente)
8. [Equipe](#8-equipe)

---

## 1. Pré-requisitos

| Requisito | Versão mínima | Como verificar |
|---|---|---|
| Python | 3.11 | `python --version` |
| pip | qualquer | `pip --version` |
| Git | qualquer | `git --version` |
| Navegador | Chrome, Firefox ou Safari (últimas 2 versões) | — |

> **Windows:** use `python` e `.venv\Scripts\activate`  
> **macOS/Linux:** use `python3` e `source .venv/bin/activate`

---

## 2. Instalação e Execução

### Passo 1 — Clonar o repositório

```bash
git clone https://github.com/soarisL/kanbite.git
cd kanbite
```

### Passo 2 — Criar e ativar o ambiente virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

Quando ativo, o terminal exibe `(.venv)` no início da linha.

### Passo 3 — Instalar as dependências

```bash
pip install -r requirements.txt
```

Dependências instaladas:

| Biblioteca | Versão | Finalidade |
|---|---|---|
| streamlit | 1.35.0 | Interface web |
| sqlalchemy | 2.0.30 | ORM e acesso ao banco |
| bcrypt | 4.1.3 | Hash de senhas |
| plotly | 5.22.0 | Gráficos de métricas |
| pandas | 2.2.2 | Manipulação de dados |
| pytest | 8.2.0 | Testes automatizados |
| pydantic | 2.7.1 | Validação de dados |

### Passo 4 — Criar as tabelas do banco

```bash
python -c "from database.base import criar_tabelas; criar_tabelas()"
```

Isso cria o arquivo `kanbite.db` na raiz do projeto com todas as tabelas.

### Passo 5 — Executar a aplicação

```bash
streamlit run app.py
```

O terminal exibirá:

```
  You can now view your Streamlit app in your browser.
  Local URL: http://localhost:8501
```

Abra `http://localhost:8501` no navegador.

---

### Execução completa em um bloco (copie e cole)

**macOS / Linux:**
```bash
git clone https://github.com/soarisL/kanbite.git
cd kanbite
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 -c "from database.base import criar_tabelas; criar_tabelas()"
streamlit run app.py
```

**Windows:**
```bash
git clone https://github.com/soarisL/kanbite.git
cd kanbite
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -c "from database.base import criar_tabelas; criar_tabelas()"
streamlit run app.py
```

---

## 3. Estrutura do Projeto

```
kanbite/
│
├── app.py                      # Entry point do Streamlit
├── requirements.txt            # Dependências
├── seed_data.py                # Script de dados de exemplo
├── conftest.py                 # Fixtures globais de teste
│
├── pages/
│   ├── 00_home.py              # Página inicial após login
│   ├── 01_login.py             # Tela de login
│   ├── 02_register.py          # Tela de cadastro
│   ├── 03_metrics.py           # Dashboard de métricas
│   └── 04_board.py             # Quadro Kanban principal
│
├── components/
│   ├── sidebar.py              # Barra lateral de navegação
│   └── kan_card.py             # Componente visual de cartão
│
├── services/
│   ├── auth_service.py         # Registro e autenticação (bcrypt)
│   ├── kanban_service.py       # Regras de negócio: WIP, CRUD
│   └── metrics_service.py      # Cálculo de métricas Kanban
│
├── database/
│   ├── engine.py               # Engine SQLAlchemy e sessão
│   ├── base.py                 # Base declarativa e criação de tabelas
│   └── repos/
│       ├── board_repo.py       # CRUD de quadros
│       ├── card_repo.py        # CRUD de cartões + timestamps
│       ├── swimlane_repo.py    # CRUD de swimlanes
│       └── user_repo.py        # CRUD de usuários
│
├── models/
│   ├── user.py                 # Entidade User
│   ├── board.py                # Entidade Board
│   ├── swimlane.py             # Entidade Swimlane
│   └── card.py                 # Entidade Card + Enums
│
├── tests/
│   ├── conftest.py             # Fixtures de banco em memória
│   ├── test_auth.py            # Testes de autenticação
│   ├── test_kanban.py          # Testes de boards e cartões
│   ├── test_metrics.py         # Testes de métricas
│   ├── test_repos.py           # Testes de repositórios
│   └── test_wip.py             # Testes de WIP limit
│
└── assets/
    └── style.css               # Estilos globais da interface
```

---

## 4. Funcionalidades — Passo a Passo

### 4.1 Criar conta

1. Acesse `http://localhost:8501`
2. A tela de **Login** é exibida. Clique em **"Cadastre-se aqui"** no rodapé.
3. Preencha os campos:
   - **Usuário:** nome único para login (ex: `chef_mario`)
   - **E-mail:** endereço de e-mail válido
   - **Senha:** mínimo 6 caracteres
   - **Confirmar Senha:** repita a senha
4. Clique em **"Criar Conta"**.
5. Mensagem de sucesso aparece. Clique em **"Ir para o Login"**.

> ⚠️ Usuário e e-mail devem ser únicos. Se já existirem, um erro é exibido.

---

### 4.2 Fazer login

1. Na tela de Login, preencha:
   - **Usuário:** seu nome de usuário
   - **Senha:** sua senha
2. Clique em **"Entrar"**.
3. Você é redirecionado para a **Home**.

> ❌ Credenciais incorretas exibem mensagem de erro em vermelho.

---

### 4.3 Criar quadro Kanban

1. No menu lateral, clique em **"Quadro"**.
2. Se não houver quadros, um formulário é exibido automaticamente. Caso já tenha quadros, esse passo pode ser pulado.
3. Preencha:
   - **Nome do quadro:** ex: `Cozinha da Nonna`
   - **WIP Limit:** número máximo de cartões simultâneos em FAZENDO (ex: `3`). Use `0` para sem limite.
4. Clique em **"Criar Quadro"**.
5. O quadro aparece com as 3 colunas: **A FAZER**, **FAZENDO**, **FEITO**.

---

### 4.4 Criar swimlane

Swimlanes são raias dentro do quadro que separam as seções da cozinha (ex: Cozinha, Confeitaria, Serviço).

1. Na página do Quadro, clique em **"🏊 Gerenciar swimlanes"** para expandir o painel.
2. Digite o nome da swimlane no campo (ex: `Cozinha Quente`).
3. Clique em **"➕ Adicionar swimlane"**.
4. A swimlane aparece listada no painel.
5. Repita para adicionar quantas swimlanes precisar.

---

### 4.5 Criar cartão

1. Na parte inferior do Quadro, clique em **"➕ Adicionar novo cartão"** para expandir o formulário.
2. Preencha os campos:
   - **Título \*** (obrigatório): nome da tarefa, ex: `Preparar Carbonara`
   - **Responsável \*** (obrigatório): nome do responsável, ex: `Chef Mario`
   - **Prioridade:** `baixa`, `media` ou `alta`
   - **Descrição:** detalhes da tarefa (opcional)
   - **Prazo:** data limite (opcional)
3. Clique em **"Criar Cartão"**.
4. O cartão aparece imediatamente na coluna **A FAZER**.

> Campos obrigatórios: Título e Responsável. Sem eles, um erro é exibido.

---

### 4.6 Mover cartão entre colunas

1. Localize o cartão no quadro e clique nele para expandir.
2. Os botões de movimentação aparecem no rodapé do cartão expandido:
   - Se o cartão está em **A FAZER**: botão `→ FAZENDO` e `→ FEITO`
   - Se o cartão está em **FAZENDO**: botão `→ A FAZER` e `→ FEITO`
   - Se o cartão está em **FEITO**: botão `→ A FAZER` e `→ FAZENDO`
3. Clique no botão da coluna de destino.
4. O cartão é movido e a contagem da coluna é atualizada.

> ⏱ Ao mover para **FAZENDO**, o campo `started_at` é registrado automaticamente.  
> ✅ Ao mover para **FEITO**, o campo `finished_at` é registrado automaticamente.

---

### 4.7 Mover cartão entre swimlanes

1. Clique no cartão para expandir.
2. Localize o seletor **"Swimlane:"** dentro do cartão expandido.
3. Selecione a nova swimlane no dropdown.
4. O cartão é movido para a swimlane selecionada imediatamente (sem clicar em botão).

> A coluna do cartão não é alterada ao mudar de swimlane.

---

### 4.8 Editar cartão

1. Clique no cartão para expandir.
2. Clique no botão **"✏️ Editar"**.
3. Um painel de edição abre com os campos atuais preenchidos:
   - Título
   - Responsável
   - Prioridade
   - Descrição
4. Altere os campos desejados e clique em **"💾 Salvar alterações"**.

> Editar um cartão **não altera** sua coluna nem sua swimlane.

---

### 4.9 Excluir cartão

1. Clique no cartão para expandir.
2. Clique em **"🗑️ Excluir"**.
3. O cartão é removido imediatamente do quadro.

> ⚠️ A exclusão é permanente e não pode ser desfeita.

---

### 4.10 Editar quadro

Para alterar o nome ou WIP limit de um quadro existente:

1. Na página do Quadro, selecione o quadro desejado no seletor no topo.
2. O WIP limit atual é exibido abaixo do seletor.
3. Para editar: no formulário de criação de board (disponível quando não há quadros) ou via edição direta — crie um novo quadro com o nome/WIP desejado se necessário.

> A atualização do WIP limit é validada no próximo movimento de cartão.

---

### 4.11 Excluir quadro

1. Para excluir um quadro, todos os seus cartões e swimlanes são removidos em cascata automaticamente.
2. Na página do Quadro com o quadro selecionado, o botão de exclusão está disponível nas opções do board.

> ⚠️ A exclusão remove **todos** os cartões e swimlanes do quadro (cascade delete).

---

### 4.12 Excluir swimlane

1. Na página do Quadro, clique em **"🏊 Gerenciar swimlanes"**.
2. Localize a swimlane na lista.
3. Clique no ícone **"🗑️"** ao lado da swimlane.
4. A swimlane é removida. Os cartões que estavam nela **permanecem no quadro**, mas ficam sem swimlane associada.

---

### 4.13 WIP Limit

O WIP Limit (Work-In-Progress Limit) define o número máximo de cartões que podem estar simultaneamente na coluna **FAZENDO**.

**Como funciona:**
- Ao criar ou editar um quadro, defina o WIP limit desejado.
- `0` significa sem limite.
- Ao tentar mover um cartão para FAZENDO quando o limite já foi atingido, o sistema exibe:

```
❌ WIP limit atingido: máximo X cartões em FAZENDO.
   Conclua um cartão antes de iniciar outro.
```

- Para liberar uma vaga, mova um cartão de FAZENDO para FEITO.

---

### 4.14 Dashboard de métricas

1. No menu lateral, clique em **"📊 Métricas"** (ou acesse `http://localhost:8501/03_metrics`).
2. Selecione o quadro desejado no seletor.
3. O dashboard exibe:

| Métrica | O que mede |
|---|---|
| **⏱ Cycle Time** | Tempo médio (em dias) que um cartão passa em FAZENDO até ir para FEITO |
| **🗓 Lead Time** | Tempo médio (em dias) desde a criação do cartão até ir para FEITO |
| **✅ Throughput** | Total de cartões que chegaram à coluna FEITO |
| **🔄 WIP Atual** | Número de cartões atualmente em FAZENDO |

4. Dois gráficos são exibidos:
   - **Barras:** quantidade de cartões por coluna (A FAZER / FAZENDO / FEITO)
   - **Pizza:** proporção de cartões entre as colunas

> Se não houver cartões com dados suficientes, a mensagem "Sem dados" é exibida nos KPIs.

---

### 4.15 Logout

1. Na **Home** (`http://localhost:8501/00_home`), clique em **"🚪 Sair"**.
2. A sessão é encerrada e você é redirecionado para a tela de login.
3. Qualquer tentativa de acessar o quadro ou métricas sem login exibe um aviso de autenticação.

---

## 5. Rodando os Testes

Com o ambiente virtual ativo, execute na raiz do projeto:

```bash
pytest
```

Para ver mais detalhes:

```bash
pytest -v
```

Para ver cobertura de código (requer `pytest-cov`):

```bash
pip install pytest-cov
pytest --cov=services --cov-report=term-missing
```

### Suites de teste disponíveis

| Arquivo | O que testa |
|---|---|
| `tests/test_auth.py` | Registro, login, senhas incorretas, usuário duplicado |
| `tests/test_kanban.py` | Criação de boards, cartões e movimentação entre colunas |
| `tests/test_wip.py` | WIP limit: bloqueio, WIP=0, liberação após conclusão |
| `tests/test_metrics.py` | Cycle time, lead time, throughput, WIP atual |
| `tests/test_repos.py` | Operações CRUD dos repositórios de dados |

> Os testes usam banco **SQLite em memória** e são totalmente isolados do banco de desenvolvimento.

---

## 6. Dados de Exemplo (Seed)

Para popular o banco com dados de demonstração do "Ristorante da Nonna":

```bash
python seed_data.py
```

Isso cria:
- **Usuário:** `nonna` / senha: `carbonara123`
- **Quadro:** `Ristorante da Nonna` com WIP limit = 3
- **Swimlanes:** Cozinha, Confeitaria, Serviço
- **8 cartões** em diferentes colunas e swimlanes com timestamps reais

Após o seed, acesse `http://localhost:8501` e faça login com `nonna` / `carbonara123`.

> ⚠️ Execute o seed apenas uma vez. Se o usuário `nonna` já existir, o script ignora e cria apenas o novo board.

---

## 7. Variáveis de Ambiente

| Variável | Padrão | Descrição |
|---|---|---|
| `DATABASE_URL` | `sqlite:///kanbite.db` | String de conexão com o banco. Para PostgreSQL em produção: `postgresql://user:senha@host/banco` |
| `SECRET_KEY` | — | Chave para tokens futuros (reservado) |

Para definir em desenvolvimento:

**macOS / Linux:**
```bash
export DATABASE_URL="sqlite:///kanbite.db"
streamlit run app.py
```

**Windows:**
```bash
set DATABASE_URL=sqlite:///kanbite.db
streamlit run app.py
```

---

## 8. Equipe

| Nome | Matrícula | Responsabilidade |
|---|---|---|
| Gustavo Pinheiro | 211066089 | Banco de Dados, Testes e Interfaces UI |
| Ismael Oliveira | 190089261 | Controle do Kanban e Auxiliar Backend |
| Maira Silva | 222026214 | Mockup, Documentação, Wireframe e Artefatos |
| Luiz Soaris | 190092025 | Backend, Frontend e Camada de Serviço |

---

*KanBite — Engenharia de Software · 2026 · Licença MIT*
