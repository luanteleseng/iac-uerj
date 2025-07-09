from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db
import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/health")
def health_check():
    return {"status": "online", "service": "Agendamento de Consultas"}

# Rota POST - Criar consulta
@app.post("/consultas/", response_model=schemas.ConsultaResponse, status_code=status.HTTP_201_CREATED)
async def criar_consulta(consulta: schemas.ConsultaBase, db: Session = Depends(get_db)):
    db_consulta = models.Consulta(**consulta.dict())
    db.add(db_consulta)
    db.commit()
    db.refresh(db_consulta)
    return db_consulta

# Rota GET - Listar todas consultas
@app.get("/consultas/", response_model=list[schemas.ConsultaResponse])
async def listar_consultas(db: Session = Depends(get_db)):
    return db.query(models.Consulta).all()

# Rota GET - Obter consulta por ID
@app.get("/consultas/{consulta_id}", response_model=schemas.ConsultaResponse)
async def obter_consulta(consulta_id: int, db: Session = Depends(get_db)):
    consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consulta com ID {consulta_id} não encontrada"
        )
    return consulta

# Rota PUT
@app.put("/consultas/{consulta_id}", response_model=schemas.ConsultaResponse)
async def atualizar_consulta(
    consulta_id: int, 
    consulta_data: schemas.ConsultaBase, 
    db: Session = Depends(get_db)
):
    consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consulta com ID {consulta_id} não encontrada"
        )
    
    for key, value in consulta_data.dict().items():
        setattr(consulta, key, value)
    
    db.commit()
    db.refresh(consulta)
    return consulta

# Rota DELETE
@app.delete("/consultas/{consulta_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_consulta(consulta_id: int, db: Session = Depends(get_db)):
    consulta = db.query(models.Consulta).filter(models.Consulta.id == consulta_id).first()
    if not consulta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Consulta com ID {consulta_id} não encontrada"
        )
    
    db.delete(consulta)
    db.commit()
    return None