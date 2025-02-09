import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
import os

# Check the current working directory
print("Current working directory:", os.getcwd())

# Load the datasets
file1 = xr.open_dataset('1998avg.nc')
file2 = xr.open_dataset('../Annual/V5GL0502.HybridPM25c_0p05.Global.199801-199812.nc')

# View variable names to ensure correctness
print("Variables in 1998avg.nc:", list(file1.data_vars))
print("Variables in the Annual file:", list(file2.data_vars))

# Use the actual variable names
pm25_avg = file1['GWRPM25_AnnualMean']
pm25_annual = file2['GWRPM25']

# Check data dimensions
print("Dimensions in 1998avg.nc:", pm25_avg.dims)
print("Dimensions in the Annual file:", pm25_annual.dims)

# If needed, interpolate data to match dimensions (optional)
# pm25_annual_interp = pm25_annual.interp_like(pm25_avg)

# Compute the difference
difference = pm25_annual - pm25_avg

# Display basic statistics of the difference
print("Minimum difference:", np.nanmin(difference.values))
print("Maximum difference:", np.nanmax(difference.values))
print("Mean difference:", np.nanmean(difference.values))
