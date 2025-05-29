from flask import Blueprint, request, jsonify
from services.reserva_service import ReservaService
from models.reserva import Reserva  
from utils.database import db

reserva_bp = Blueprint('reserva', __name__, url_prefix='/api')

@reserva_bp.route('/')
def health_check():
    return jsonify({
        "status": "online", 
        "service": "reservas",
        "message": "Serviço de reservas operacional"
    }), 200

@reserva_bp.route('/reservas', methods=['POST'])
def criar_reserva():
    try:
        dados = request.json
        reserva = ReservaService.criar_reserva(dados)
        return jsonify({
            "id": reserva.id,  
            "sala": reserva.sala,
            "data": reserva.data,
            "horario": f"{reserva.hora_inicio}-{reserva.hora_fim}"
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 400

@reserva_bp.route('/reservas', methods=['GET'])
def listar_reservas():
    reservas = Reserva.query.all()
    return jsonify([{
        "id": r.id,
        "sala": r.sala,
        "data": r.data,
        "horario": f"{r.hora_inicio}-{r.hora_fim}"
    } for r in reservas])

@reserva_bp.route('/reservas/<int:id>', methods=['GET'])
def buscar_reserva(id):
    reserva = Reserva.query.get(id)
    if not reserva:
        return jsonify({"erro": "Reserva não encontrada"}), 404
    return jsonify({
        "id": reserva.id,
        "sala": reserva.sala,
        "data": reserva.data,
        "horario": f"{reserva.hora_inicio}-{reserva.hora_fim}"
    })
    
@reserva_bp.route('/reseta', methods=['POST'])
def resetar_reservas():
    try:
        db.session.query(Reserva).delete()
        db.session.commit()
        return jsonify({"status": "reservas resetadas"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"erro": str(e)}), 500