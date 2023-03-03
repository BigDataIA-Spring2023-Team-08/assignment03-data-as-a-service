from airflow.models import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from airflow.models.param import Param
from datetime import timedelta
#import pandas as pd
import os
#from sqlalchemy import create_engine
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
from great_expectations.data_context.types.base import (
    DataContextConfig,
    CheckpointConfig
)

# Great Expectation Path (Inside working_dir)
base_path = "/opt/airflow/working_dir"

ge_root_dir = os.path.join(base_path, "great_expectations")
print(ge_root_dir)


dag = DAG(
    dag_id="ge_dag",
    schedule="0 0 * * *",   # https://crontab.guru/
    start_date=days_ago(0),
    catchup=False,
    dagrun_timeout=timedelta(minutes=60),
    tags=["great_expectations", "AWS S3", "GOES18", "NEXRAD"],
)

# # Checkpoint DAGS for Great Expectation Reports (GOES18, NEXRAD)
with dag:
    ge_goes18_checkpoint_pass = GreatExpectationsOperator(
        task_id="task_goes18_checkpoint_pass",
        data_context_root_dir=ge_root_dir,
        checkpoint_name="goes18_checkpoint_v0.1",
        fail_task_on_validation_failure=False
        # trigger_rule="all_done"
    )

    ge_nexrad_checkpoint_pass = GreatExpectationsOperator(
        task_id="task_nexrad_checkpoint_pass",
        data_context_root_dir=ge_root_dir,
        checkpoint_name="nexrad_checkpoint_v0.2",
        fail_task_on_validation_failure=False
        # trigger_rule="all_done"
    )

# # Flow
    ge_goes18_checkpoint_pass >> ge_nexrad_checkpoint_pass
