from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from models.reservation import Reservation


class ReservationListResource(Resource):
    def get(self):
        reservations = Reservation.get_all_published()
        data = []
        for reservation in reservations:
            if reservation.is_publish is True:
                data.append(reservation.data())
                return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        reservation = Reservation(name=json_data['name'], pet=json_data['pet'], service=json_data['service'],
                                  user_id=current_user)
        reservation.save()
        return reservation.data(), HTTPStatus.CREATED


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
    def put(self, reservation_id):
        reservation = next((reservation for reservation in reservation_list if reservation.id == reservation_id), None)
        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND
        reservation.is_publish = True
        return {}, HTTPStatus.NO_CONTENT

    def delete(self, reservation_id):
        reservation = next((reservation for reservation in reservation_list if reservation.id == reservation_id), None)
        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND
        reservation.is_publish = False
        return {}, HTTPStatus.NO_CONTENT
