# -*- coding: utf-8 -*-

import datacube
import os

def query(product,longitude, latitude, time, measurements, crs, output_crs, resolution,**kwargs):
    # Create task execution results directory
    airflow_dag_id = os.environ['AIRFLOW_CTX_DAG_ID']
    airflow_task_id = os.environ['AIRFLOW_CTX_TASK_ID']
    results_path = os.path.join('/analysis_storage',airflow_dag_id,airflow_task_id)
    os.makedirs(name=results_path, exist_ok=True)
    
    # Perform the task
    dc = datacube.Datacube(app="query")
    dataset = dc.load(
        product=product,
        longitude=longitude,
        latitude=latitude,
        time=time,
        measurements=measurements,
        crs=crs,
        output_crs=crs,
        resolution=resolution
    )
    
    file_name = airflow_task_id + '.nc'
    file_path = os.path.join(results_path,file_name)
    
    del dataset.time.attrs['units']
    dataset.to_netcdf(file_path)
