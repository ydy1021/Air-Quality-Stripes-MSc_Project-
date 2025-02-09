# Global PM2.5 Concentration Visualization Toolkit

## Overview
This repository contains two Python scripts for processing and visualizing global PM2.5 concentration data:

1. **NetCDF to Image Converter** (`generate_images.py`)  
   Processes annual PM2.5 data from NetCDF files and generates standardized visualization maps.

2. **Interactive Viewer** (`slider.py`)  
   Provides a GUI application with a time slider to explore PM2.5 concentration maps across years (1998-2023).

## Features
### generate_images.py: Data Processing & Visualization
- Processes NetCDF files following pattern: `V5GL0502.HybridPM25c_0p05.Global.??????-??????.nc`
- Implements non-uniform color classification for scientific visualization
- Automatic output directory creation
- Progress tracking in console

### slider.py: Interactive Visualization
- Tkinter-based GUI with smooth year slider (1998-2023)
- Optimized image handling to prevent memory leaks

## Requirements
### Python Libraries
- Core:  
  `xarray`, `netCDF4`, `matplotlib`, `pillow`, `tkinter`

Install with:
```bash
pip install xarray netCDF4 matplotlib pillow