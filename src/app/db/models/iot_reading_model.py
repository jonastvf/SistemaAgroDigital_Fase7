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
