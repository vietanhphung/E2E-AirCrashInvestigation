import boto3
import configparser
import csv
import io
from io import StringIO
import pathlib
from dotenv import dotenv_values


configuration_path = pathlib.Path(__file__).parent.resolve()
script_path = pathlib.Path(__file__).parent.resolve()
config = dotenv_values(f"{configuration_path}/pipeline.conf")

bucket=config["bucket_name"]
host=config["host"]
port=config["port"]
dbname=config["dbname"]
user=config["user"]
password=config["password"]

configuration_path = pathlib.Path(__file__).parent.resolve()
script_path = pathlib.Path(__file__).parent.resolve()
config = dotenv_values(f"{configuration_path}/credentials.conf")

access = config["access_key"]
secret = config["secret_key"]


# save file locally
def loadCSV(data,fname):
    headers = data[0].keys()
    with open(fname, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        # Write the header (column names)
        writer.writeheader()
        # Write the data rows
        writer.writerows(data)




#save to S3 bucket
def saveToS3(data,fname):
    try:
        s3 = boto3.client('s3', aws_access_key_id=access,
        aws_secret_access_key=secret)

        csv_buffer = io.StringIO()

        # Extract field names (keys) from the first dictionary
        fieldnames = data[0].keys()

        # Write the list of dictionaries to the buffer as CSV
        writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

        # Upload CSV data from buffer to S3
        s3.put_object(
            Bucket=bucket,
            Key=fname,
            Body=csv_buffer.getvalue()
        )
        print("Data saved to S3")
    except:
        print("Error, input may be []")


#read file from S3
def getFromS3(fname):
    s3 = boto3.client('s3', aws_access_key_id=access,
    aws_secret_access_key=secret)

    response = s3.get_object(Bucket=bucket, Key=fname)
    file_content = response['Body'].read().decode('utf-8')
    data = StringIO(file_content)
    print('data from S3 extracted')
    return data




"""

#save JSON File Locally
def loadJSON():             
    with open('data.json', 'w') as f:
        json.dump(infoList, f)
#save html content locally
def save_html(html, path):
    with open(path, 'wb') as f:
        f.write(html)    


#open html locally
def open_html(path):
    with open(path, 'rb') as f:
        return f.read()   

"""

