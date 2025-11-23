from flask import Blueprint, render_template, current_app, request, jsonify
from app.controller.dashboard_controller import DashboardController
import json

from app.services.ml_service import MlService

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
CONTROLLER = DashboardController()

@dashboard_bp.route('/')
def index():
    menus = {
        "Calc - Area de Plantio": '/fase1'
    }

    return render_template("pages/dashboard.html", menus=menus)

@dashboard_bp.route('/fase-1')
def phase_one():
    cultures = CONTROLLER.get_cultures()
    calcs = CONTROLLER.get_calcs()
    formats = CONTROLLER.get_formats()
    products = CONTROLLER.get_products()
    return render_template(
        "pages/calc-area.html",
        sub_title="Cálculo de area de plantio",
        cultures=cultures,
        calcs=calcs,
        formats=formats,
        products=products
    )

@dashboard_bp.route('/fase-1/statistics')
def statistics():
    result = CONTROLLER.get_statistics()

    print(result)

    if result["status"] != "success":
        return render_template(
            "pages/statistics.html",
            error=result["detail"],
            stats=None,
        )

    data = result["data"]

    if isinstance(data, dict):
        data = [data]

    return render_template(
        "pages/statistics.html",
        error=None,
        stats=data,
    )

@dashboard_bp.route('/fase-1/weather')
def weather():
    return render_template('pages/weather.html', error=None,)

@dashboard_bp.route('/fase-3/iot')
def iot():
    return render_template('pages/iot.html', error=None)

@dashboard_bp.route('/fase4')
def phase4():
    data = CONTROLLER.get_iot_dashboard()

    return render_template(
        'pages/fase4_dashboard.html',
        data=data
    )

@dashboard_bp.route('/fase-5/ml')
def phase5():
    ml_service = MlService()
    try:
        ml_data = ml_service.load_ml_data()
    except Exception as e:
        ml_data = {}
        print(f"Erro ao carregar dados: {e}")

    print(ml_data)

    return render_template("pages/fase5_ml.html", ml_data=ml_data)

@dashboard_bp.route('/fase-5/aws')
def phase5_aws():
    return render_template('pages/aws-calculator.html')