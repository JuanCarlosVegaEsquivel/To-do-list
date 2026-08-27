# main.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, Integer, String, Boolean
from pydantic import BaseModel
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

# 1. La "direccion" de conexion a tu base de datos
# Formato: mysql+pymysql://usuario:contraseña@servidor/nombre_basededatos
DATABASE_URL = "mysql+pymysql://root:contrasenia@localhost/todo_list"

# 2. El "engine" es lo que realmente maneja la conexion con MySQL
engine = create_engine(DATABASE_URL)

# 3. SessionLocal es como una "conversacion" que abrimos con la base de datos
# cada vez que queremos leer o escribir algo
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. base es la clase de la que van a heredar nuestro "modelos"
# (los modelos son las tablas, representadas como clases de Python)
Base = declarative_base()

# Este modelo representa la tabla "tareas" que ya creaste en MySQL
# Cada atributo de la clase = una columna de la tabla
class Tarea(Base):
    __tablename__ = "tareas" # el nombre exacto de la tabla en MySQL

    id= Column(Integer, primary_key=True, index=True)
    titulo = Column(String(255), nullable=False)
    completada = Column(Boolean, default=False) 

# Lo que el cliente (frontend) nos manda cuando CREA una tarea nueva
class TareaCreate(BaseModel):
    titulo: str

# Lo que la API nos devuelve cuando le pedimos tareas
class TareaResponse(BaseModel):
    id: int
    titulo: str
    completada: bool

    class Config:
        from_attributes = True # permite convertir un objeto SQLAlchemy a este schema automaticamente

# Esto crea la tabla de MySQL si no existe (viendo el modelo Tarea de arriba)
# Como ya la creaste a mano, esto no hace nada nuevo, pero es una buena practica
Base.metadata.create_all(bind=engine)

#Creamos la aplicacion de FastAPI
app = FastAPI()

# Esta funcion abre una sesion de base de datos, la "presta" a la ruta que la necesite
# y se asegura de cerrarla cuando termina (aunque haya un error)
def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()

# RUTA 1: obtener TODAS las tareas
@app.get("/tareas", response_model=list[TareaResponse])
def obtener_tareas(db: Session = Depends(get_db)):
    tareas = db.query(Tarea).all()
    return tareas

# RUTA 2: crear una tarea nueva
@app.post("/tareas", response_model=TareaResponse)
def crear_tarea(tarea: TareaCreate, db: Session = Depends(get_db)):
    nueva_tarea = Tarea(titulo=tarea.titulo) # creamos el objeto en memoria
    db.add(nueva_tarea) #lo marcamos para guardar
    db.commit() # confirmamos el cambio en la base de datos de verdad
    db.refresh(nueva_tarea) #actualizamos el objeto con el id que MySQL le asigno
    return nueva_tarea

# RUTA 3: marcar una tarea como completada (o volverla a marcar como pendiente)
@app.put("/tareas/{tarea_id}", response_model=TareaResponse)
def actualizar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()

    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    tarea.completada = not tarea.completada # invierte el valor: True pasa a False y viceversa
    db.commit()
    db.refresh(tarea)
    return tarea

# RUTA 4: borrar una tarea
@app.delete("/tareas/{tarea_id}")
def borrar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()

    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    db.delete(tarea)
    db.commit()
    return {"mensaje": "Tarea eliminada correctamente"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # "*" = permite peticiones desde cualquier origen
    allow_methods=["*"], # permite todos los metodos (GET, POST, PUT, DELETE)
    allow_headers=["*"], # permite todos los headers
)
