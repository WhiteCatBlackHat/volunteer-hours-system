from flask import Flask
from .extentions import db
from .routes import main_bp

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    app.register_blueprint(main_bp)

    return app