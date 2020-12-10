from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.service import Service, service_list


class ServiceListResource(Resource):
    def get(self):
        data = []
        for service in service_list:
            if service.is_publish is True:
                data.append(service.data)
                return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()
        service = Service(name=data['name'], description=data['description'], duration=data['duration'])
        service_list.append(service)
        return service.data, HTTPStatus.CREATED


class ServiceResource(Resource):
    def get(self, service_id):
        service = next((service for service in service_list if service.id == service_id and service.is_publish == True),
                       None)
        if service is None:
            return {'message': 'service not found'}, HTTPStatus.NOT_FOUND
        return service.data, HTTPStatus.OK

    def put(self, service_id):
        data = request.get_json()
        service = next((service for service in service_list if service.id == service_id), None)
        if service is None:
            return {'message': 'service not found'}, HTTPStatus.NOT_FOUND
        service.name = data['name']
        service.description = data['description']
        service.duration = data['duration']
        return service.data, HTTPStatus.OK


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
