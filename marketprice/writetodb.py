import json

import certifi
import flask
import pandas as pd
import urllib3
from flask import jsonify
from flask_restful import Resource
from influxdb import DataFrameClient


class WriteToDB(Resource):
    """
    Contains the process of writing data from Api to Influx DATABASE
    """

    def get(self):
        """
                1. This end point receives two parameters
                    1.1. startTimestamp
                    1.2. endTimestamp

                2. combines the two parameters with awattar url to form awattar url
                3. an API call is made to https://api.awattar.at
                4. Awattar returns a json data
                5.Json data is converted to Pandas Dataframe inorder to interact with it further,
                6.Further processing done include
                    6.1. Converting the timestamps to dateTime format
                    6.2 setting startTimestamp as the index
                7. Creating influxdb client
                8. Switching to the database to work with in my case i chose 'TestingDb'
                9. Writing the data to the database in a try exception clause



                :return: "sucess " or "Fail"
                """
        # getting the two parameters from the get request
        startTimestamp = int(flask.request.args.get("startTimestamp"))
        endTimestamp = int(flask.request.args.get("endTimestamp"))

        # Test print the two value in the console to confirm i have
        # the right value
        print(startTimestamp)
        print(endTimestamp)

        # then i proceed with connection pooling which is handled by
        # urllib pool manager
        http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())

        # Proceed to define the Url which will be called , you notice i have incorporated
        # the start and end parameters from the get request
        url = 'https://api.awattar.at/v1/marketdata?start=' + str(startTimestamp) + '&end=' + str(endTimestamp)
        print(url)

        # this makes the request with external world to the Api world
        api_request = http.request('GET', url)
        api_request.status

        # 200 status means the connection was successful there are many http
        # codes with different meaning visit wikipedia for all codes
        # using this link https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
        print(api_request.status)

        # The next step is decode the data into json into a way i can handle it with python
        data = json.loads(api_request.data.decode('utf-8'))

        # To process the data further with python data analytics library pandas
        # for easy processing i convert it into pandas dataframe
        df_apidata = pd.json_normalize(data, "data")
        # df_apidata.drop(columns=['end_timestamp'])

        # converted_df = pd.to_datetime(df_apidata['start_timestamp'], unit='ms')
        df_marketprice = df_apidata[['marketprice', 'unit']]
        df_apidata['start_timestamp'] = pd.to_datetime(
            df_apidata['start_timestamp'],
            unit='ms'
        )
        # df_apidata['end_timestamp'] = pd.to_datetime(
        #     df_apidata['end_timestamp'],
        #     unit='ms'
        # )
        df_apidata.set_index('start_timestamp', inplace=True)
        print(df_apidata.head(5))
        # timeValues = df_apidata[['start_timestamp','end_timestamp']]

        # tags = [{'start_timestamp': df_apidata[['start_timestamp']],'end_timestamp': df_apidata[['end_timestamp']],'marketprice': df_apidata[['marketprice']], 'unit': df_apidata[['unit']]}]
        tags = {'unit': df_apidata[['unit']]}
        # columns = [{'start_timestamp': df_apidata[['start_timestamp']], 'end_timestamp': df_apidata[['end_timestamp']],
        #         'marketprice': df_apidata[['marketprice']], 'unit': df_apidata[['unit']]}]

        print(df_apidata.dtypes)
        client = DataFrameClient(host='localhost', port=8086)

        client.switch_database('testingdb')
        try:
            client.write_points(df_apidata, 'demo9', tags=tags, protocol='line')
        except:
            error_dict = {'failed': 'failed to write to database check your parameters'}
            return jsonify(error_dict)

        # ,tags=tags,database='kalidb',protocol = "json",time_precision='n'

        # This was not necessary but i included it to confirm the data
        # the head() function takes the number of rows you want to check
        print(df_apidata.head(10))

        success_dict = {'success': 'Successfully created the data into the database'}

        return jsonify(success_dict)
