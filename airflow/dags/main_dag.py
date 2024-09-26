from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.bash import BashOperator



default_args = {"owner": "airflow", "retry_delay":timedelta(minutes = 2), "retries": 1}

with DAG(
    dag_id="AirCrashInvestigation_pipeline",
    default_args = default_args,
    description= "end to end Air Crash Investigation Analytic System",
    start_date = datetime(2024,9,22,1),
    schedule_interval = '@daily'


) as dag:

<<<<<<< Updated upstream
    scrape = BashOperator(
        task_id="scrape_LoadS3",
        bash_command="python3 /opt/airflow/tasks/flightDataWebScrape.py",
    )

    validate = BashOperator(
            task_id="validate_LoadS3",
            bash_command="python3 /opt/airflow/tasks/dataValidate.py",
        )
    
    load = BashOperator(
        task_id="loadRedshift",
        bash_command="python3 /opt/airflow/tasks/loadRedshift.py",
    )


 

scrape>>validate>>load
=======
    scrape_data = BashOperator(
        task_id="scrape_loadS3",
        bash_command="python3 /opt/airflow/tasks/flightDataWebScrape.py",
    )

    validate_data = BashOperator(
            task_id="validate_loadS3",
            bash_command="python3 /opt/airflow/tasks/flightDataWebScrape.py",
        )

    load_redshift = BashOperator(
            task_id="loadRedshift",
            bash_command="python3 /opt/airflow/tasks/flightDataWebScrape.py",
        )
>>>>>>> Stashed changes
   
scrape_data >> validate_data >> load_redshift