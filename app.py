from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api
from config import Config
from extensions import db, jwt
from resources.user import UserListResource,UserResource, MeResource,UserServiceListResource,\
    UserReservationListResource
from resources.service import ServiceListResource, ServiceResource, ServicePublishResource
from resources.reservation import ReservationListResource, ReservationResource, ReservationPublishResource
from resources.token import TokenResource, RefreshResource, RevokeResource, black_list


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    register_extensions(app)
    register_resources(app)
    return app


def register_extensions(app):
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    jwt.init_app(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in black_list


def register_resources(app):
    api = Api(app)
    # user
    api.add_resource(UserListResource, '/users')
    api.add_resource(UserResource, '/users/<string:username>')
    api.add_resource(MeResource, '/me')
    api.add_resource(UserServiceListResource, '/users/<string:username>/services')
    api.add_resource(UserReservationListResource, '/users/<string:username>/reservations')
    # services
    api.add_resource(ServiceListResource, '/services')
    api.add_resource(ServiceResource, '/services/<int:service_id>')
    api.add_resource(ServicePublishResource, '/services/<int:service_id>/publish')
    # reservations
    api.add_resource(ReservationListResource, '/reservations')
    api.add_resource(ReservationResource, '/reservations/<int:reservation_id>')
    api.add_resource(ReservationPublishResource, '/reservations/<int:reservation_id>/publish')
    # token
    api.add_resource(TokenResource, '/token')
    api.add_resource(RefreshResource, '/refresh')
    api.add_resource(RevokeResource, '/revoke')


if __name__ == '__main__':
    app = create_app()
    app.run()
