# -*- coding: utf-8 -*-

from common import write_geotiff_from_xr

import xarray as xr
import os

def median_composite(**kwargs):
    # Create task execution results directory
    airflow_dag_id = os.environ['AIRFLOW_CTX_DAG_ID']
    airflow_task_id = os.environ['AIRFLOW_CTX_TASK_ID']
    results_path = os.path.join('/analysis_storage',airflow_dag_id,'median')
    os.makedirs(name=results_path, exist_ok=True)

    task = kwargs['task']
    task_instance = kwargs['task_instance']

    dataset_file_path = task_instance.xcom_pull(task_ids=task.upstream_task_ids,key='dataset_file_path')[0]

    dataset = xr.open_dataset(dataset_file_path)
    
    median = dataset.median('time', skipna=True)
    
    file_name = airflow_task_id + '.nc'
    file_path = os.path.join(results_path,file_name)
    
    #del median.time.attrs['units']
    #del median.pixel_qa.attrs['flags_definition']
    
    median.to_netcdf(file_path)

    task_instance.xcom_push('dataset_file_path',file_path)