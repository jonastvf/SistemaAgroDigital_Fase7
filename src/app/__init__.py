from datetime import datetime

from flask import Flask

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

    @app.context_processor
    def inject_globals():
        return {
            "current_year": datetime.utcnow().year,
            "title": "System Agro Digital"
        }

    return app