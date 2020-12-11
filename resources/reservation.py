from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.reservation import Reservation, reservation_list


class ReservationListResource(Resource):
    def get(self):
        data = []
        for reservation in reservation_list:
            if reservation.is_publish is True:
                data.append(reservation.data)
                return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()
        reservation = Reservation(name=data['name'], pet=data['pet'], service=data['service'])
        reservation_list.append(reservation)
        return reservation.data, HTTPStatus.CREATED


class ReservationResource(Resource):
    def get(self, reservation_id):
        reservation = next((reservation for reservation in reservation_list if reservation.id == reservation_id and
                            reservation.is_publish == True), None)
        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND
        return reservation.data, HTTPStatus.OK

    def put(self, reservation_id):
        data = request.get_json()
        reservation = next((reservation for reservation in reservation_list if reservation.id == reservation_id), None)
        if reservation is None:
            return {'message': 'reservation not found'}, HTTPStatus.NOT_FOUND
        reservation.name = data['name']
        reservation.description = data['pet']
        reservation.duration = data['service']
        return reservation.data, HTTPStatus.OK


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
