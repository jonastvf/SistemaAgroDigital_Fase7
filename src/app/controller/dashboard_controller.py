import os

from app.db.connection.sql_alchemy import SqlAlchemyBuilder
from app.services.planting_service import PlantingService
from app.services.iot_service import IotService
from flask import current_app
from pathlib import Path
import subprocess
import json

from app.dashboard_phase4.analytics import load_iot_readings, compute_statistics
from app.dashboard_phase4.charts import plot_humidity, plot_ph, plot_pump
from app.dashboard_phase4.ml import forecast_humidity
from app.services.aws_alert_service import AwsAlertService



class DashboardController:
    sql_server   = os.getenv('MYSQL_HOST')
    sql_database = os.getenv('MYSQL_DATABASE')
    db_builder = SqlAlchemyBuilder(sql_server, sql_database)
    session_local = db_builder.get_session()

    def get_cultures(self):
        return PlantingService.get_cultures(self.session_local())

    def get_calcs(self):
        return PlantingService.get_calcs(self.session_local())

    def get_formats(self):
        return PlantingService.get_format_types(self.session_local())

    def get_products(self):
        return PlantingService.get_products(self.session_local())

    def get_statistics(self):
        session = self.session_local()
        try:
            base_dir = Path(current_app.root_path)
            r_dir = base_dir / "r"
            csv_path = r_dir / "dados.csv"

            PlantingService.export_calcs_to_csv(session, csv_path)

            result = subprocess.run(
                ["Rscript", "statistics.R"],
                cwd=r_dir,
                capture_output=True,
                text=True
            )

            if result.returncode != 0:
                current_app.logger.error("Rscript stdout: %s", result.stdout)
                current_app.logger.error("Rscript stderr: %s", result.stderr)
                return {
                    "status": "error",
                    "detail": (
                        f"Erro ao executar R (code {result.returncode}).\n\n"
                        f"STDOUT:\n{result.stdout}\n\nSTDERR:\n{result.stderr}"
                    ),
                }

            raw = result.stdout.strip()
            stats = json.loads(raw)

            return {
                "status": "success",
                "data": stats,
            }

        except Exception as e:
            return {
                "status": "error",
                "detail": str(e),
            }
        finally:
            session.close()

    def get_iot_dashboard(self):
        df = load_iot_readings()

        if len(df) == 0:
            return {'status': 'error', 'message': 'Nenhuma leitura IoT encontrada'}

        stats = compute_statistics(df)
        charts = {
            "humidity": plot_humidity(df),
            "ph": plot_ph(df),
            "pump": plot_pump(df),
        }

        forecast_img, forecast_values = forecast_humidity(df)

        return {
            "stats": stats,
            "charts": charts,
            "forecast_chart": forecast_img,
            "forecast_values": forecast_values
        }
