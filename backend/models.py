from database import Base
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# tabla intermedia para relacion N:M juegos - generos

juegos_generos = Table(
    "juegos_generos",
    Base.metadata,
    Column("juego_id", ForeignKey("juegos.id"), primary_key=True),
    Column("genero_id", ForeignKey("generos.id"), primary_key=True),
)

# tablas de catalogo 1:N


class Estado(Base):
    __tablename__ = "estados"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    juegos = relationship("Juego", back_populates="estado")


class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    juegos = relationship("Juego", back_populates="categoria")


class Opinion(Base):
    __tablename__ = "opiniones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    juegos = relationship("Juego", back_populates="opinion")


class Genero(Base):
    __tablename__ = "generos"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    juegos = relationship("Juego", secondary=juegos_generos, back_populates="generos")


# <<< TABLA PRINCIPAL >>>
class Juego(Base):
    __tablename__ = "juegos"
    id = Column(String, primary_key=True)  # Usamos String por que en SQL es UUID
    titulo = Column(String, nullable=False)
    duracion_horas = Column(Numeric(5, 1), nullable=True)
    puntuacion = Column(Numeric(3, 1), nullable=True)
    notas = Column(String, nullable=True)
    activo = Column(Boolean, default=True)
    creado_en = Column(DateTime(timezone=True), server_default=func.now())
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())

    # foraneas
    estado_id = Column(Integer, ForeignKey("estados.id"))
    categoria_id = Column(Integer, ForeignKey("categorias.id"))
    opinion_id = Column(Integer, ForeignKey("opiniones.id"))
    # usuario_id = Column(String, ForeignKey("perfiles.id"))
    # esta comentado hasta hacer el login

    # Relaciones
    estado = relationship("Estado", back_populates="juegos")
    categoria = relationship("Categoria", back_populates="juegos")
    opinion = relationship("Opinion", back_populates="juegos")
    generos = relationship("Genero", secondary=juegos_generos, back_populates="juegos")
