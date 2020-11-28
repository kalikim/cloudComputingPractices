from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint

from geoname.geonames import GeoNames
from marketprice.dbcheck import influxDatabaseC
from marketprice.electricitymarket import ElectricityPrice
from marketprice.writetodb import WriteToDB

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
api.add_resource(ElectricityPrice, '/price')
api.add_resource(WriteToDB, '/writetodb')
api.add_resource(influxDatabaseC, '/database')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
