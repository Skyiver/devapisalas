import requests
from flask import current_app
from models.reserva import Reserva
from utils.database import db

class ReservaService:
    
    @staticmethod
    def validar_turma(turma_id):
        try:
            response = requests.get(
                f"{current_app.config.get('C1_API_URL', 'http://localhost:5002')}/api/turmas/{turma_id}"
            )
            return response.status_code == 200
        except requests.exceptions.RequestException:
            return False

    @staticmethod
    def validar_conflito(dados):
        return Reserva.query.filter(
            (Reserva.sala == dados['sala']) &
            (Reserva.data == dados['data']) &
            (
                (Reserva.hora_inicio <= dados['hora_fim']) &
                (Reserva.hora_fim >= dados['hora_inicio'])
            )
        ).first() is not None

    @staticmethod
    def criar_reserva(dados):
        if not ReservaService.validar_turma(dados['turma_id']):
            raise ValueError("Turma inválida")
            
        if ReservaService.validar_conflito(dados):
            raise ValueError("Conflito de horário")
            
        reserva = Reserva(**dados)
        db.session.add(reserva)
        db.session.commit()
        return reserva