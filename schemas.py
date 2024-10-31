# schemas.py
from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional, Literal

class UsuarioCreate(BaseModel):
    nombre_usuario: str
    correo: EmailStr
    contraseña: str

class CategoriaCreate(BaseModel):
    nombre: str
    descripcion: Optional[str]
    color: Optional[str]

class ActividadCreate(BaseModel):
    titulo: str
    prioridad: Literal['alta', 'media', 'baja']
    estado: Literal['pendiente', 'en_progreso', 'completada', 'cancelada']
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    categoria_id: int

class RecordatorioCreate(BaseModel):
    titulo: str
    fecha_hora: datetime
    repeticion: Optional[Literal['diaria', 'semanal', 'mensual', 'anual', 'ninguna']] = 'ninguna'
    estado: Optional[Literal['activo', 'inactivo']] = 'activo'
    nota_adicional: Optional[str]
    actividad_id: int
