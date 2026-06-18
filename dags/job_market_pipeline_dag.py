from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator


default_args = {
    'owner': 'Mahlaka',
    "retries" : 1, 
    "retry_delay": timedelta(minutes=5),

}

with DAG (
    dag_id = "job_market_pipeline_dag",
    start_date=datetime(2025, 1, 1),
    schedule_interval = "@daily",
    default_args = default_args,
    catchup = False,
    tags = ['job_market', 'spark', 's3',  "postgres"],
) as dag: 

    download_dataset = BashOperator(
        task_id = 'download_kaggle_dataset',
        bash_command = 'python scripts/download_kaggle_dataset.py',
    )
    
    spark_transform = BashOperator(
        task_id = 'spark_transform',
        bash_command="spark-submit spark_jobs/transform_jobs.py",
    )
    
    load_to_postgres = BashOperator(
        task_id = 'load_to_postgres',
        bash_command = 'python scripts/load_to_postgres.py',
    )
    
    data_quality_checks = BashOperator(
        task_id="data_quality_checks",
        bash_command="python scripts/data_quality_checks.py",
    )

download_dataset >> spark_transform >> load_to_postgres >> data_quality_checks