#  # getting the two parameters from the get request
#  startTimestamp = int(flask.request.args.get("startTimestamp"))
#  endTimestamp = int(flask.request.args.get("endTimestamp"))
#
#  # Test print the two value in the console to confirm i have
#  # the right value
#  print(startTimestamp)
#  print(endTimestamp)
#
#  # then i proceed with connection pooling which is handled by
#  # urllib pool manager
#  http = urllib3.PoolManager(
#      cert_reqs='CERT_REQUIRED',
#      ca_certs=certifi.where())
#
#  # Proceed to define the Url which will be called , you notice i have incorporated
#  # the start and end parameters from the get request
#  url = 'https://api.awattar.at/v1/marketdata?start=' + str(startTimestamp) + '&end=' + str(endTimestamp)
#  print(url)
#
#  # this makes the request with external world to the Api world
#  api_request = http.request('GET', url)
#  api_request.status
#
#  # 200 status means the connection was successful there are many http
#  # codes with different meaning visit wikipedia for all codes
#  # using this link https://en.wikipedia.org/wiki/List_of_HTTP_status_codes
#  print(api_request.status)
#
#  # The next step is decode the data into json into a way i can handle it with python
#  data = json.loads(api_request.data.decode('utf-8'))
#
#  # To process the data further with python data analytics library pandas
#  # for easy processing i convert it into pandas dataframe
#  df_apidata = pd.json_normalize(data, "data")
#
#
#  df_apidata.reset_index(drop=True)
#  Fields=['start_timestamp','marketprice', 'unit']
#  fixtags={'unit':'Eur/MWh'}
#
#  datatags=['unit']
#  file_name='C:\\Users\\kaki\\cloudComputingPractices\\marketprice\\mycsvdatainflux.csv'
#  df_from_csv=pd.read_csv(file_name,sep=',',index_col=False,parse_dates=['start_timestamp'], usecols=Fields)
#  df_from_csv.set_index('start_timestamp', inplace=True)
#
#  print(df_from_csv.head())
#
#
#  # converted_df = pd.to_datetime(df_apidata['start_timestamp'], unit='ms')
#  # df_apidata['start_timestamp'] = pd.to_datetime(
#  #     df_apidata['start_timestamp'],
#  #     unit='ms'
#  # )
#  # df_apidata['end_timestamp'] = pd.to_datetime(
#  #     df_apidata['end_timestamp'],
#  #     unit='ms'
#  # )
#  # df_apidata.to_csv(r'mycsvdropdatainflux.csv')
#  # print(df_from_csv.shape)
#  # print(df_from_csv.head(5))
#  #
#  # df_from_csv = df_from_csv.set_index(pd.DatetimeIndex(df_apidata['start_timestamp']))
#  # print(df_from_csv.head(5))
#  # print(df_from_csv.dtypes)
#  # timeValues = df_apidata[['start_timestamp', 'end_timestamp']]
#
#  # timeValues = df_apidata[['end_timestamp']]
#  # timeValues.index = df_apidata[['start_timestamp']]
#  # tags = {'marketprice': df_apidata[['marketprice']], 'unit': df_apidata[['unit']]}
#
#  # timeValues = df_apidata[['start_timestamp','end_timestamp']]
#
#  # tags = [{'start_timestamp': df_apidata[['start_timestamp']],'end_timestamp': df_apidata[['end_timestamp']],'marketprice': df_apidata[['marketprice']], 'unit': df_apidata[['unit']]}]
#  # tags = {'unit': df_from_csv[['unit']]}
#
#  # influxdata = json.dumps(df_apidata.to_json())
#  # host = ' http://127.0.0.1'
#  # port = 8086
#  # user = 'root'
#  # password = 'root'
#  # dbname = 'kalidb'
#  # dbuser = 'kalikimanzi'
#  # dbuser_password = 'kalikimanzi123'
#  client = DataFrameClient(host='localhost', port=8086)
#
#  client.switch_database('testingdb')
#
# # print(df_apidata.dtypes)
#  # dfnew=df_from_csv[['marketprice']]
#  client.write_points(df_from_csv, 'demo4',tags=fixtags,protocol='line')
#
#  # ,tags=tags,database='kalidb',protocol = "json",time_precision='n'
#
#  # This was not necessary but i included it to confirm the data
#  # the head() function takes the number of rows you want to check
#  print(df_from_csv.head(10))
#
#  # since i am interested with only marketprice
#  # online i extract the marketprice column  from the dataframe by creating
#  # another dataframe with the market price column, though i can also extract other
#  # columns by specifying them
#  df_marketprice = df_from_csv[['marketprice', 'unit']]
#
#  # The reason why i am changing this a dictionary is because it takes a longer process
#  # to serialize a dataframe to json format. since using jsonify i can convert
#  # the python dictionary to json format to be send over the api
#  marketprice_dictionary = df_marketprice.to_dict("dict")
#
#  return jsonify(marketprice_dictionary)
