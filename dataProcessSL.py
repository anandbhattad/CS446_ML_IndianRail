import pandas as pd
import pickle as pk
import numpy as np
import csv
import math
import re

#df = pd.read_csv("ndls_pnbe.csv", delimiter = ",")

#pk.dump(df, open('filtered.p', "wb"))
with open(r'filtered.p', "rb") as datafile:
    data = pk.load(datafile)
    
""" ASSUMPTIONS MADE """
### Generating Features from the data for Delhi to Patna
print("Feature Generations Started")  
size = len(data)
#travel_class=["1A", "2A", "2S", "3A", "3E", "CC", "FC", "SL"]
X = np.zeros(size) #### 5242 is number of entries found between NDLS and PNBE and 8 is total number of features
Y = np.zeros(size) ### First considering all waitlists as confirmed 
j=0
for i in range(size):
    """SELECT ROWS if WAITING LIST IS TRUE AND IF FROM AND TO STATIONS ARE DELHI AND PATNA RESPECTIVELY"""
    if (data.iloc[i][9] == 'SL' and data.iloc[i][11][0]=='W'):
       X[i]=int(re.sub("\D", "", data.iloc[i][11]))
       print("hi1")
       if data.iloc[i][12][0]!='W':
           print ("hi")
