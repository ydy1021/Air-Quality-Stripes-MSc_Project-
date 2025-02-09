import xarray as xr

# Load the dataset
ds = xr.open_dataset('V5GL0502.HybridPM25c_0p05.Global.199801-199812.nc')

# Iterate through data variables and display the first 20 rows
for var in ds.data_vars:
    print(f"Variable: {var}")
    print("=" * 50)

    # Get the variable data
    data = ds[var]

    # Check data dimensions and display the first 20 rows or slices
    if 'time' in data.dims:
        # For data containing the time dimension
        print(data.isel(time=slice(0, 20)))
    elif 'lat' in data.dims and 'lon' in data.dims:
        # For 2D data, display the first 20 latitude rows and all longitudes
        print(data.isel(lat=slice(0, 20)))
    else:
        # For other cases, display the first 20 values directly
        print(data.values[:20])

    print("\n" + "=" * 50 + "\n")
