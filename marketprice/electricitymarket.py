import json

import certifi
import flask
import pandas as pd
import urllib3
from flask import jsonify
from flask_restful import Resource


class ElectricityPrice(Resource):

    def get(self):
        """
        1. This end point receives two parameters
            1.1. startTimestamp
            1.2. endTimestamp

        2. Combines the two parameters with awattar url to form awattar url
        3. An API call is made to https://api.awattar.at
        4. Awattar returns a json data
        5. Json data is converted to Pandas Dataframe inorder to interact with it further,
        6. Several manipulation and processing can be carried out on this data though i only chose to
        extract the marketprices, and the unit price which is send back to the user as a JSON

        :return: marketprice, unit JSON
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

        df_apidata.set_index('start_timestamp', inplace=True)
        print(df_apidata.head(5))

        # This was not necessary but i included it to confirm the data
        # the head() function takes the number of rows you want to check
        print(df_apidata.head(10))

        # since i am interested with only marketprice
        # online i extract the marketprice column  from the dataframe by creating
        # another dataframe with the market price column, though i can also extract other
        # columns by specifying them
        df_marketprice = df_apidata[['marketprice', 'unit']]

        # The reason why i am changing this a dictionary is because it takes a longer process
        # to serialize a dataframe to json format. since using jsonify i can convert
        # the python dictionary to json format to be send over the api
        marketprice_dictionary = df_marketprice.to_dict("dict")

        return jsonify(marketprice_dictionary)
