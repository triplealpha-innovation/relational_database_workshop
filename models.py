from __future__ import annotations
from internal_modules import Base
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy import ForeignKey
from typing import List
import datetime

class Cliente(Base):
    __tablename__ = 'cliente'

    id: Mapped[str] = mapped_column(primary_key=True, unique=True)
    nombre: Mapped[str]
    apellido: Mapped[str]

    ventas: Mapped[List[Venta]] = relationship(back_populates='cliente')

class Articulo(Base):
    __tablename__ = 'articulo'

    producto: Mapped[str] = mapped_column(primary_key=True)
    precio: Mapped[float]

    ventas: Mapped[List[Venta]] = relationship(back_populates='articulo')

class Venta(Base):
    __tablename__ = 'venta'

    fecha: Mapped[datetime.datetime] = mapped_column(primary_key=True, default=datetime.datetime.now())
    cliente_id: Mapped[int] = mapped_column(ForeignKey('cliente.id'), primary_key=True)
    articulo_id: Mapped[int] = mapped_column(ForeignKey('articulo.producto'), primary_key=True)
    cantidad: Mapped[int]

    cliente: Mapped[Cliente] = relationship(back_populates='ventas')
    articulo: Mapped[Articulo] = relationship(back_populates='ventas')

