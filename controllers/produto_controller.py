from flask import Blueprint, request, render_template, redirect, url_for, session, flash
from models.produto import Produto
from models import db
from models.produto_dao import ProdutoDAO

produto_bp = Blueprint('produto_bp', __name__)

@produto_bp.route("/cadastrar", methods=['GET', 'POST'])
def cadastrar_produto():
    if 'user_id' not in session:
        flash('Você precisa estar logado para cadastrar um produto', 'danger')
        return redirect(url_for('user_bp.login'))
    
    if request.method == 'POST':
        nome = request.form['nome']
        custo = float(request.form['custo'])
        preco_venda_desejado = float(request.form['preco_venda_desejado'])
        user_id = session['user_id']

        produto = Produto(nome=nome, custo=custo, preco_venda_desejado=preco_venda_desejado, user_id=user_id)
        db.session.add(produto)
        db.session.commit()
        flash('Produto cadastrado com sucesso', 'success')
        return redirect(url_for('index'))
    return render_template('cadastrar.html')

@produto_bp.route('/vender/<int:id>', methods=['GET', 'POST'])
def vender_produto(id):
    produto = Produto.query.get_or_404(id)
    if 'user_id' not in session or produto.user_id != session['user_id']:
        flash('Você não tem permissão para vender este produto', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        venda = float(request.form['venda'])
        produto.venda = venda
        produto.vendido = True
        db.session.commit()
        flash('Produto marcado como vendido', 'success')
        return redirect(url_for('produto_bp.listar_produtos'))
    return render_template('vender.html', produto=produto)

@produto_bp.route('/exibir', methods=['GET', 'POST'])
def listar_produtos():
    if 'user_id' not in session:
        flash('Você precisa estar logado para ver seus produtos', 'danger')
        return redirect(url_for('user_bp.login'))

    user_id = session['user_id']
    
    if request.method == 'POST':
        termo_pesquisa = request.form.get('termo_pesquisa', '').strip()
        produtos_disponiveis = Produto.query.filter(
            Produto.user_id == user_id,
            Produto.vendido == False,
            Produto.nome.contains(termo_pesquisa)
        ).all()
        produtos_vendidos = Produto.query.filter(
            Produto.user_id == user_id,
            Produto.vendido == True,
            Produto.nome.contains(termo_pesquisa)
        ).all()
    else:
        produtos_disponiveis = Produto.query.filter_by(user_id=user_id, vendido=False).all()
        produtos_vendidos = Produto.query.filter_by(user_id=user_id, vendido=True).all()
    
    return render_template('produtos.html', produtos_disponiveis=produtos_disponiveis, produtos_vendidos=produtos_vendidos)

@produto_bp.route('/deletar/<int:id>', methods=['POST'])
def deletar_produto(id):
    produto = Produto.query.get_or_404(id)
    if 'user_id' not in session or produto.user_id != session['user_id']:
        flash('Você não tem permissão para deletar este produto', 'danger')
        return redirect(url_for('index'))
    
    db.session.delete(produto)
    db.session.commit()
    flash('Produto deletado com sucesso', 'success')
    return redirect(url_for('produto_bp.listar_produtos'))

@produto_bp.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar_produto(id):
    produto = Produto.query.get_or_404(id)
    if 'user_id' not in session or produto.user_id != session['user_id']:
        flash('Você não tem permissão para editar este produto', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        produto.nome = request.form.get('nome', produto.nome)
        produto.custo = float(request.form.get('custo', produto.custo))
        produto.preco_venda_desejado = float(request.form.get('preco_venda_desejado', produto.preco_venda_desejado))
        db.session.commit()
        flash('Produto atualizado com sucesso!', 'success')
        return redirect(url_for('produto_bp.listar_produtos'))
    
    return render_template('editar.html', produto=produto)
