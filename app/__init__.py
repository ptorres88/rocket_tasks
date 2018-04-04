from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import config

# general access for the db
db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    db.init_app(app)

    # for all runtime routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .api_v1_0 import api as api_v1_0_blueprint
    app.register_blueprint(api_v1_0_blueprint, url_prefix='/api/v1.0')
    return app
