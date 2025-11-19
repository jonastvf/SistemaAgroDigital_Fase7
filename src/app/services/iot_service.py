import random
from datetime import datetime
from app.db.models.iot_reading_model import IotReading


class IotService:

    @staticmethod
    def simulate_reading(previous=None):
        # 1) Valores base (caso seja o primeiro registro)
        if previous is None:
            prev_h = 55
            prev_ph = 6.8
            prev_p = 1
            prev_k = 1
        else:
            prev_h = previous.humidity
            prev_ph = previous.ph
            prev_p = previous.phosphorus
            prev_k = previous.potassium

        # --- Simulador 80/20 ---
        def sim(prev, minv, maxv, slow, rand):
            if random.random() < 0.8:
                new_val = prev + random.uniform(-slow, slow)
            else:
                new_val = prev + random.uniform(-rand, rand)
            return max(min(new_val, maxv), minv)

        humidity = sim(prev_h, 20, 80, 2, 8)
        ph = sim(prev_ph, 5.5, 7.5, 0.1, 0.5)

        # nutrientes mudam com baixa frequência
        phosphorus = 1 if random.random() > 0.1 else 0
        potassium = 1 if random.random() > 0.1 else 0

        # --- LÓGICA DA BOMBA ---
        pump_on = (
            humidity < 30
            or ph < 6 or ph > 8
            or phosphorus == 0
            or potassium == 0
        )

        return {
            "timestamp": datetime.utcnow(),
            "humidity": round(humidity, 2),
            "ph": round(ph, 2),
            "phosphorus": phosphorus,
            "potassium": potassium,
            "pump_on": pump_on,
        }

    @staticmethod
    def save_reading(session, data: dict):
        reading = IotReading(**data)
        session.add(reading)
        session.commit()
        session.refresh(reading)
        return reading

    @staticmethod
    def get_last_reading(session):
        return session.query(IotReading).order_by(IotReading.id.desc()).first()
