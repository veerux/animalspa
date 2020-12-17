from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from models.reservation import Reservation
from schemas.reservation import ReservationSchema

reservation_schema = ReservationSchema()
reservation_list_schema = ReservationSchema(many=True)


class ReservationListResource(Resource):
    def get(self):
        reservation = Reservation.get_all_published()
        return reservation_list_schema.dump(reservation), HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        data = reservation_schema.load(data=json_data)
        reservation = Reservation(**data)
        reservation.user_id = current_user
        reservation.save()
        return reservation_schema.dump(reservation), HTTPStatus.CREATED

    @jwt_required
    def patch(self, reservation_id):
        json_data = request.get_json()
        data = reservation_schema.load(data=json_data, partial=('name',))
        reservation = Reservation.get_by_id(reservation_id=reservation_id)
        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        reservation.name = data.get('name') or reservation.name
        reservation.pet = data.get('pet') or reservation.pet
        reservation.service = data.get('service') or reservation.service
        reservation.duration = data.get('duration') or reservation.duration

        reservation.save()
        return reservation_schema.dump(reservation), HTTPStatus.OK


class ReservationResource(Resource):

    @jwt_optional
    def get(self, reservation_id):
        reservation = Reservation.get_by_id(reservation_id=reservation_id)
        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if reservation.is_publish == False and reservation.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        return reservation.data(), HTTPStatus.OK

    @jwt_required
    def put(self, reservation_id):
        json_data = request.get_json()
        reservation = Reservation.get_by_id(reservation_id=reservation_id)
        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        reservation.name = json_data['name']
        reservation.pet = json_data['pet']
        reservation.service = json_data['service']
        reservation.duration = json_data['duration']
        reservation.save()
        return reservation.data(), HTTPStatus.OK

    @jwt_required
    def delete(self, reservation_id):
        reservation = Reservation.get_by_id(reservation_id=reservation_id)
        if reservation is None:
            return {'message': 'Reservation not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        reservation.delete()
        return {}, HTTPStatus.NO_CONTENT


class ReservationPublishResource(Resource):
    @jwt_required
    def put(self, reservation_id):
        reservation = Reservation.get_by_id(reservation_id=reservation_id)
        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        reservation.is_publish = True
        reservation.save()
        return {}, HTTPStatus.NO_CONTENT

    @jwt_required
    def delete(self, reservation_id):
        reservation = Reservation.get_by_id(reservation_id=reservation_id)
        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()
        if current_user != reservation.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        reservation.is_publish = False
        reservation.save()
        return {}, HTTPStatus.NO_CONTENT
