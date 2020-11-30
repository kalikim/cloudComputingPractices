# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 18:03:24 2020

@author: Kali Kimanzi
@regNo: S1920770026
"""
import json

import certifi
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import urllib3

"""
EXERCISE 1 
"""

http = urllib3.PoolManager(
    cert_reqs='CERT_REQUIRED',
    ca_certs=certifi.where())
url = 'https://maps2.dcgis.dc.gov/dcgis/rest/services/FEEDS/MPD/MapServer/2/query?where=1%3D1&outFields=*&outSR=4326&f=json'
url2 = 'http://api.geonames.org/postalCodeSearchJSON?formatted=true&postalcode=9011&maxRows=10&username=kalikimanzi&style=full'
r = http.request('GET', url2)
r.status
data = json.loads(r.data.decode('utf-8'))
# displaying the returned postalcode data
print(data)
df_postal_codes = pd.json_normalize(data, "postalCodes")
# print the first five rows of the dataframe to confirm if it is the required data
df_postal_codes.head()

"""
Getting other data from other Api webclients 
for this case i took the moving market price of electricity 
from https://www.awattar.com/services/api/ 
"""
# this is the api url with start and end timestamps
url = 'https://api.awattar.at/v1/marketdata?start=1546300800000&end=1577750400000'
r = http.request('GET', url)
# checks whether the api call was successful 200 represents a successful api call
r.status
# decodes the from the json data to python dictionary
data = json.loads(r.data.decode('utf-8'))
# normalizes the json data into python pandas data frame using the 'feature' data
df_electricity_prices = pd.json_normalize(data, "data")
# print the first five rows of the dataframe to confirm if it is the required data
df_electricity_prices.head()
# To work on marketprices on we will have to create a new dataframe with only marketprices
df_marketprices = df_electricity_prices[['marketprice']]
# print the first five rows of the dataframe to confirm if it is the required data
df_marketprices.head()
plt.plot(df_marketprices.marketprice)
plt.show()

"""
PRACTICE 3 
THE MOVING AVERAGE 
"""
# creating a moving average using pandas rolling function
df_marketprices['movingAvg'] = df_marketprices.iloc[:, 0].rolling(window=500).mean()
df_marketprices.head()
# we notice the movingAvg column created contain NaN values so we calculate the average
# first
avg_movingAvg = df_marketprices["movingAvg"].astype("float").mean(axis=0)
print(avg_movingAvg)
# replace the NaN Values with the average
df_marketprices["movingAvg"].replace(np.nan, avg_movingAvg, inplace=True)
df_marketprices.head()
error_value = df_marketprices['movingAvg'] - df_marketprices['marketprice']
df_marketprices['error'] = error_value
df_marketprices.head(5)
# plotting the two values to see the difference  between the original marketprice
# and the moving average values 

plt.plot(df_marketprices['marketprice'], label='Marketprices')
plt.plot(df_marketprices['movingAvg'], label='MovingAverageValues')
plt.plot(df_marketprices['error'], label='error')
plt.legend(loc=2)
plt.title("The Plot Showing the difference")
plt.show()
