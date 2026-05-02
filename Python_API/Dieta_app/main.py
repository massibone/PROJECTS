from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import crud, models, schemas
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/utenti/", response_model=schemas.UtenteCreate)
def create_utente(utente: schemas.UtenteCreate, db: Session = Depends(get_db)):
    return crud.create_utente(db=db, utente=utente)

@app.post("/pasti/", response_model=schemas.PastoCreate)
def create_pasto(pasto: schemas.PastoCreate, utente_id: int, db: Session = Depends(get_db)):
    return crud.create_pasto(db=db, pasto=pasto, utente_id=utente_id)

@app.post("/liste_spesa/", response_model=schemas.ListaSpesaOut)
def create_lista_spesa(lista: schemas.ListaSpesaCreate, utente_id: int, db: Session = Depends(get_db)):
    return crud.create_lista_spesa(db=db, lista=lista, utente_id=utente_id)
