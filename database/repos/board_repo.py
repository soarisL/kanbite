# TODO: Dev2 implementar CRUD de Board

"""
Repositories/board_repo.py - Repositório de Boards
"""

from sqlalchemy.orm import Session 
'''
* Biblioteca que faz o mapeamento das classes de python para tabelas
de bancos de dados relacional -> Manipula dados de objetos
* Session: Mecanismo central que gerencia os objetos
    -> Estabelece a conversa
    -> Acumula as alterações e joga para o banco
'''
from models.board import Board

class BoardRepository:

    def __init__(self, db: Session):
        self.db = db
        
    def create_board(self, name: str, owner_id: int, wip_todo: int = 0, wip_doing: int = 3) -> Board:
        '''
        name -> espera uma string
        owned_id -> int
        wip_todo -> int com valor 0 -> sem limite (pode ter várias tarefas)
        wip_doing -> int com valor 3 -> so podem ter 3 projetos em andamento
        '''
        board = Board(
            name=name,
            owner_id=owner_id,
            wip_todo=wip_todo,
            wip_doing=wip_doing

        )
        self.db.add(board)
        self.db.commit()
        self.db.refresh(board)
        return board
    
    def get_by_id(self, board_id: int) -> Board | None:
        return self.db.query(Board).filter(Board.id == board_id).first()
    
    def get_by_owned(self, owned_id: int) -> Board | None:
        return self.db.query(Board).filter(Board.owner_id == owned_id).all()
    
    # Atualiza os nomes -> coloca nomes no bd
    def update_name(self, board_id: int, new_name: str) -> Board | None:
        board = self.get_by_id(board_id)
        if not board:
            return None
        
        # Coloca o novo nome da tarefa
        board.name = new_name
        # Adiciona no bd
        self.db.commit()
        # Atualiza
        self.db.refresh(board)
        return board
    
    # Deleta o nome -> Apaga a tarefea
    def delete_board(self, board_id: int) -> bool:
        board = self.get_by_id(board_id)
        if not board: 
            return False
        
        self.db.delete(board)
        self.db.commit()
        return True