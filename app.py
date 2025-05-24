from flask import Flask
from models.reserva import db
from routes.reserva_route import reserva_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reservas.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(reserva_bp)

@app.before_first_request
def criar_tabelas():
    with app.app_context():
        db.create_all()
        
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    db.init_app(app)
    
    # Importe e registre o blueprint corretamente
    from routes.reserva_route import reserva_bp
    app.register_blueprint(reserva_bp, url_prefix='/api')  # Adicione o url_prefix
    
    return app

if __name__ == '__main__':
    app.run(port=5003, debug=True)