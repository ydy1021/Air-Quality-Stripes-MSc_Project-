import xarray as xr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim
import seaborn as sns

# File paths
weighted_file = "concat_weighted_output.nc"
unweighted_file = "concat_unweighted_output.nc"

# Read NetCDF files
ds_weighted = xr.open_dataset(weighted_file)
ds_unweighted = xr.open_dataset(unweighted_file)

# Select London and get latitude and longitude
geolocator = Nominatim(user_agent="geoapi")
london_location = geolocator.geocode("London")
london_lat, london_lon = london_location.latitude, london_location.longitude

# Variable names
pm25_var_weighted = "PM25_WEIGHTED"
pm25_var_unweighted = "PM25_UNWEIGHTED"
lon_var = "longitude"
lat_var = "latitude"

# Extract PM2.5 data
pm25_weighted = ds_weighted[pm25_var_weighted]
pm25_unweighted = ds_unweighted[pm25_var_unweighted]

# Get the nearest grid point data for London
london_weighted = pm25_weighted.sel(latitude=london_lat, longitude=london_lon, method="nearest")
london_unweighted = pm25_unweighted.sel(latitude=london_lat, longitude=london_lon, method="nearest")

# Convert to Pandas DataFrame
df_weighted = london_weighted.to_dataframe().reset_index()
df_unweighted = london_unweighted.to_dataframe().reset_index()

# Fix cftime datetime format issues
df_weighted["time"] = pd.to_datetime(df_weighted["time"].astype(str))
df_unweighted["time"] = pd.to_datetime(df_unweighted["time"].astype(str))

# Merge the data
df_weighted["PM25_unweighted"] = df_unweighted[pm25_var_unweighted]
df_weighted["City"] = "London"

# Plot time series visualization
plt.figure(figsize=(12, 6))
plt.plot(df_weighted["time"], df_weighted[pm25_var_weighted], label="London (Weighted)", color='blue')
plt.plot(df_weighted["time"], df_weighted["PM25_unweighted"], linestyle="dashed", label="London (Unweighted)", color='red')
plt.xlabel("Year")
plt.ylabel("PM2.5 Concentration (µg/m³)")
plt.title("PM2.5 Concentration in London (Weighted vs. Unweighted)")
plt.legend()
plt.grid(True)
plt.savefig("london_pm25_comparison.png", dpi=300)
plt.show()

# Compute weighting adjustment factor
df_weighted["Weighting Factor"] = df_weighted[pm25_var_weighted] / df_weighted["PM25_unweighted"]

# Compute the difference between weighted and unweighted data
df_weighted["PM25_Difference"] = df_weighted[pm25_var_weighted] - df_weighted["PM25_unweighted"]

# Plot the difference between weighted and unweighted PM2.5
plt.figure(figsize=(12, 6))
plt.plot(df_weighted["time"], df_weighted["PM25_Difference"], color='purple', label="Weighted - Unweighted")
plt.axhline(0, color='black', linestyle="--", linewidth=1)
plt.xlabel("Year")
plt.ylabel("PM2.5 Difference (µg/m³)")
plt.title("Difference Between Weighted and Unweighted PM2.5 in London")
plt.legend()
plt.grid(True)
plt.savefig("london_pm25_difference.png", dpi=300)
plt.show()

# Print the average weighting factor
print("Average Weighting Factor for London:", df_weighted["Weighting Factor"].mean())
