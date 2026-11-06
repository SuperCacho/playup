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


class JuegoCreate(JuegoBase):
    pass


class JuegoResponse(JuegoBase):
    id: str
    activo: bool
    creado_en: datetime
