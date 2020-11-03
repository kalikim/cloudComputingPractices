import json

import certifi
import urllib3
from flask import jsonify
from flask_restful import Resource


class GeoNames(Resource):
    def get(self):
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())

        url2 = 'http://api.geonames.org/postalCodeSearchJSON?formatted=true&postalcode=9011&maxRows=10&username=kalikimanzi&style=full'
        r = http.request('GET', url2)
        r.status
        data = json.loads(r.data.decode('utf-8'))

        return jsonify(data)


class CurlPractice(Resource):
    def get(self):
        name = {"myname": "my name is kali kimanzi"}
        return jsonify(name)
