
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class VueloBD(Base):
    __tablename__ = 'vuelos'
    id = Column(Integer, primary_key=True, index=True)
    destino = Column(String)
    hora = Column(String)
    prioridad = Column(String)

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./vuelos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
