# -*- coding: utf-8 -*-

import datacube

def query(product,longitude, latitude, time, measurements, crs, output_crs, resolution):
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
    
    dataset.to_netcdf('dataset.nc')

query(
    product='ls8_collections_sr_scene',
    longitude=(-73, -72),
    latitude=(4, 5),
    time=('2020-12-12','2020-12-12'),
    measurements=['red','blue','green'],
    crs='EPSG:4326',
    output_crs='EPSG:4326',
    resolution=(-0.00008983111,0.00008971023)
)
