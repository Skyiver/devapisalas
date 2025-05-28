import os
import requests
from models.reserva import Reserva
from utils.database import db

class ReservaService:
    C1_API_URL = os.getenv('C1_API_URL', 'http://host.docker.internal:5002/api')
    
    @staticmethod
    def validar_turma(turma_id):
        try:
            response = requests.get(
                f"{ReservaService.C1_API_URL}/turmas/{turma_id}",
                timeout=5  
            )
            return response.status_code == 200
        except requests.exceptions.RequestException as e:
            print(f"Erro ao validar turma: {str(e)}")
            return False

    @staticmethod
    def validar_conflito(dados):
        conflito = Reserva.query.filter(
            (Reserva.sala == dados['sala']) &
            (Reserva.data == dados['data']) &
            (Reserva.hora_inicio <= dados['hora_fim']) &
            (Reserva.hora_fim >= dados['hora_inicio'])
        ).first()
        
        return conflito is not None

    @staticmethod
    def criar_reserva(dados):
        campos_obrigatorios = ['turma_id', 'sala', 'data', 'hora_inicio', 'hora_fim']
        for campo in campos_obrigatorios:
            if campo not in dados or not dados[campo]:
                raise ValueError(f"Campo obrigatório faltando: {campo}")
        
        if not ReservaService.validar_turma(dados['turma_id']):
            raise ValueError("Turma não encontrada no sistema acadêmico")
            
        if ReservaService.validar_conflito(dados):
            raise ValueError("Conflito de horário na sala selecionada")
            
        reserva = Reserva(
            turma_id=dados['turma_id'],
            sala=dados['sala'],
            data=dados['data'],
            hora_inicio=dados['hora_inicio'],
            hora_fim=dados['hora_fim']
        )
        
        db.session.add(reserva)
        db.session.commit()
        return reserva