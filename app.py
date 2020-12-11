from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extensions import db
from resources.user import UserListResource
from resources.service import ServiceListResource, ServiceResource, ServicePublishResource
from resources.reservation import ReservationListResource, ReservationResource, ReservationPublishResource

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
    api.add_resource(UserListResource, '/users')
    api.add_resource(ServiceListResource, '/services')
    api.add_resource(ServiceResource, '/services/<int:service_id>')
    api.add_resource(ServicePublishResource, '/services/<int:service_id>/publish')
    api.add_resource(ReservationListResource, '/reservations')
    api.add_resource(ReservationResource, '/reservations/<int:service_id>')
    api.add_resource(ReservationPublishResource, '/reservations/<int:service_id>/publish')


if __name__ == '__main__':
    app = create_app()
    app.run()
