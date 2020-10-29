from flask_restful import Resource
from flask import jsonify, request
import pandas as pd
from io import StringIO
import requests
import numpy as np
import urllib3
from urllib3 import request
import certifi
import json



class GeoNames(Resource):
    def get(self):
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())
        url = 'https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/MPD/MapServer/2/query?where=1%3D1&outFields=*&outSR=4326&f=json'
        url2='http://api.geonames.org/postalCodeSearchJSON?formatted=true&postalcode=9011&maxRows=10&username=kalikimanzi&style=full'
        r = http.request('GET', url2)
        r.status
        data = json.loads(r.data.decode('utf-8'))


        # s = requests.get(url2).text
        # df = pd.read_csv(StringIO(s))

        return jsonify(data)








