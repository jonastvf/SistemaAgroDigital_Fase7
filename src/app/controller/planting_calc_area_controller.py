import os

from app.db.connection.sql_alchemy import SqlAlchemyBuilder
from app.services.planting_service import PlantingService


class PlantingCalcAreaController:
    sql_server   = os.getenv('MYSQL_HOST')
    sql_database = os.getenv('MYSQL_DATABASE')
    db_builder = SqlAlchemyBuilder(sql_server, sql_database)
    session_local = db_builder.get_session()

    def get_cultures(self):
        return PlantingService.get_cultures(self.session_local())

    def get_calcs(self):
        return PlantingService.get_calcs(self.session_local())