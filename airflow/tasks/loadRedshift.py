
import psycopg2
import pathlib
from dotenv import dotenv_values


configuration_path = pathlib.Path(__file__).parent.resolve()
script_path = pathlib.Path(__file__).parent.resolve()
config = dotenv_values(f"{configuration_path}/pipeline.conf")



host = config["host"].split(":")[0]
bucket= config["bucket_name"]
port  = config["port"]
dbname  = config["dbname"]
user  = config["user"]
password  = config["password"]
table  = config["table"]
role  = config["role"]



create_table_query = f"""
    CREATE TABLE IF NOT EXISTS flight_incidents (
        incident_date INTEGER,
        incident_time INTEGER,
        location VARCHAR(255),               -- Location of the incident
        operator VARCHAR(255),               -- Operator of the flight
        flight VARCHAR(255),                 -- Flight number
        route VARCHAR(255),                  -- Flight route
        aircraft VARCHAR(255),              -- Aircraft type/model
        registration VARCHAR(255),           -- Aircraft registration
        cnln VARCHAR(255),                   -- Certificate of Registration Number
        aboard INT,                          -- Number of people aboard
        fatalities INT,                      -- Number of fatalities
        ground INT,                          -- Number of people on the ground affected
        summary VARCHAR(5000)                       -- Summary of the incident
    );
    """

copy_table_query = f"""
    CREATE TABLE tempData (LIKE flight_incidents);

    BEGIN TRANSACTION;
    COPY tempData
    FROM 's3://flightcrashbucket/silver.csv'
    IAM_ROLE 'arn:aws:iam::038462789002:role/flightanalysis-redshift-s3-access-role'
    FORMAT AS CSV
    DELIMITER ','
    IGNOREHEADER 1
    REGION 'us-east-1';
    DROP TABLE flight_incidents;
    ALTER TABLE tempData RENAME TO flight_incidents;
    COMMIT TRANSACTION;
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
        # Execute command to crate table and load data from S3 to Redshift
        cur.execute(create_table_query)
        cur.execute(copy_table_query)
        conn.commit()
        print("Command executed")
        print(host,bucket,port,dbname,user,password,table,role)
    
    except psycopg2.Error as db_err:
        print(f"Database error: {db_err}")
    except Exception as e:
        print(f"General error: {e}")

    
    finally:
        if conn:
            cur.close()
            conn.close()
            print("Redshift connection closed")

if __name__ == "__main__":
    load_csv_to_redshift()
