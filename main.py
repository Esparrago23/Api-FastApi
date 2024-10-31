# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models, schemas, auth

app = FastAPI()

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Registro de usuario
@app.post("/register", response_model=schemas.UsuarioCreate)
def register(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    hashed_password = auth.get_password_hash(user.contraseña)
    db_user = models.Usuario(nombre_usuario=user.nombre_usuario, correo=user.correo, contraseña=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Inicio de sesión
@app.post("/login")
def login(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.Usuario).filter(models.Usuario.correo == user.correo).first()
    if not db_user or not auth.verify_password(user.contraseña, db_user.contraseña):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = auth.create_access_token(data={"sub": db_user.nombre_usuario})
    return {"access_token": access_token, "token_type": "bearer"}

# CRUD para Categorías

@app.post("/categorias/", response_model=schemas.CategoriaCreate)
def create_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.get("/categorias/", response_model=list[schemas.CategoriaCreate])
@app.get("/categorias/{categoria_id}", response_model=schemas.CategoriaCreate)
def read_categoria(categoria_id: int = None, db: Session = Depends(get_db)):
    if categoria_id:
        db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
        if db_categoria is None:
            raise HTTPException(status_code=404, detail="Categoria not found")
        return db_categoria
    return db.query(models.Categoria).all()  # Retorna todas las categorías

@app.put("/categorias/{categoria_id}", response_model=schemas.CategoriaCreate)
def update_categoria(categoria_id: int, categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
    
    for key, value in categoria.dict().items():
        setattr(db_categoria, key, value)
    
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

@app.delete("/categorias/{categoria_id}", status_code=204)
def delete_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria not found")
    
    db.delete(db_categoria)
    db.commit()
    return

# CRUD para Actividades

@app.post("/actividades/", response_model=schemas.ActividadCreate)
def create_actividad(actividad: schemas.ActividadCreate, db: Session = Depends(get_db)):
    db_actividad = models.Actividad(**actividad.dict())
    db.add(db_actividad)
    db.commit()
    db.refresh(db_actividad)
    return db_actividad

@app.get("/actividades/", response_model=list[schemas.ActividadCreate])
@app.get("/actividades/{actividad_id}", response_model=schemas.ActividadCreate)
def read_actividad(actividad_id: int = None, db: Session = Depends(get_db)):
    if actividad_id:
        db_actividad = db.query(models.Actividad).filter(models.Actividad.id == actividad_id).first()
        if db_actividad is None:
            raise HTTPException(status_code=404, detail="Actividad not found")
        return db_actividad
    return db.query(models.Actividad).all()  # Retorna todas las actividades

@app.put("/actividades/{actividad_id}", response_model=schemas.ActividadCreate)
def update_actividad(actividad_id: int, actividad: schemas.ActividadCreate, db: Session = Depends(get_db)):
    db_actividad = db.query(models.Actividad).filter(models.Actividad.id == actividad_id).first()
    if db_actividad is None:
        raise HTTPException(status_code=404, detail="Actividad not found")
    
    for key, value in actividad.dict().items():
        setattr(db_actividad, key, value)
    
    db.commit()
    db.refresh(db_actividad)
    return db_actividad

@app.delete("/actividades/{actividad_id}", status_code=204)
def delete_actividad(actividad_id: int, db: Session = Depends(get_db)):
    db_actividad = db.query(models.Actividad).filter(models.Actividad.id == actividad_id).first()
    if db_actividad is None:
        raise HTTPException(status_code=404, detail="Actividad not found")
    
    db.delete(db_actividad)
    db.commit()
    return

# CRUD para Recordatorios

@app.post("/recordatorios/", response_model=schemas.RecordatorioCreate)
def create_recordatorio(recordatorio: schemas.RecordatorioCreate, db: Session = Depends(get_db)):
    db_recordatorio = models.Recordatorio(**recordatorio.dict())
    db.add(db_recordatorio)
    db.commit()
    db.refresh(db_recordatorio)
    return db_recordatorio

@app.get("/recordatorios/", response_model=list[schemas.RecordatorioCreate])
@app.get("/recordatorios/{recordatorio_id}", response_model=schemas.RecordatorioCreate)
def read_recordatorio(recordatorio_id: int = None, db: Session = Depends(get_db)):
    if recordatorio_id:
        db_recordatorio = db.query(models.Recordatorio).filter(models.Recordatorio.id == recordatorio_id).first()
        if db_recordatorio is None:
            raise HTTPException(status_code=404, detail="Recordatorio not found")
        return db_recordatorio
    return db.query(models.Recordatorio).all()  # Retorna todos los recordatorios

@app.put("/recordatorios/{recordatorio_id}", response_model=schemas.RecordatorioCreate)
def update_recordatorio(recordatorio_id: int, recordatorio: schemas.RecordatorioCreate, db: Session = Depends(get_db)):
    db_recordatorio = db.query(models.Recordatorio).filter(models.Recordatorio.id == recordatorio_id).first()
    if db_recordatorio is None:
        raise HTTPException(status_code=404, detail="Recordatorio not found")
    
    for key, value in recordatorio.dict().items():
        setattr(db_recordatorio, key, value)
    
    db.commit()
    db.refresh(db_recordatorio)
    return db_recordatorio

@app.delete("/recordatorios/{recordatorio_id}", status_code=204)
def delete_recordatorio(recordatorio_id: int, db: Session = Depends(get_db)):
    db_recordatorio = db.query(models.Recordatorio).filter(models.Recordatorio.id == recordatorio_id).first()
    if db_recordatorio is None:
        raise HTTPException(status_code=404, detail="Recordatorio not found")
    
    db.delete(db_recordatorio)
    db.commit()
    return
