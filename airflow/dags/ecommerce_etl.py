from datetime import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator


with DAG(
    dag_id="ecommerce_etl",
    start_date=datetime(2026, 1, 1),
    schedule=None,
    catchup=False,
    tags=["ecommerce", "etl"],
) as dag:

    generate_data = BashOperator(
        task_id="generate_data",
        bash_command="cd /opt/airflow && python /opt/airflow/src/generate_data.py",
        retries=2,
    )

    load_data = BashOperator(
        task_id="load_data",
        bash_command="cd /opt/airflow && python /opt/airflow/src/load_data.py",
        retries=2,
    )

    validate_data = BashOperator(
        task_id="validate_data",
        bash_command="cd /opt/airflow && python /opt/airflow/src/validate_data.py",
        retries=1,
    )

    generate_data >> load_data >> validate_data