# -*- coding: utf-8 -*-

import datacube
import os

import numpy as np

from cloud_mask import landsat_qa_clean_mask
from cloud_mask import landsat_clean_mask_invalid
from common import write_geotiff_from_xr

def query(product,longitude, latitude, time, measurements, crs, output_crs, resolution,**kwargs):
    # Create task execution results directory
    airflow_dag_id = os.environ['AIRFLOW_CTX_DAG_ID']
    airflow_task_id = os.environ['AIRFLOW_CTX_TASK_ID']
    results_path = os.path.join('/analysis_storage',airflow_dag_id,'query')
    os.makedirs(name=results_path, exist_ok=True)
    
    # Perform the query task
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
    
    # Perform cloud and invalid values masking
    no_data = -9999
    
    mask_nan = ~np.isnan(dataset)
    mask_inf = ~np.isinf(dataset)

    invalid_mask = landsat_clean_mask_invalid(dataset)
    clean_mask = landsat_qa_clean_mask(dataset,platform='LANDSAT_8',cover_types=['clear','water'])
    dataset = dataset.where(invalid_mask & clean_mask & mask_nan & mask_inf,other=no_data)
    
    file_name = airflow_task_id + '.nc'
    file_path = os.path.join(results_path,file_name)
    
    del dataset.time.attrs['units']
    del dataset.pixel_qa.attrs['flags_definition']
    
    dataset.to_netcdf(file_path)
       
    task_instance = kwargs['task_instance']
    task_instance.xcom_push('dataset_file_path',file_path)
