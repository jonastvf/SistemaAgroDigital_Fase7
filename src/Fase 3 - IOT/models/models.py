from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue

Base = declarative_base()

class UnidadeMedida(Base):
    __tablename__ = 'unidade_medida'

    id_unidade_medida = Column(Integer, primary_key=True)
    name_unidade_medida = Column(String(50), nullable=False)

    sensores_mpx = relationship("SensorMPX", back_populates="unidade_medida")


class AreaCapturada(Base):
    __tablename__ = 'area_capturada'

    id_area_capturada = Column(Integer, primary_key=True, server_default=FetchedValue())
    nm_area_capturada = Column(String(100), nullable=False)

    sensores_mpx = relationship("SensorMPX", back_populates="area_capturada")


class SensorMPX(Base):
    __tablename__ = 'sensor_mpx'

    id_sensor_mpx = Column(Integer, primary_key=True, autoincrement=True)
    id_unidade_medida = Column(Integer, ForeignKey('unidade_medida.id_unidade_medida'))
    id_area_capturada = Column(Integer, ForeignKey('area_capturada.id_area_capturada'))
    vlr_sensor_mpx = Column(Float, nullable=False)
    dt_hr_sensor_mpx = Column(DateTime, nullable=False)

    unidade_medida = relationship("UnidadeMedida", back_populates="sensores_mpx")
    area_capturada = relationship("AreaCapturada", back_populates="sensores_mpx")
