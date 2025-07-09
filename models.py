from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from sqlalchemy.sql import func
from .database import Base

class Consulta(Base):
    __tablename__ = 'consultas'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_cliente = Column(String(255))
    data_consulta = Column(Date)
    hora_consulta = Column(Time)
    status = Column(String(50))
    data_criacao = Column(DateTime, server_default=func.now())