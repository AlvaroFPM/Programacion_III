# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, crear_base_datos
from models import Personaje, Mision
from Cola import ColaMisiones

app = FastAPI()
crear_base_datos()

@app.post("/personajes")
def crear_personaje(nombre: str, db: Session = Depends(get_db)):
    nuevo = Personaje(nombre=nombre)
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

@app.post("/misiones")
def crear_mision(nombre: str, descripcion: str = "", experiencia: int = 0, estado: str = "pendiente", db: Session = Depends(get_db)):
    nueva = Mision(nombre=nombre, descripcion=descripcion, experiencia=experiencia, estado=estado)
    db.add(nueva)
    db.commit()
    db.refresh(nueva)
    return nueva

@app.post("/personajes/{personaje_id}/misiones/{mision_id}")
def aceptar_mision(personaje_id: int, mision_id: int, db: Session = Depends(get_db)):
    cola = ColaMisiones(personaje_id, db)
    cola.enqueue(mision_id)
    return {"mensaje": "Misión encolada exitosamente."}

@app.post("/personajes/{personaje_id}/completar")
def completar_mision(personaje_id: int, db: Session = Depends(get_db)):
    cola = ColaMisiones(personaje_id, db)
    mision_relacionada = cola.dequeue()
    if not mision_relacionada:
        raise HTTPException(status_code=404, detail="No hay misiones para completar.")
    
    personaje = db.query(Personaje).filter_by(id=personaje_id).first()
    mision = db.query(Mision).filter_by(id=mision_relacionada.mision_id).first()
    personaje.experiencia += mision.experiencia
    db.commit()
    return {"mensaje": "Misión completada.", "xp_ganada": mision.experiencia}

@app.get("/personajes/{personaje_id}/misiones")
def listar_misiones(personaje_id: int, db: Session = Depends(get_db)):
    cola = ColaMisiones(personaje_id, db)
    lista = cola.get_all()
    return [{"mision_id": item.mision_id, "orden": item.orden} for item in lista]
