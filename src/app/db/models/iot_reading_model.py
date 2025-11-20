from sqlalchemy import Integer, DateTime, DECIMAL, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.db.models.base_model import BaseModel


class IotReading(BaseModel):
    __tablename__ = "iot_reading"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    humidity: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)
    ph: Mapped[float] = mapped_column(DECIMAL(5, 2), nullable=False)

    phosphorus: Mapped[bool] = mapped_column(Boolean, nullable=False)
    potassium: Mapped[bool] = mapped_column(Boolean, nullable=False)

    pump_on: Mapped[bool] = mapped_column(Boolean, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "humidity": float(self.humidity),
            "ph": float(self.ph),
            "phosphorus": bool(self.phosphorus),
            "potassium": bool(self.potassium),
            "pump_on": bool(self.pump_on),
        }

