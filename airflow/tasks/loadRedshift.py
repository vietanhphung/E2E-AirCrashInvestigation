import pipelineActions
import psycopg2
import boto3
import configparser
import pathlib



script_path = pathlib.Path(__file__).parent.resolve()
config = configparser.ConfigParser()
config_file_path = script_path / 'pipeline.conf'
config.read(config_file_path)
bucket = config.get('aws_boto_credentials', 'bucket_name')
file =  config.get('aws_boto_credentials', 'file')

host = config.get('redshift','host')
port = config.get('redshift','port')
dbname = config.get('redshift','dbname')
user = config.get('redshift','user')
password = config.get('redshift','password')
table = config.get('redshift','table')
role = config.get('redshift','role')




# SQL COPY command for Redshift
copy_query = f"""
    COPY {table}
    FROM 's3://{bucket}/{file}'
    IAM_ROLE '{role}'
    FORMAT AS CSV
    DELIMITER ','
    IGNOREHEADER 1
    REGION 'us-east-1';
"""

def load_csv_to_redshift():
    conn = None
    try:
        # Connect to Redshift
        conn = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )
        cur = conn.cursor()
        print("Connected to Redshift")
        
        # Execute COPY command to load data from S3 to Redshift
        cur.execute(copy_query)
        conn.commit()
        print("Data loaded successfully!")
    
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Redshift connection closed")

if __name__ == "__main__":
    load_csv_to_redshift()
