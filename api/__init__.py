import os
import sys
import socket
from flask import Flask
from flasgger import Swagger

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from api.config.swagger import template, swagger_config
from api.app import bank
from api.models.database import create_tables
from api.insert_db import create_customers

ip_address = socket.gethostbyname(socket.gethostname())
create_tables()
create_customers()

def create_app(test_config=None):
    # create and configure app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY='dev')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_mapping(
            SWAGGER={
                'title': "API",
                'uiversion': 3
            }
        )

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.register_blueprint(bank)
    Swagger(app, config=swagger_config, template=template)

    # with app.test_request_context("/"):
    # global ip_address
    # ip_address = request.remote_addr
    # @app.route("/")
    # def hello():
    #     return "Hello, world"

    return app
