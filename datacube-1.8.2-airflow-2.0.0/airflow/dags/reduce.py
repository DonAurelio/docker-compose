# -*- coding: utf-8 -*-

import xarray as xr
import os

def one_reduce():
    # Ceate task execution results directory
    airflow_dag_id = os.environ['AIRFLOW_CTX_DAG_ID']
    airflow_task_id = os.environ['AIRFLOW_CTX_TASK_ID']
    results_path = os.path.join('/analysis_storage',airflow_dag_id,'one_reduce')
    os.makedirs(name=results_path, exist_ok=True)

    task = kwargs['task']
    task_instance = kwargs['task_instance']

    dataset_file_path = task_instance.xcom_pull(task_ids=task.upstream_task_ids,key='dataset_file_path')

    print('dataset_file_path',dataset_file_path)
