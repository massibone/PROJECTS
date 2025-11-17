from sqlalchemy.orm import Session
import models, schemas

def get_utente(db: Session, utente_id: int):
    return db.query(models.Utente).filter(models.Utente.id == utente_id).first()

def create_utente(db: Session, utente: schemas.UtenteCreate):
    db_utente = models.Utente(**utente.dict())
    db.add(db_utente)
    db.commit()
    db.refresh(db_utente)
    return db_utente

def create_pasto(db: Session, pasto: schemas.PastoCreate, utente_id: int):
    db_pasto = models.Pasto(**pasto.dict(), utente_id=utente_id)
    db.add(db_pasto)
    db.commit()
    db.refresh(db_pasto)
    return db_pasto

def create_lista_spesa(db: Session, lista: schemas.ListaSpesaCreate, utente_id: int):
    db_lista = models.ListaSpesa(**lista.dict(), utente_id=utente_id)
    db.add(db_lista)
    db.commit()
    db.refresh(db_lista)
    return db_lista
