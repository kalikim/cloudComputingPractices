import json

import certifi
import urllib3
from flask import jsonify
from flask_restful import Resource


class GeoNames(Resource):
    """
    This returns Postal codes of Austria
    """

    def get(self):
        """
        1. Connects to Geonames Api via my username and api key
            (Honestly i didnt do much tweak like providing the username and Api key separately)
        2. Return a json file with all postal codes in Austria.
        3. This data is send back to the user via this endpoints
        Further processing can be done. use it the way you want
        :return: JSON with all postal codes in Austria
        """
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())

        url2 = 'http://api.geonames.org/postalCodeSearchJSON?formatted=true&postalcode=9011&maxRows=10&username=kalikimanzi&style=full'
        r = http.request('GET', url2)
        r.status
        data = json.loads(r.data.decode('utf-8'))

        return jsonify(data)
