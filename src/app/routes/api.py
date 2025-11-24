from flask import Blueprint, request, jsonify
import os

from sqlalchemy import select

from app.db.connection.sql_alchemy import SqlAlchemyBuilder
from app.db.models.culture_model import Culture
from app.services.planting_service import PlantingService
from app.services.weather_service import WeatherService
from app.services.iot_service import IotService


api_bp = Blueprint('api', __name__, url_prefix='/api')
SERVICE = PlantingService()
SQL_SERVER = os.getenv('MYSQL_HOST')
SQL_DATABASE = os.getenv('MYSQL_DATABASE')
db_builder = SqlAlchemyBuilder(SQL_SERVER, SQL_DATABASE)
SessionLocal = db_builder.get_session()


@api_bp.route('/teste')
def teste():
    pass


@api_bp.route('/calc-area', methods=['POST'])
def calc_area():
    data = request.get_json()
    response = PlantingService.calc_and_register(
        SessionLocal(),
        data.get('culture'),
        data.get('area')
    )

    return jsonify(response)

@api_bp.route('/culture', methods=['POST'])
def create_culture():
    data = request.get_json()
    response = PlantingService.create_culture(
        SessionLocal(),
        data
    )

    if data.get('status') == 'error':
        return jsonify(response), 500

    return jsonify(response), 201

@api_bp.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get("city")  # /api/weather?city=São Paulo
    result = WeatherService.get_weather_by_city(city)

    status_code = 200 if result["status"] == "success" else 400
    return jsonify(result), status_code

from app.services.aws_alert_service import AwsAlertService

@api_bp.route("/iot/simulate", methods=["POST"])
def simulate_iot():
    session = SessionLocal()

    try:
        last = IotService.get_last_reading(session)
        data = IotService.simulate_reading(previous=last)
        saved = IotService.save_reading(session, data)

        reading = saved.to_dict()
        alert_triggered = False
        alert_messages = []

        if reading["humidity"] < 25:
            alert_messages.append(f"Umidade muito baixa: {reading['humidity']}%")
        if reading["ph"] < 5.5 or reading["ph"] > 8.5:
            alert_messages.append(f"pH fora do ideal: {reading['ph']}")
        if reading["phosphorus"] is False:
            alert_messages.append("Fósforo ausente no solo.")
        if reading["potassium"] is False:
            alert_messages.append("Potássio ausente no solo.")

        # Se houver alertas, dispara um SNS
        if alert_messages:
            alert_triggered = True
            AwsAlertService.publish_alert(
                subject="🚨 Alerta IoT — FarmTech",
                message="\n".join(alert_messages)
            )

        return jsonify({
            "status": "success",
            "alert": alert_triggered,
            "data": reading,
            "messages": alert_messages
        })

    except Exception as e:
        return jsonify({"status": "error", "detail": str(e)}), 500

    finally:
        session.close()


@api_bp.route('/iot/readings')
def get_iot_readings():
    session = SessionLocal()
    return jsonify(IotService.get_readings(session))




