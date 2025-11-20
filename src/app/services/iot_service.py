import random
from datetime import datetime
from app.db.models.iot_reading_model import IotReading
from sqlalchemy import select
from sqlalchemy.orm import Session


class IotService:

    @staticmethod
    def get_last_reading(session: Session) -> IotReading | None:
        return (
            session.query(IotReading)
            .order_by(IotReading.id.desc())
            .first()
        )

    @staticmethod
    def simulate_reading(previous: IotReading | None) -> dict:
        def sim(prev, min_v, max_v, slow: float| int=5, noise: float | int=2):
            prev = float(prev)
            # 80% passo curto, 20% passo mais aleatório
            if random.random() < 0.8:
                new_val = prev + random.uniform(-slow, slow)
            else:
                new_val = prev + random.uniform(-slow * 2, slow * 2)

            new_val += random.uniform(-noise, noise)

            return max(min(new_val, max_v), min_v)

        if previous is None:
            humidity = random.uniform(35, 65)
            ph = random.uniform(5.8, 7.2)
            phosphorus = random.choice([0, 1])
            potassium = random.choice([0, 1])
        else:
            prev_h = float(previous.humidity)
            prev_ph = float(previous.ph)
            prev_p = int(previous.phosphorus)
            prev_k = int(previous.potassium)

            humidity = sim(prev_h, 20, 80, slow=4, noise=1)

            ph = sim(prev_ph, 4.0, 8.0, slow=0.25, noise=0.1)

            if random.random() < 0.15:
                prev_p = 1 - prev_p
            if random.random() < 0.15:
                prev_k = 1 - prev_k

            phosphorus = prev_p
            potassium = prev_k

        pump_on = (
                humidity < 40
                or ph < 6.0
                or ph > 7.5
                or phosphorus == 0
                or potassium == 0
        )

        return {
            "humidity": round(humidity, 2),
            "ph": round(ph, 2),
            "phosphorus": phosphorus,
            "potassium": potassium,
            "pump_on": pump_on,
        }


    @staticmethod
    def save_reading(session: Session, data: dict) -> IotReading:
        reading = IotReading(
            humidity=data["humidity"],
            ph=data["ph"],
            phosphorus=data["phosphorus"],
            potassium=data["potassium"],
            pump_on=data["pump_on"],
            timestamp=datetime.utcnow()
        )

        session.add(reading)
        session.commit()
        session.refresh(reading)
        return reading

    @staticmethod
    def get_readings(session: Session):
        stmt = select(
            IotReading.id,
            IotReading.timestamp,
            IotReading.humidity,
            IotReading.ph,
            IotReading.phosphorus,
            IotReading.potassium,
            IotReading.pump_on
        ).order_by(IotReading.timestamp)

        rows = session.execute(stmt).all()

        return [
            {
                "id": row.id,
                "timestamp": row.timestamp,
                "humidity": row.umidity,
                "ph": row.ph,
                "phosphorus": row.phosphorus,
                "potassium": row.potassium,
                "pump_on": row.pump_on

            }
            for row in rows
        ]
