# City-Level PM2.5 Concentration Visualization Toolkit

## Overview
This repository contains a Python script for processing and visualizing **city-level PM2.5 concentration data** from a CSV file.  
The dataset includes **PM2.5 data for 10 selected cities**, extracted from a larger Excel file containing global air pollution data.

### **Selected Cities:**
1. **Edinburgh, United Kingdom**  
2. **London, United Kingdom**  
3. **Cairo, Egypt**  
4. **Beijing, China**  
5. **Sydney, Australia**  
6. **New York City, USA**  
7. **Santiago, Chile**  
8. **Berlin, Germany**  
9. **Riyadh, Saudi Arabia**  
10. **Astana, Kazakhstan**  

These cities were selected from an **Excel dataset containing global air pollution records**, and their **PM2.5 concentration values were extracted** into `selected_cities_pm25.csv`.

## Features
### `generate_city_figures.py`: City PM2.5 Data Processing & Visualization
**Functionality:**
- Reads **PM2.5 concentration data** from `selected_cities_pm25.csv`.
- Processes historical air pollution trends for 10 selected cities.
- Uses **non-uniform color classification** to highlight pollution severity.
- Generates **heatmap-style visualizations** for each city.
- Overlays a **white trend line** on the heatmap for better readability.
- Saves **individual PM2.5 concentration charts** for each city in the output directory.

**Technologies Used:**
- **Data Handling:** `pandas` for loading and processing city-level PM2.5 data from CSV.
- **Data Visualization:** `matplotlib` for creating **color-coded heatmaps** and trend lines.
- **Color Mapping:** `matplotlib.colors.BoundaryNorm` for **non-uniform PM2.5 classification**.
- **File Management:** `os.makedirs()` ensures the output directory exists before saving images.

**How to Run:**
```bash
python generate_city_figures.py
