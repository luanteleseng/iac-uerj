from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Optional

class ConsultaBase(BaseModel):
    nome_cliente: str
    data_consulta: date
    hora_consulta: time
    status: Optional[str] = "agendado"

class ConsultaResponse(ConsultaBase):
    id: int
    data_criacao: datetime

    class Config:
        from_attributes = True