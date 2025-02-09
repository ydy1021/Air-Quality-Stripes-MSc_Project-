import xarray as xr
import numpy as np
import os

# Path to the data folder
data_folder = 'E:\Master2\FYP\Global\Global\Monthly'  # Modify according to the actual path

# Automatically read all monthly files for the year 1998
file_list = [f'V5GL0502.HybridPM25c_0p05.Global.1998{str(month).zfill(2)}-1998{str(month).zfill(2)}.nc'
             for month in range(1, 13)]
file_paths = [os.path.join(data_folder, file) for file in file_list]

# Read all NetCDF files and merge them
datasets = [xr.open_dataset(file) for file in file_paths]

# Merge datasets along a newly created time dimension
combined_data = xr.concat(datasets, dim='time')

# Calculate the annual mean for 1998
annual_mean = combined_data['GWRPM25'].mean(dim='time')  # Compute the mean of GWRPM25

# Save as a new NetCDF file
annual_mean_dataset = annual_mean.to_dataset(name='GWRPM25_AnnualMean')  # Name it as GWRPM25_AnnualMean
annual_mean_dataset.to_netcdf('1998avg.nc')

print("✅ The annual mean PM2.5 for 1998 has been calculated and saved as '1998avg.nc'.")
