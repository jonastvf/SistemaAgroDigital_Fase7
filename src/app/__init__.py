from datetime import datetime

from flask import Flask, send_from_directory


def create_app():
    app = Flask(
        __name__,
        template_folder="view",
        static_folder="assets"
    )

    from .routes import (
        dashboard_bp,
        api_bp
    )
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(api_bp)

    app.config['TEMPLATES_AUTO_RELOAD'] = True

    @app.route('/assets/<path:filename>')
    def serve_assets(filename):
        return send_from_directory("app/assets", filename)

    @app.context_processor
    def inject_globals():
        return {
            "current_year": datetime.utcnow().year,
            "title": "System Agro Digital",
            "menu": [
                {
                    'label': 'Fase 1 -Area de plantio',
                    'url': '/dashboard/fase-1',
                    'sub_item': {
                        'url': '/dashboard/fase-1/statistics',
                        'label': 'Estatísticas'
                    }
                },
                {
                    'label': 'Fase 1 - Previsão do tempo',
                    'url': '/dashboard/fase-1/weather',
                },
                {
                    'label': 'Fase 3 - IOT',
                    'url': '/dashboard/fase-3/iot',
                    'sub_item': {
                        'url': '/dashboard/fase4',
                        'label': 'Gráficos e métricas'
                    }
                },
                {
                    'label': 'Fase 5 - ML',
                    'url': '/dashboard/fase-5/ml'
                },
                {
                    'label': 'Fase 5 - Calculadora AWS',
                    'url': '/dashboard/fase-5/aws'
                },
                {
                    "label": "Fase 6 - Detecção de objetos",
                    "url": '/dashboard/fase-6/visao',
                    "sub_item": {
                        "label": "Comparaçao de pipelines",
                        "url": '/dashboard/fase-6/parte-2'
                    }
                }


            ]
        }

    return app