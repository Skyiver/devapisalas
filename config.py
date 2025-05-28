import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///reservas.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    API_TURMAS = os.getenv('C1_API_URL', 'http://host.docker.internal:5002/api')