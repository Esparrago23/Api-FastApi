# models.py
from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, Date, DateTime, TIMESTAMP
from sqlalchemy.orm import relationship
from database import Base
import enum

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_usuario = Column(String(50), unique=True, index=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP")

class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    descripcion = Column(Text)
    color = Column(String(7))
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))

class Actividad(Base):
    __tablename__ = "actividades"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    prioridad = Column(Enum("alta", "media", "baja"), nullable=False)
    estado = Column(Enum("pendiente", "en_progreso", "completada", "cancelada"), nullable=False)
    fecha_inicio = Column(Date)
    fecha_fin = Column(Date)
    categoria_id = Column(Integer, ForeignKey("categorias.id"))

class Recordatorio(Base):
    __tablename__ = "recordatorios"

    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    fecha_hora = Column(DateTime, nullable=False)
    repeticion = Column(Enum("diaria", "semanal", "mensual", "anual", "ninguna"), default="ninguna")
    estado = Column(Enum("activo", "inactivo"), default="activo")
    nota_adicional = Column(Text)
    actividad_id = Column(Integer, ForeignKey("actividades.id"))
