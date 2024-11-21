import os
import xarray as xr
import geopandas as gpd
import rioxarray
import matplotlib.pyplot as plt

def plot_precipitation(precipitation, time=0):
    precipitation_at_time = precipitation.isel(time=time)

    precipitation_at_time.plot()
    plt.title("Precipitation at Time Step " + str(time))
    plt.show()

def clip_data(data):
    precipitation = data["pr"]
    plot_precipitation(precipitation)
    precipitation = precipitation.rio.write_crs(standard_crs)
    clipped = precipitation.rio.clip(shapefile.geometry, shapefile.crs)
    return clipped

standard_crs = "EPSG:4326"

# Load the shapefile
shp_file = "./shapes/1203/WBDHU4.shp"
shapefile = gpd.read_file(shp_file)

# Ensure the shapefile and NetCDF coordinates have the same CRS
shapefile = shapefile.to_crs(standard_crs)

precipitation_data = {}
for filename in os.listdir('./precipitation_data'):
    if filename.endswith('.nc'):
        year = filename.split('_')[6]
        data = xr.open_dataset('./precipitation_data/' + filename)
        precipitation_data[year] = clip_data(data)
        input()
