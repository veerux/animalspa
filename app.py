from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db
from models.user import User
from resources.service import ServiceListResource, ServiceResource, ServicePublishResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)
    return app


def register_extensions(app):
    db.init_app(app)
    migrate = Migrate(app, db)


def register_resources(app):
    api = Api(app)
    api.add_resource(ServiceListResource, '/services')
    api.add_resource(ServiceResource, '/services/<int:service_id>')
    api.add_resource(ServicePublishResource, '/services/<int:service_id>/publish')


if __name__ == '__main__':
    app = create_app()
    app.run()
