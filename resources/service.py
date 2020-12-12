from flask import request
from flask_restful import Resource
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity, jwt_required, jwt_optional
from models.service import Service


class ServiceListResource(Resource):
    def get(self):
        services = Service.get_all_published()
        data = []
        for service in services:
            if service.is_publish is True:
                data.append(service.data())
                return {'data': data}, HTTPStatus.OK

    @jwt_required
    def post(self):
        json_data = request.get_json()
        current_user = get_jwt_identity()
        service = Service(name=json_data['name'], description=json_data['description'], duration=json_data['duration'],
                          user_id=current_user)
        service.save()
        return service.data(), HTTPStatus.CREATED


class ServiceResource(Resource):

    @jwt_optional
    def get(self, service_id):
        service = Service.get_by_id(service_id=service_id)
        if service is None:
            return {'message': 'Service not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()

        if service.is_publish == False and service.user_id != current_user:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN

        return service.data(), HTTPStatus.OK

    @jwt_required
    def put(self, service_id):
        json_data = request.get_json()
        service = Service.get_by_id(service_id=service_id)
        if service is None:
            return {'message': 'Service not found'}, HTTPStatus.NOT_FOUND
        current_user = get_jwt_identity()

        if current_user != service.user_id:
            return {'message': 'Access is not allowed'}, HTTPStatus.FORBIDDEN
        service.name = json_data['name']
        service.description = json_data['description']
        service.duration = json_data['duration']

        service.save()
        return service.data(), HTTPStatus.OK


class ServicePublishResource(Resource):
    def put(self, service_id):
        service = next((service for service in service_list if service.id == service_id), None)
        if service is None:
            return {'message': 'service not found'}, HTTPStatus.NOT_FOUND
        service.is_publish = True
        return {}, HTTPStatus.NO_CONTENT

    def delete(self, service_id):
        service = next((service for service in service_list if service.id == service_id), None)
        if service is None:
            return {'message': 'service not found'}, HTTPStatus.NOT_FOUND
        service.is_publish = False
        return {}, HTTPStatus.NO_CONTENT
