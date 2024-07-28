from . import db
from .produto import Produto

class ProdutoDAO:
    
    @staticmethod
    def get_all_produto():
        return Produto.query.all()
