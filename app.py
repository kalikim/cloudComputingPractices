from flask import Flask, redirect, jsonify, request
from flask_cors import CORS
from flask_restful import Api, Resource
from flask_swagger_ui import get_swaggerui_blueprint
import pandas as pd
from werkzeug.utils import secure_filename

from geoname.geonames import GeoNames

app = Flask(__name__)
CORS(app)
api = Api(app)

### swagger specific ###
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yaml'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "cloudcomputing"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)




api.add_resource(GeoNames, '/')


if __name__ == '__main__':
    app.run()
