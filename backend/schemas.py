from datetime import datetime

from pydantic import BaseModel


class JuegoBase(BaseModel):
    titulo: str
    duracion_horas: float | None = None
    puntuacion: float | None = None
    notas: str | None = None
    estado_id: int | None = None
    categoria_id: int | None = None
    opinion_id: int | None = None
    portada_url: str | None = None
    usuario_id: str | None = None


class JuegoCreate(JuegoBase):
    generos: list[int] | None = []


class JuegoResponse(JuegoBase):
    id: str
    activo: bool
    creado_en: datetime
    generos: list[dict] | None = []


class UserRegister(BaseModel):
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str
