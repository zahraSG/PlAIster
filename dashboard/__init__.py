from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from dashboard.config import Config


db=SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()


def create_app(config_class= Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from dashboard.main.routes import main
    from dashboard.users.routes import users
    from dashboard.device.routes import device
    from dashboard.plots.routes import plots
    from dashboard.charts.routes import charts

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(device)
    app.register_blueprint(plots)
    app.register_blueprint(charts)

    return app
