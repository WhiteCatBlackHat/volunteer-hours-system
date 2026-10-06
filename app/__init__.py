from flask import Flask
from .extensions import db, migrate
from .routes import main_bp
from . import models

def create_app(config_object='config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_object)

    db.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(main_bp)

    return app