from flask import Flask
from flask_restful import Api
from resources.service import ServiceListResource, ServiceResource, ServicePublishResource

app = Flask(__name__)
api = Api(app)
api.add_resource(ServiceListResource, '/services')
api.add_resource(ServiceResource, '/services/<int:service_id>')
api.add_resource(ServicePublishResource, '/services/<int:service_id>/publish')
if __name__ == '__main__':
    app.run(port=5000, debug=True)