from datetime import datetime,timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from readData import streamData

default_args={
    'owner':'airflow',
    'start_data':datetime(2024,10,24,11,00),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}
with DAG('Data_ingestion',
        default_args=default_args,
        description='...',
        schedule_interval=timedelta(days=1),
        start_date=datetime(2024,10,23),
        catchup=False,
        ) as dag:


    streaming_task=PythonOperator(
        task_id='stream_data_from_api',
        python_callable=streamData
    )
    streaming_task
