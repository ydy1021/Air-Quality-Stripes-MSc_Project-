# PM2.5 Data Processing & Visualization Toolkit

## Overview
This repository contains two Python scripts designed for **processing, visualizing, and interactively exploring** PM2.5 concentration data from NetCDF files:

1. **NetCDF to Image Converter** (`generate_images.py`)  
   Extracts annual PM2.5 data from NetCDF files and generates standardized **global visualization maps**.

2. **Interactive Image Viewer** (`slider.py`)  
   Provides a **Tkinter-based GUI** with a **time slider** to browse PM2.5 concentration maps interactively.

## Features
### `generate_images.py`: PM2.5 Data Processing & Visualization
**Functionality:**
- Reads PM2.5 concentration data from a **NetCDF (.nc) file** using `xarray`.
- Detects time, latitude, longitude, and PM2.5 concentration values.
- Handles **CF-time (cftime)** formatted timestamps and converts them to standard `datetime` format.
- Uses **non-uniform color classification** for PM2.5 concentration to enhance visualization clarity.
- Generates **global PM2.5 heatmaps** for each year using `matplotlib` and saves them as PNG images.
- Automatically creates the **output directory** if it does not exist.
- Outputs progress updates to the **console**.

**Technologies Used:**
- **NetCDF Data Handling:** `xarray` for opening, reading, and processing `.nc` files.
- **Date Conversion:** `cftime` and `pandas.Timestamp` for handling NetCDF's non-standard date formats.
- **Data Visualization:** `matplotlib` and `pcolormesh()` for creating high-resolution heatmaps.
- **Color Mapping:** `matplotlib.colors.BoundaryNorm` for **non-uniform classification** of PM2.5 concentration levels.
- **File Management:** `os.makedirs()` ensures that the output directory exists before saving images.

**How to Run:**
```bash
python generate_images.py
