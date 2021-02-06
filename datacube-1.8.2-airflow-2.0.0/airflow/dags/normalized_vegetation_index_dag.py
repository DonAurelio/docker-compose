import datacube

from airflow.decorators import dag, task
from airflow.operators.python import get_current_context
from airflow.utils.dates import days_ago

default_args = {
    'owner': 'airflow',
}

@dag(default_args=default_args, schedule_interval=None, start_date=days_ago(2))
def normalized_vegetation_index():
    @task()
    def query(product: str, longitude: float, latitude: float, time: tuple, measurements: list, crs: str, output_crs: str, resolution: tuple,**kwargs):
        """
        dc = datacube.Datacube(app="Cana")
        dataset = dc.load(
            product=product,
            longitude=longitude,
            latitude=latitude,
            time=time,
            measurements=measurements,
            crs=crs,
            output_crs=output_crs,
            resolution=resolution
        )

        dataset
        

        dataset.to_netcdf('ndvi.nc')
        
        """
        context = get_current_context()
        task_instance = context["ti"]
        print('ti',task_instance,'kwargs',kwargs)


    kwargs = {
        'product': "ls8_collections_sr_scene",
        'longitude': (-73.03944, -72.83944000000001),
        'latitude': (5.4521500000000005, 5.65215),
        'time': ('2020-09-21', '2020-09-23'),
        'measurements': ["red","blue","green","nir","swir1","swir2","scl"],
        'crs': "EPSG:4326",
        'output_crs': "EPSG:4326",
        'resolution': (-0.00008983111,0.00008971023)
    }
        
    query(**kwargs)

result = normalized_vegetation_index()