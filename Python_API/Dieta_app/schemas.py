from pydantic import BaseModel
from typing import Optional
from datetime import date

class UtenteCreate(BaseModel):
    nome: str
    eta: int
    peso: float
    altezza: float
    obiettivo_calorico: int

class PastoCreate(BaseModel):
    nome: str
    calorie: int
    proteine: float
    carboidrati: float
    grassi: float

class ListaSpesaCreate(BaseModel):
    ingrediente: str
    quantita: str
    data: date

class ListaSpesaOut(BaseModel):
    ingrediente: str
    quantita: str
    data: date

5. database.py (Configurazione DB)
python
Copia
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./dieta.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
