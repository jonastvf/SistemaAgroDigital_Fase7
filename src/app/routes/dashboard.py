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

@dashboard_bp.route('/fase-6/visao')
def fase6_visao():
    data = {
        "charts": {
            "training_metrics": "fase6/training_metrics.png",
            "inference_example_1": "fase6/inference_1.png",
            "inference_example_2": "fase6/inference_2.png",
            "inference_example_3": "fase6/inference_3.png",
            "inference_example_6": "fase6/inference_6.png",
            "inference_example_7": "fase6/inference_7.png",
            "map_epochs": "fase6/map_epochs.png",
            "map_models": "fase6/map_models.png",
            "models_table": "fase6/models_table.png",
            "val_box_loss": "fase6/val_box_loss.png",
        },
        "metrics_table": [
            {
                "modelo": "30 Épocas (Pequeno)",
                "map_geral": 0.393,
                "map_banana": 0.687,
                "map_garfo": 0.0999,
                "tamanho_mb": 14.4,
                "tempo_min": 34,
            },
            {
                "modelo": "60 Épocas (Pequeno)",
                "map_geral": 0.513,
                "map_banana": 0.764,
                "map_garfo": 0.262,
                "tamanho_mb": 14.4,
                "tempo_min": 68,
            },
            {
                "modelo": "60 Épocas (Médio)",
                "map_geral": 0.789,
                "map_banana": 0.995,
                "map_garfo": 0.584,
                "tamanho_mb": 42.2,
                "tempo_min": 8,
            },
        ],
        "highlights": [
            "Aumentar de 30 para 60 épocas no YOLOv5s melhorou o mAP geral em cerca de 30%.",
            "O YOLOv5m trouxe o melhor desempenho geral (mAP≈0.79) e quase perfeito para a classe banana (mAP≈0.995).",
            "A classe garfo é mais difícil: o ganho real veio com o modelo médio (mAP≈0.584).",
            "O modelo médio é maior (~42 MB), mas treina rápido (≈8 minutos) em ambiente de GPU (Colab).",
        ],
    }

    return render_template("pages/fase6_visao.html", data=data)

@dashboard_bp.route('/fase-6/parte-2')
def fase6_parte2():
    return render_template('pages/fase6_entrega2.html')