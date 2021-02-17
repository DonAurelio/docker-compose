from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

from query import query

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
    'longitude': (-73, -71),
    'latitude': (4, 6),
    'time': ('2020-12-12','2020-12-12'),
    'measurements': ['red','blue','green'],
    'crs': 'EPSG:4326',
    'output_crs': 'EPSG:4326',
    'resolution': (-0.00008983111,0.00008971023)
}

lon_min, lon_max = query_kwargs['longitude']
lat_min, lat_max = query_kwargs['latitude']

for latitude in range(lat_min,lat_max):
    for longitude in range(lon_min,lon_max):

        query_task_kwargs ={
            'product': 'ls8_collections_sr_scene',
            'longitude': (longitude, longitude + 1),
            'latitude': (latitude, latitude + 1),
            'time': ('2020-12-12','2020-12-12'),
            'measurements': ['red','blue','green'],
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

        query_task




