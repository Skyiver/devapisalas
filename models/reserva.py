from datetime import datetime
from utils.database import db  

class Reserva(db.Model):
    __tablename__ = 'reservas'
    
    id = db.Column(db.Integer, primary_key=True)
    turma_id = db.Column(db.Integer, nullable=False)  
    sala = db.Column(db.String(50), nullable=False)   
    data = db.Column(db.String(20), nullable=False)  
    hora_inicio = db.Column(db.String(10), nullable=False)
    hora_fim = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(15), default='pendente')  
    
    def to_json(self):
        return {
            "id": self.id,
            "turma": self.turma_id,
            "sala": self.sala,
            "data": self.data,
            "horario": f"{self.hora_inicio}-{self.hora_fim}",  
            "status": self.status
        }