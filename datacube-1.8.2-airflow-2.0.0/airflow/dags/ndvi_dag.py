from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from query import query
from median import median_composite
from ndvi import ndvi
from reduce import one_reduce

args = {
    'owner': 'airflow',
}

dag = DAG(
    dag_id='ndvi_dag',
    default_args=args,
    schedule_interval=None,
    start_date=days_ago(2),
    tags=['example'],
)

query_kwargs ={
    'product': 'ls8_collections_sr_scene',
    'longitude': (-74, -72),
    'latitude': (5, 7),
    'time': ('2021-01-29','2021-01-29'),
    'measurements': ['red','blue','green','pixel_qa'],
    'crs': 'EPSG:4326',
    'output_crs': 'EPSG:4326',
    'resolution': (-0.00008983111,0.00008971023)
}

lon_min, lon_max = query_kwargs['longitude']
lat_min, lat_max = query_kwargs['latitude']

query_tasks = []

# query map by tile
for latitude in range(lat_min,lat_max):
    for longitude in range(lon_min,lon_max):

        query_task_kwargs ={
            'product': 'ls8_collections_sr_scene',
            'longitude': (longitude, longitude + 1),
            'latitude': (latitude, latitude + 1),
            'time': ('2020-12-12','2020-12-12'),
            'measurements': ['red','blue','green','pixel_qa'],
            'crs': 'EPSG:4326',
            'output_crs': 'EPSG:4326',
            'resolution': (-0.00008983111,0.00008971023)
        }
        
        task_id = 'query_{latitude}_{longitude}'.format(
            latitude=latitude, longitude=longitude
        ) 
        
        query_task = PythonOperator(
            task_id=task_id,
            python_callable=query,
            op_args=None,
            op_kwargs=query_task_kwargs,
            provide_context=True,
            dag=dag,
        )
        
        query_tasks.append(query_task)

# Identity map (median composite)
median_tasks = []
for i, query_task in enumerate(query_tasks):
    median_task = PythonOperator(
            task_id=f'median_{i}',
            python_callable=median_composite,
            op_args=None,
            op_kwargs=query_task_kwargs,
            provide_context=True,
            dag=dag,
        )
    
    median_tasks.append(median_task)
    query_task >> median_task
    
# Identity map (ndvi)
ndvi_tasks = []
for i, median_task in enumerate(median_tasks):
    ndvi_task = PythonOperator(
            task_id=f'ndvi_{i}',
            python_callable=ndvi,
            op_args=None,
            op_kwargs=query_task_kwargs,
            provide_context=True,
            dag=dag,
        )
    
    ndvi_tasks.append(ndvi_task)
    median_task >> ndvi_task
    
# One reduce
mosaic_task = PythonOperator(
    task_id='mosaic',
    python_callable=one_reduce,
    op_args=None,
    op_kwargs=query_task_kwargs,
    provide_context=True,
    dag=dag,
)

ndvi_tasks >> mosaic_task

