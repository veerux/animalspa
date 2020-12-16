from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_optional, get_jwt_identity, jwt_required
from http import HTTPStatus
from utils import hash_password
from models.user import User
from models.service import Service
from models.reservation import Reservation
from schemas.user import UserSchema
from schemas.service import ServiceSchema
from schemas.reservation import ReservationSchema
from webargs import fields
from webargs.flaskparser import use_kwargs


user_schema = UserSchema()
user_public_schema = UserSchema(exclude=('email', ))
service_list_schema = ServiceSchema(many=True)
reservation_list_schema = ReservationSchema(many=True)


class UserListResource(Resource):
    def post(self):

        json_data = request.get_json()
        data = user_schema.load(data=json_data)

        if User.get_by_username(data.get('username')):
            return {'message': 'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(data.get('email')):
            return {'message': 'email already used'}, HTTPStatus.BAD_REQUEST

        user = User(**data)
        user.save()

        return user_schema.dump(user), HTTPStatus.CREATED


class UserResource(Resource):
    @jwt_optional
    def get(self, username):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'user not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user == user.id:
            data = user_schema.dump(user)
        else:
            data = user_public_schema.dump(user)
        return data, HTTPStatus.OK


class UserServiceListResource(Resource):
    @jwt_optional
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self, username, visibility):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'
        services = Service.get_all_by_user(user_id=user.id, visibility=visibility)
        return service_list_schema.dump(services), HTTPStatus.OK


class UserReservationListResource(Resource):
    @jwt_optional
    @use_kwargs({'visibility': fields.Str(missing='public')})
    def get(self, username, visibility):
        user = User.get_by_username(username=username)
        if user is None:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user == user.id and visibility in ['all', 'private']:
            pass
        else:
            visibility = 'public'
        reservations = Reservation.get_all_by_user(user_id=user.id, visibility=visibility)
        return reservation_list_schema.dump(reservations), HTTPStatus.OK


class MeResource(Resource):
    @jwt_required
    def get(self):
        user = User.get_by_id(id=get_jwt_identity())
        return user_schema.dump(user), HTTPStatus.OK
