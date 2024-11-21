import geopandas as gpd
import matplotlib.pyplot as plt
import xarray as xr
import rioxarray
import cartopy.crs as ccrs
import netCDF4 as nc
import pandas as pd

standard_crs = "EPSG:4326"
time = 182
year = 1948
shapefile1_path = "./shapes/1203/WBDHU4.shp"
shapefile1 = gpd.read_file(shapefile1_path)
shapefile2_path = "./shapes/1204/WBDHU4.shp"
shapefile2 = gpd.read_file(shapefile2_path)

shapefile = pd.concat([shapefile1, shapefile2], ignore_index=True)


# data = nc.Dataset('./precipitation_data/CPC-CONUS_total_precipitation_day_0.25x0.25_conus_' + str(year) + '_v1.0.nc', "r")
data = xr.open_dataset('./precipitation_data/CPC-CONUS_total_precipitation_day_0.25x0.25_conus_' + str(year) + '_v1.0.nc')
precipitation = data["pr"]
precipitation = precipitation.assign_coords(
    lon=(((precipitation['lon'] + 180) % 360) - 180)
)
precipitation = precipitation.rio.set_spatial_dims(x_dim='lon', y_dim='lat', inplace=False)
precipitation = precipitation.rio.write_crs(shapefile.crs)

precipitation = precipitation.rio.clip(shapefile.geometry, shapefile.crs, drop=True, all_touched=True)
precipitation_at_time = precipitation.isel(time=time)

fig, ax = plt.subplots(subplot_kw={"projection": ccrs.PlateCarree()})

precipitation_at_time.plot(ax=ax,
                        transform=ccrs.PlateCarree(), # Transform to match the projection
                    )

shapefile.boundary.plot(ax=ax, edgecolor="red", linewidth=1.5)
plt.title("Precipitation at Time Step " + str(time))
plt.show()