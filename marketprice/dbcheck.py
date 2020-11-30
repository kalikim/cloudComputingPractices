from flask import jsonify
from flask_restful import Resource
from influxdb import DataFrameClient


class influxDatabaseC(Resource):
    """
    This is for checking the Influx databases available in your setup
    """

    def get(self):
        """
        1. Create influx database instance
        2. Run command to check for databases available in your influxdb environment

        :return: dictionary of databases available
        """
        client = DataFrameClient(host='localhost', port=8086)
        print('list of databases')
        print(client.get_list_database())

        return jsonify(client.get_list_database())
