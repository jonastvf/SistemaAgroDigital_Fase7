from flask import Blueprint, render_template
from app.controller.planting_calc_area_controller import PlantingCalcAreaController

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
CONTROLLER = PlantingCalcAreaController()

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

    print(calcs)


    return render_template(
        "pages/calc-area.html",
        sub_title="Cálculo de area de plantio",
        cultures=cultures,
        calcs=calcs
    )