#!/usr/bin/env python
import pandas as pd
import numpy as np  
import datetime
import sys
#--------------------------------------------------------------
#Functions
#--------------------------------------------------------------
# Reads a csv data file with all stations and trains and converts into a csv
# that has the stations we're looking at. 
def readRawData(inFileName,outFileName,FromStation,ToStation):
    fd = open(inFileName,'r')
    od = open(outFileName, 'w')
    for line in fd.readlines():
        for From in FromStation:
            for To in ToStation:
                if line.__contains__("SL") or line.__contains__("3A"):
                    if line.__contains__(From) and line.__contains__(To):
                        if line.index(From) < line.index(To):
                            od.write(line)
                            od.write("\n")
    fd.close()
    od.close()
# converts the date column of the data to day of the week.
def dateToDay(inputDate):
    month,day, year = (int(x) for x in inputDate.split('/'))    
    ans = datetime.date(year, month, day)
    return (ans.strftime("%A"))
#-----------------------------------------------------------------
inFile = sys.argv[1] #input full data .csv file
outFile = sys.argv[2]# output .csv that we want to create
print ("The input .csv file name :\"" , inFile,"\"")
print ("The  output .csv file name : \"" , outFile,"\"")
fromStation = []# list of all from stations
toStation = []# list of all to stations. This method makes it easy to do
#clustering 

fd1 = open(sys.argv[3],'r') # From stations file
fd2 = open(sys.argv[4],'r') # To station file
for line1 in fd1.readlines():
    fromStation.append(str(line1).rstrip())
for line2 in fd2.readlines():    
    toStation.append(str(line2).rstrip())
fd1.close()
fd2.close()

readRawData(inFile, outFile, fromStation, toStation) # Function Call  

#Reads excel file and only takes columns J, L to P. Change this to include more columns 
df = pd.read_csv(outFile, usecols= [9,10,11,12,13,14,15])

df.columns=  ['travelClass', 'date', 'bookingStatus', 'status1Day', 'status2Days','status1Week', 'status1Month'] #Names these columns

df.fillna(value=-1, inplace=True)  #Since we don't have any negative number, fills all na's as -1

df['labels'] = np.zeros(len(df['travelClass']))
for idx, row in df.iterrows():
	if row.isin(['Confirmed']).any() or row.str.contains('RAC',na=False).any():
		df.set_value(idx,'labels', 1)

LL = ['status1Day', 'status1Week','status1Month', 'status2Days','bookingStatus']
#rownot row.str.contains('W/L')]	
#Remove all RAC and make them 0
#replace all letters of the alphabet with nothing and spaces with backslash.
#These 5 following lines strip from the left hand side all numbers until it hits a non digit
#The items which are purely empty are converted to nan in the bottom and turned to -1
#df.replace(r'\s+|^$', np.nan, regex=True, inplace=True)
for i in range (0, len(LL)):
    df[LL[i]] = df[LL[i]].str.rstrip(to_strip= "ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    df[LL[i]].replace(regex=True, inplace=True, to_replace=r'[^W/L\d\s,].*', value= r'0')
    df[LL[i]].replace(regex=True, inplace=True, to_replace=[r'[a-zA-Z/]', r'\s' ], value=[r'', r'/'])
    df[LL[i]] = df[LL[i]].str.lstrip(to_strip= "123456789,")
    df[LL[i]].replace(regex=True, inplace=True, to_replace=r'\D', value=r'')
df.fillna(value=-1, inplace=True)

df.date = df.date.apply(lambda d: dateToDay(str(d).split(' ')[0]))

df["isWeekend"] = df["date"]
df["Monday"] = df["date"]
df.Monday.replace(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday","Saturday"],[0,1,0,0,0,0,0], inplace = True)

df["Tuesday"] = df["date"]
df.Tuesday.replace(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday","Saturday"],[0,0,1,0,0,0,0], inplace = True)

df["Wednesday"] = df["date"]
df.Wednesday.replace(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday",
    "Friday","Saturday"],[0,0,0,1,0,0,0], inplace = True)

df["Thursday"] = df["date"]
df.Thursday.replace(["Sunday", "Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday"],[0,0,0,0,1,0,0], inplace = True)

df["Friday"] = df["date"]
df.Friday.replace(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday","Saturday"],[0,0,0,0,0,1,0], inplace = True)

df["Saturday"] = df["date"]
df.Saturday.replace(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"],[0,0,0,0,0,0,1], inplace = True)

df["Sunday"] = df["date"]
df.Sunday.replace(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday","Saturday"],[1,0,0,0,0,0,0], inplace = True)

df.isWeekend.replace(["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday","Saturday"],[1,0,0,0,0,0,1], inplace = True)


#df=df[['labels',"travelClass","Sunday", "Monday", "Tuesday", "Wednesday","Thursday","Friday","Saturday", 'bookingStatus', 'status1Day','status2Days','status1Week', 'status1Month', 'isWeekend']] #Names these columns

# only keep data when travel class is in SL,1A,2A,3A
df = df[df["travelClass"].isin(["SL","1A","2A","3A"])]
df['labels'].replace([0,1], [-1,1], inplace = True)
df["class_SL"] = df["travelClass"]
df.class_SL.replace(["SL","1A" ,"2A", "3A"],[1,0,0,0], inplace = True)
df["class_1A"] = df["travelClass"]
df.class_1A.replace(["SL","1A" ,"2A", "3A"],[0,1,0,0], inplace = True)
df["class_2A"] = df["travelClass"]
df.class_2A.replace(["SL","1A" ,"2A", "3A"],[0,0,1,0], inplace = True)
df["class_3A"] = df["travelClass"]
df.class_3A.replace(["SL","1A" ,"2A", "3A"],[0,0,0,1], inplace = True)
#df.rename(columns={"date": "Day"}, inplace = True)

df=df[['labels','bookingStatus','status1Day','status2Days','status1Week','status1Month',"class_SL", "class_3A","Sunday", "Monday","Tuesday", "Wednesday","Thursday","Friday","Saturday"]] #Names these columns

#Convert all these columns to integers finally.
df["labels"] = df["labels"].astype(int)
df['status1Day'] = df['status1Day'].astype(int,  raise_on_error=False)
for i in range (1, len(LL)):
    df[LL[i]] = df[LL[i]].astype(int)

#--------------------------------------------------------------------------
# interpolation code to fill the missing data
#--------------------------------------------------------------------------
df.dropna(inplace=True)
df.astype(int)
cnt=0

for idx, row in df.iterrows():

    #print("New row ", list(row[2:6]), "  unique:", len(np.unique(row[2:6])))
    if row["bookingStatus"] == 0 or row["status1Month"]==0:
	    df.drop(idx, inplace =True)
	    cnt=cnt+1
	    continue

    # case when 3 or more are missing. Nothing to be done here
    if len(np.unique(row[2:6]))<=2:
	    df.drop(idx, inplace =True)
	    cnt=cnt+1
	    continue

    # we have 2 missing data
    if list(row[2:6]).count(-1) == 2:

        # this is the special case for the 2 missing scenario
        if row["status1Month"]==-1 and row["status1Week"]==-1:
            # if bookingStatus - status2Days greater than a chosen number, use
            # bookingStatus for status1Month and interpolate, otherwise set to
            # status1Week
            if row["bookingStatus"] - row["status2Days"] > 60:
                df.set_value(idx, 'status1Month', row['bookingStatus'])
                row['status1Month'] = row['bookingStatus']
            elif row["bookingStatus"] > row["status2Days"]:
                df.set_value(idx, "status1Week", row['bookingStatus'])
                row["status1Week"] = row["bookingStatus"]
            else:
                df.drop(idx, inplace =True)
                cnt=cnt+1
                continue
                #print("status2Days is less than bookingStatus. Stopping")
                #assert False
            
            #now interpolate
            assert list(row[2:6]).count(-1) == 1
         
        # this is the normal case of 2 missing scenario, do normal
        # interpolation 
        else:
            minidict = {2:1, 3:2, 4:7, 5:30}  # mapping index:#days
            namesdict = {2:"status1Day", 3:"status2Days", 4:"status1Week", 5:"status1Month"}
            givens = [] # the non -1 indices
            non_givens = [] # the -1 indices
            for i in range(2,6):
                if row[i] != -1:
                    givens.append(i)
                else:
                    non_givens.append(i)
             
            assert len(givens) == 2
            assert len(non_givens) == 2

            slope = (row[givens[0]] - row[givens[1]]) / (minidict[givens[0]] -
                    minidict[givens[1]])

            val = row[givens[0]] + (minidict[non_givens[0]] - minidict[givens[0]])*slope
            
            # setting a negative val makes no sense, drop this data
            if val < 0:
                df.drop(idx, inplace =True)
                cnt=cnt+1
                continue
            
            df.set_value(idx, namesdict[non_givens[0]], val)
            row[namesdict[non_givens[0]]] = val

            assert list(row[2:6]).count(-1) == 1

    # we have just one missing data
    if list(row[2:6]).count(-1) == 1:

        # this is the special case for the 1 missing scenario
        if row["status1Month"]==-1:
            if row["bookingStatus"] > row["status1Week"]:
                df.set_value(idx, 'status1Month', row['bookingStatus'])
            else:
                df.set_value(idx, 'status1Month', row['status1Week'])

        # this is the normal case of 1 missing point, do normal
        # interpolation
        else:
            # 1Week is missing
            if row["status1Week"]==-1:
                slope = (row["status1Month"] - row['status2Days'])/28.0
                df.set_value(idx, 'status1Week', row["status1Month"] - slope*23)

            # 2Day is missing
            elif row['status2Days']==-1:
                slope = (row["status1Week"] - row['status1Month'])/23.0
                df.set_value(idx, 'status2Days', row["status1Week"] - slope*5)
    
            # 1Day is missing
            elif row['status1Day']==-1:
                slope = (row["status1Week"] - row['status2Days'])/5.0
                df.set_value(idx, 'status1Day', row["status2Days"] - slope)

            else:
                print("Why are we here???")
                assert False

        continue

    #print("Number of missing value are ", list(row[2:6]).count(-1), " __ ",
    #        list(row[2:6]))


# if we have negative value in status1Day, make it 0
df['status1Day'][df['status1Day'] < 0] = 0

# sanity check for negative vals
for idx, row in df.iterrows():
    if list(row[2:6]).count(-1) > 0:
        print("Alert! Negative values in row[2:6]")
        assert False

# change labels depending on the day1 value
df.loc[df['status1Day'] > 0, 'labels'] = -1
df.loc[df['status1Day'] == 0, 'labels'] = 1

#print (df)
df.to_csv("out_"+sys.argv[1]+".csv", index=False)

#print (cnt)                                       

#--------------------------------------------------

#Write to csv
df.to_csv("features.csv", index=False)
#df.to_csv("features_"+fromStation+"_"+toStation+".csv", index=False)
