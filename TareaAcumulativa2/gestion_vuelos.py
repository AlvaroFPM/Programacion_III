
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from typing import List, Optional
from db import VueloBD, SessionLocal, init_db
from lista_vuelos import ListaVuelos

app = FastAPI()
init_db()
lista = ListaVuelos()

class Vuelo(BaseModel):
    destino: str
    hora: str
    prioridad: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/vuelos/")
def agregar_vuelo(vuelo: Vuelo):
    lista.agregar_vuelo(vuelo.dict())
    return {"mensaje": "Vuelo agregado"}

@app.post("/vuelos/emergencia")
def agregar_emergencia(vuelo: Vuelo):
    lista.agregar_emergencia(vuelo.dict())
    return {"mensaje": "Vuelo de emergencia agregado"}

@app.post("/vuelos/insertar/{posicion}")
def insertar_en_posicion(posicion: int, vuelo: Vuelo):
    lista.insertar_en_posicion(vuelo.dict(), posicion)
    return {"mensaje": f"Vuelo insertado en posición {posicion}"}

@app.delete("/vuelos/{posicion}")
def eliminar_vuelo(posicion: int):
    vuelo = lista.extraer_vuelo(posicion)
    return {"mensaje": "Vuelo eliminado", "vuelo": vuelo}

@app.put("/vuelos/mover")
def mover_vuelo(origen: int, destino: int):
    resultado = lista.cambiar_posicion(origen, destino)
    return {"mensaje": "Movimiento exitoso" if resultado else "Movimiento inválido"}

@app.get("/vuelos/")
def obtener_vuelos():
    return lista.mostrar_vuelos()

@app.get("/vuelos/proximo")
def obtener_mas_proximo():
    return lista.obtener_mas_proximo()

@app.get("/vuelos/ultimo")
def obtener_ultimo():
    return lista.obtener_ultimo()

@app.get("/vuelos/total")
def obtener_total():
    return {"total": lista.contador}
