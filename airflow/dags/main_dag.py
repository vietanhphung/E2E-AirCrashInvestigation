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

    scrape_audiophile_data = BashOperator(
        task_id="scrape",
        bash_command="python3 /tasks/testcode.py",
    )

   
