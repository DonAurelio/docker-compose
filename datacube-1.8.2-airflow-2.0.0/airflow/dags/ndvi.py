# -*- coding: utf-8 -*-

def ndvi(dataset):
    # Create task execution results directory
    airflow_dag_id = os.environ['AIRFLOW_CTX_DAG_ID']
    airflow_task_id = os.environ['AIRFLOW_CTX_TASK_ID']
    results_path = os.path.join('/analysis_storage',airflow_dag_id,'ndvi')
    os.makedirs(name=results_path, exist_ok=True)

    task = kwargs['task']
    task_instance = kwargs['task_instance']

    dataset_file_path = task_instance.xcom_pull(task_ids=task.upstream_task_ids,key='dataset_file_path')[0]

    dataset = xr.open_dataset(dataset_file_path)
    dataset['ndvi'] = (dataset.nir - dataset.red) / (dataset.nir + dataset.red)
    
    # Generación de máscara que establece que deseamos dejar aquellos píxeles que presentan un ndvi mayor que -1.0
    mask_lower = dataset.ndvi >= -1.0

    # Generación de máscara que establece que deseamos dejar aquellos píxeles que son menores que 1.0
    mask_higher = dataset.ndvi <= 1.0

    # Aplicamos ambas máscaras sobre todo el dataset
    masked_dataset = dataset.where(mask_lower & mask_higher)
    
    # Obtener un dataset solo con el ndvi
    ndvi = masked_dataset[['ndvi']]
    
    file_name = airflow_task_id + '.nc'
    file_path = os.path.join(results_path,file_name)
    
    del ndvi.time.attrs['units']
    del ndvi.pixel_qa.attrs['flags_definition']
    
    ndvi.to_netcdf(file_path)

    task_instance.xcom_push('dataset_file_path',file_path)