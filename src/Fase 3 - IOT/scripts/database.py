import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, SensorMPX, UnidadeMedida, AreaCapturada
from datetime import datetime

# Dados de conexão com o Oracle
username = 'system'
password = 'L3v12345'
dsn = 'localhost:1521/FREE'

# Criação do engine
engine = create_engine(f'oracle+cx_oracle://{username}:{password}@{dsn}')

# Criação das tabelas
Base.metadata.create_all(engine)

# Sessão para inserir dados de exemplo
Session = sessionmaker(bind=engine)
session = Session()

# Dados de exemplo
unit = UnidadeMedida(name_unidade_medida='Celsius')
area = AreaCapturada(nm_area_capturada='Área 1')
sensor = SensorMPX(
    vlr_sensor_mpx=25.3,
    dt_hr_sensor_mpx=datetime.now(),
    unidade_medida=unit,
    area_capturada=area
)

session.add_all([unit, area, sensor])
session.commit()

print("Tabelas criadas e dados de exemplo inseridos com sucesso.")
