from flask import Flask, render_template, url_for, session
from models import db
from controllers.produto_controller import produto_bp
from controllers.user_controller import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///banco.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'  # Adicione uma chave secreta

db.init_app(app)

app.register_blueprint(produto_bp, url_prefix='/produto')
app.register_blueprint(user_bp, url_prefix='/user')

@app.route('/')
def index():
    return render_template('index.html', logged_in='user_id' in session)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
