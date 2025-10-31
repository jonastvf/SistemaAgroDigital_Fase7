from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import SensorMPX, UnidadeMedida, AreaCapturada


# Dados de conexão com o Oracle
username = 'system'
password = 'L3v12345'
dsn = 'localhost:1521/FREE'


engine = create_engine(f'oracle+cx_oracle://{username}:{password}@{dsn}')
Session = sessionmaker(bind=engine)
session = Session()

# SensorMPX
def create_sensor(value, unit_id, area_id):
    sensor = SensorMPX(value=value, unit_id=unit_id, area_id=area_id)
    session.add(sensor)
    session.commit()
    return sensor

def read_sensor(sensor_id):
    return session.query(SensorMPX).filter_by(id=sensor_id).first()

def update_sensor(sensor_id, value=None, unit_id=None, area_id=None):
    sensor = session.query(SensorMPX).filter_by(id=sensor_id).first()
    if value is not None:
        sensor.value = value
    if unit_id is not None:
        sensor.unit_id = unit_id
    if area_id is not None:
        sensor.area_id = area_id
    session.commit()
    return sensor

def delete_sensor(sensor_id):
    sensor = session.query(SensorMPX).filter_by(id=sensor_id).first()
    session.delete(sensor)
    session.commit()

# UnidadeMedida
def create_unit(name):
    unit = UnidadeMedida(name=name)
    session.add(unit)
    session.commit()
    return unit

def read_unit(unit_id):
    return session.query(UnidadeMedida).filter_by(id=unit_id).first()

def update_unit(unit_id, name=None):
    unit = session.query(UnidadeMedida).filter_by(id=unit_id).first()
    if name:
        unit.name = name
    session.commit()
    return unit

def delete_unit(unit_id):
    unit = session.query(UnidadeMedida).filter_by(id=unit_id).first()
    session.delete(unit)
    session.commit()

# AreaCapturada
def create_area(name):
    area = AreaCapturada(name=name)
    session.add(area)
    session.commit()
    return area

def read_area(area_id):
    return session.query(AreaCapturada).filter_by(id=area_id).first()

def update_area(area_id, name=None):
    area = session.query(AreaCapturada).filter_by(id=area_id).first()
    if name:
        area.name = name
    session.commit()
    return area

def delete_area(area_id):
    area = session.query(AreaCapturada).filter_by(id=area_id).first()
    session.delete(area)
    session.commit()
