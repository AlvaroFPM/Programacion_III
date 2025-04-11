# cola.py
from models import MisionPersonaje
from sqlalchemy.orm import Session

class ColaMisiones:
    def __init__(self, personaje_id: int, db: Session):
        self.personaje_id = personaje_id
        self.db = db

    def enqueue(self, mision_id: int):
        orden = self.size()
        nueva = MisionPersonaje(
            personaje_id=self.personaje_id,
            mision_id=mision_id,
            orden=orden
        )
        self.db.add(nueva)
        self.db.commit()

    def dequeue(self):
        primera = self.first()
        if primera:
            self.db.delete(primera)
            self.db.commit()
            # Reajustar orden
            self.reordenar()
            return primera
        return None

    def first(self):
        return (
            self.db.query(MisionPersonaje)
            .filter_by(personaje_id=self.personaje_id)
            .order_by(MisionPersonaje.orden)
            .first()
        )

    def is_empty(self):
        return self.size() == 0

    def size(self):
        return (
            self.db.query(MisionPersonaje)
            .filter_by(personaje_id=self.personaje_id)
            .count()
        )

    def reordenar(self):
        items = (
            self.db.query(MisionPersonaje)
            .filter_by(personaje_id=self.personaje_id)
            .order_by(MisionPersonaje.orden)
            .all()
        )
        for i, item in enumerate(items):
            item.orden = i
        self.db.commit()

    def get_all(self):
        return (
            self.db.query(MisionPersonaje)
            .filter_by(personaje_id=self.personaje_id)
            .order_by(MisionPersonaje.orden)
            .all()
        )
