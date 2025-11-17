from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Utente(Base):
    __tablename__ = "utenti"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    eta = Column(Integer)
    peso = Column(Float)
    altezza = Column(Float)
    obiettivo_calorico = Column(Integer)  # es. 2000 kcal

class Pasto(Base):
    __tablename__ = "pasti"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    calorie = Column(Integer)
    proteine = Column(Float)
    carboidrati = Column(Float)
    grassi = Column(Float)
    utente_id = Column(Integer, ForeignKey("utenti.id"))

class ListaSpesa(Base):
    __tablename__ = "liste_spesa"
    id = Column(Integer, primary_key=True, index=True)
    ingrediente = Column(String)
    quantita = Column(String)
    utente_id = Column(Integer, ForeignKey("utenti.id"))
    data = Column(Date)
