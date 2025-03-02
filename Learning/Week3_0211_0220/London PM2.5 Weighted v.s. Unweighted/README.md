# London PM2.5 Analysis and Visualization

## Overview
This repository contains a Python script for processing and visualizing PM2.5 concentration data for London using NetCDF files. The script extracts air pollution data from weighted and unweighted datasets, compares their values, and visualizes their differences.

## Features
### PM2.5 Data Extraction & Processing
- Reads PM2.5 concentration data from two NetCDF files:  
  - **Weighted dataset** (`concat_weighted_output.nc`)  
  - **Unweighted dataset** (`concat_unweighted_output.nc`)
- Retrieves geographical coordinates for London using the `geopy` library.
- Extracts PM2.5 values for London from the nearest grid point in the dataset.
- Converts `xarray.Dataset` objects into `pandas.DataFrame` for easy manipulation.
- Handles time format issues by converting `cftime` timestamps into `datetime`.

### Visualization & Analysis
- **PM2.5 Time Series Comparison**  
  - Plots **weighted vs. unweighted** PM2.5 concentration in London over time.
  - Saves the visualization as `london_pm25_comparison.png`.
  
- **PM2.5 Difference Analysis**  
  - Computes the difference between weighted and unweighted values.
  - Plots the difference over time to show the impact of weighting.
  - Saves the visualization as `london_pm25_difference.png`.

- **Statistical Insights**  
  - Computes the **weighting factor**, defined as:  
    ```
    Weighting Factor = PM25_WEIGHTED / PM25_UNWEIGHTED
    ```
  - Prints the average weighting factor for London.

## Requirements
### Python Libraries
The script relies on the following Python libraries:

- Core libraries:  
  `xarray`, `pandas`, `numpy`, `matplotlib`, `seaborn`, `geopy`

Install dependencies using:
```bash
pip install xarray pandas numpy matplotlib seaborn geopy
