# PM2.5 Data Processing and Visualization

This repository contains two Python scripts:
1. **`generate_pm25_maps.py`** - Processes NetCDF files containing PM2.5 data and generates annual PM2.5 concentration maps.
2. **`pm25_viewer.py`** - Provides a Tkinter-based interactive viewer to browse through the generated PM2.5 images.

---

## **1. PM2.5 Data Processing (`generate_pm25_maps.py`)**
This script reads NetCDF files containing PM2.5 concentration data, extracts relevant information, and generates yearly images.

### **Features**
✅ Reads PM2.5 data from NetCDF files.  
✅ Extracts relevant geospatial data (longitude, latitude).  
✅ Uses a non-uniform colormap (`plasma`) for better visualization.  
✅ Saves output images as PNG files with appropriate labels.  

### **Dependencies**
Before running the script, install the required libraries:
```bash
pip install xarray matplotlib numpy
