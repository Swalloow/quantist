from flask import Flask

from .config import Config


def create_app(config_class=Config):
    # create and configure the app
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config_class)

    # register blueprints
    from . import main, errors, invest, report
    app.register_blueprint(main.bp)
    app.register_blueprint(errors.bp)
    app.register_blueprint(invest.bp)
    app.register_blueprint(report.bp)

    app.add_url_rule('/', endpoint='index')

    return app
