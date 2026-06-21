"""
models/__init__.py - Registro central dos models SQLAlchemy

Importar TODOS os models aqui, no nivel do pacote, garante que o
SQLAlchemy registre todas as classes antes de qualquer mapper ser
configurado. Sem isso, relationship() que referencia outra classe
por string (ex: relationship("Board", ...)) pode falhar com
"expression 'Board' failed to locate a name", dependendo de qual
modulo da aplicacao importa 'models.user' primeiro.

Qualquer codigo que precise dos models deve poder fazer apenas
`import models` (ou importar um submodulo especifico) que esta
lista garante que todas as classes already estao registradas.
"""
from models.user import User
from models.board import Board
from models.swimlane import Swimlane
from models.card import Card, Coluna, Prioridade

__all__ = ["User", "Board", "Swimlane", "Card", "Coluna", "Prioridade"]
