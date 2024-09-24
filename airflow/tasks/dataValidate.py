from datetime import datetime
import re
from pipelineActions import *
import pandas as pd



#This file will do initial transformation of bronze data, taken from S3, to silver data, then upload back silver data csv file back into S3


#convert String to camel case
def camel(s):
    # Split the string by spaces, capitalize the first letter of each part except the first, and join them
    parts = str(s).split()
    return parts[0].capitalize() + ''.join(word.capitalize() for word in parts[1:])

def getInt(s):
    # Use regular expression to find all digit characters
    try:
        return int(''.join(re.findall(r'\d', s))) 
    except:
        return None



def convertFormat(o):
    if o != {}:
        #o["date"] =  int(datetime.strptime(o["date"], "%B %d, %Y").strftime("%Y%m%d") )
        o["date"] = pd.to_datetime(o['date'], format='%B %d, %Y').strftime('%Y%m%d')
        o["time"] = getInt(o["time"]) if o["time"] != "?" else None
        o["location"] = camel(o["location"]) if o["location"] != "?" else None
        o["operator"] = camel(o["operator"]) if o["operator"] != "?" else None
        o["flight"] = camel(o["flight"]) if o["flight"] != "?" else None
        o["route"] = camel(o["route"])if o["route"] != "?" else None
        o["aircraft"] = camel(o["aircraft"])if o["aircraft"] != "?" else None
        o["registration"] = camel(o["registration"])if o["registration"] != "?" else None
        o["cnln"] = camel(o["cnln"])if o["cnln"] != "?" else None
        o["aboard"] = getInt(o["aboard"])if o["aboard"] != "?" else None
        o["fatalities"] = getInt(o["fatalities"])if o["fatalities"] != "?" else None
        o["ground"] = getInt(o["ground"])if o["ground"] != "?" else None
        o["summary"] = str(o["summary"])if o["summary"] != "?" else None 
        print(o['time'])
        return o
    else:
        return None
    



dataList = []

def dataIngest():
    df = pd.read_csv('data.csv').dropna(how='all') # read and drop all empty rows
    result = df.to_dict(orient='records')
    for d in result:
        if d != {}:
            converted = convertFormat(d)
            dataList.append(converted)




dataIngest()
#loadCSV(dataList,'silver.csv')
saveToS3(dataList, 'silver.csv')


