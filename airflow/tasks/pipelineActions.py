import boto3
import configparser
import csv
import io


config = configparser.ConfigParser()
config.read('pipeline.conf')
access = config.get('aws_boto_credentials', 'access_key')
secret = config.get('aws_boto_credentials', 'secret_key')
account = config.get('aws_boto_credentials', 'account_id')
bucket = config.get('aws_boto_credentials', 'bucket_name')

host = config.get('redshift','host')
port = config.get('redshift','port')
dbname = config.get('redshift','dbname')
user = config.get('redshift','user')
password = config.get('redshift','password')



# use locally
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
        Bucket='flightcrashdata',
        Key=fname,
        Body=csv_buffer.getvalue()
    )




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

