# PM2.5 Data Processing and Analysis

This repository contains three Python scripts for processing and analyzing PM2.5 data from NetCDF files using `xarray` and `numpy`. The scripts perform the following tasks:

1. **`calculate_annual_mean.py`** – Reads monthly PM2.5 data files for 1998, merges them, calculates the annual mean, and saves the result as a new NetCDF file.
2. **`explore_dataset.py`** – Loads and inspects the contents of a NetCDF file, displaying the first 20 rows of each variable.
3. **`compare_annual_data.py`** – Compares a precomputed annual mean dataset with the original monthly dataset and calculates the difference.

## Requirements

Before running the scripts, ensure you have the following Python packages installed:

```bash
pip install xarray numpy matplotlib
