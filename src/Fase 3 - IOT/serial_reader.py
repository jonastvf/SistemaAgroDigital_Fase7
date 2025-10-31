import serial
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import SensorMPX


# Dados de conexão com o Oracle
username = 'system'
password = 'L3v12345'
dsn = 'localhost:1521/FREE'


# Configuração do SQLAlchemy
engine = create_engine(f'oracle+cx_oracle://{username}:{password}@{dsn}')
Session = sessionmaker(bind=engine)
session = Session()

# Configuração da porta serial
serial_port = '/dev/ttyUSB0'  # ou 'COM3' no Windows
baud_rate = 9600
ser = serial.Serial(serial_port, baud_rate)

# Leitura contínua da porta serial
while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').strip()
        try:
            value = float(line)
            unit_id = 1  # ajuste conforme necessário
            area_id = 1  # ajuste conforme necessário
            sensor = SensorMPX(value=value, unit_id=unit_id, area_id=area_id)
            session.add(sensor)
            session.commit()
            print(f"Dado inserido: {value}")
        except ValueError:
            print(f"Valor inválido recebido: {line}")
