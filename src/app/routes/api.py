from flask import Blueprint, request, jsonify
import os

from sqlalchemy import select

from app.db.connection.sql_alchemy import SqlAlchemyBuilder
from app.db.models.culture_model import Culture
from app.services.planting_service import PlantingService
api_bp = Blueprint('api', __name__, url_prefix='/api')

SERVICE = PlantingService()
SQL_SERVER = os.getenv('MYSQL_HOST')
SQL_DATABASE = os.getenv('MYSQL_DATABASE')
db_builder = SqlAlchemyBuilder(SQL_SERVER, SQL_DATABASE)
SessionLocal = db_builder.get_session()


@api_bp.route('/teste')
def teste():
    # lista = PlantingService.get_cultures(SessionLocal())
    # print(lista)

    lista = PlantingService.calc_and_register(SessionLocal(), 1, 500)
    return jsonify(lista)


    #
    # try:
    #     with SessionLocal() as session:
    #         stmt = select(Culture)
    #         result = session.scalars(stmt).all()
    #
    #         if not result:
    #             return jsonify({
    #                 'status': 'success',
    #                 'message': "No cultures found",
    #             })
    #
    #         culture_data = [
    #             c.to_dict() if hasattr(c, 'to_dict') else {
    #                 "id": c.id,
    #                 "name": c.name,
    #                 "product_id": c.product_id,
    #                 "format_id": c.format_id,
    #                 "street_size_m": c.street_size_m
    #             }
    #             for c in result
    #         ]
    #
    #         return jsonify({
    #             "status": "success",
    #             "message": f"{len(culture_data)} cultures found",
    #             "data": culture_data
    #         })
    # except Exception as e:
    #     return jsonify({
    #         'status': 'error',
    #         'message': 'Query for cultures failed',
    #         'detail': str(e)
    #     })

@api_bp.route('/calc-area', methods=['POST'])
def calc_area():
    data = request.get_json()
    print(data.get('culture'))
    print('\n')
    print('-'*20)
    print(data.get('area'))

    response = PlantingService.calc_and_register(
        SessionLocal(),
        data.get('culture'),
        data.get('area')
    )


    return jsonify(response)
