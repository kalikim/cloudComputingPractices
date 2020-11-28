from flask import jsonify
from flask_restful import Resource
from influxdb import DataFrameClient


class influxDatabaseC(Resource):

    def get(self):
        client = DataFrameClient(host='localhost', port=8086)
        print('list of databases')
        print(client.get_list_database())
        client.switch_database('kalidb')

        # print(df_apidata.dtypes)
        # client.write_points(df_apidata,'demo1',tags=tags,protocol ='json' )

        # ,tags=tags,database='kalidb',protocol = "json",time_precision='n'

        # This was not necessary but i included it to confirm the data
        # the head() function takes the number of rows you want to check
        # print(df_apidata.head(10))

        # since i am interested with only marketprice
        # online i extract the marketprice column  from the dataframe by creating
        # another dataframe with the market price column, though i can also extract other
        # columns by specifying them
        # df_marketprice = df_apidata[['marketprice', 'unit']]
        #
        # # The reason why i am changing this a dictionary is because it takes a longer process
        # # to serialize a dataframe to json format. since using jsonify i can convert
        # # the python dictionary to json format to be send over the api
        # marketprice_dictionary = df_marketprice.to_dict("dict")

        return jsonify(client.get_list_database())
