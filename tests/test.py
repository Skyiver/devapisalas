import pytest
from unittest.mock import patch
from flask import Flask
from models.reserva import db, Reserva  
from routes.reserva_route import reserva_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['TESTING'] = True
    
    db.init_app(app)
    app.register_blueprint(reserva_bp, url_prefix='/api')
    
    with app.app_context():
        db.create_all()
        db.session.query(Reserva).delete()
        db.session.commit()
    
    return app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        yield client

@patch('services.reserva_service.requests.get')
def test_criar_reserva_valida(mock_get, client):
    mock_get.return_value.status_code = 200
    
    response = client.post('/api/reservas', json={
        "turma_id": 1001,
        "sala": "LAB1",
        "data": "2024-12-01",
        "hora_inicio": "09:00",
        "hora_fim": "11:00"
    })
    
    assert response.status_code == 201
    assert response.json["sala"] == "LAB1"

@patch('services.reserva_service.requests.get')
def test_conflito_horario(mock_get, client):
    mock_get.return_value.status_code = 200
    
    # -------Reserva -------------
    client.post('/api/reservas', json={
        "turma_id": 2001,
        "sala": "LAB3",
        "data": "2024-12-10",
        "hora_inicio": "10:00",
        "hora_fim": "12:00"
    })

    # ------- Conflito de reserva ----------
    response = client.post('/api/reservas', json={
        "turma_id": 2002,
        "sala": "LAB3",
        "data": "2024-12-10",
        "hora_inicio": "11:00",
        "hora_fim": "13:00"
    })
    
    assert response.status_code == 400
    assert "Conflito" in response.json["erro"]