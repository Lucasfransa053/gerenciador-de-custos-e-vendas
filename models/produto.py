from . import db

class Produto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    custo = db.Column(db.Float, nullable=False)
    preco_venda_desejado = db.Column(db.Float, nullable=False)
    venda = db.Column(db.Float, nullable=True)
    vendido = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, nome, custo, preco_venda_desejado, user_id):
        self.nome = nome
        self.custo = custo
        self.preco_venda_desejado = preco_venda_desejado
        self.user_id = user_id
        self.venda = None
        self.vendido = False
