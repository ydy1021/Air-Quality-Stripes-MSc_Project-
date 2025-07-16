#!/usr/bin/env python3
"""
Script to extract PM2.5 data for 2022
Extract PM2.5 data for 2022 from concat_weighted_output.nc file and save as lightweight JSON format
"""

import netCDF4 as nc
import numpy as np
import json
import sys
import os

def extract_pm25_2022():
    """Extract PM2.5 data for 2022"""
    
    # Input and output file paths
    input_file = 'public/concat_weighted_output.nc'
    output_file = 'public/pm25_2022_data.json'
    
    if not os.path.exists(input_file):
        print(f"Error: File not found {input_file}")
        return False
    
    try:
        print("Reading NetCDF file...")
        dataset = nc.Dataset(input_file, 'r')
        
        # Print file information
        print("File variables:", list(dataset.variables.keys()))
        print("File dimensions:", list(dataset.dimensions.keys()))
        
        # Try to find coordinate variables
        lat_var = None
        lon_var = None
        pm25_var = None
        time_var = None
        
        # Find latitude variable
        for var_name in ['lat', 'latitude', 'y']:
            if var_name in dataset.variables:
                lat_var = var_name
                break
        
        # Find longitude variable
        for var_name in ['lon', 'longitude', 'x']:
            if var_name in dataset.variables:
                lon_var = var_name
                break
        
        # Find PM2.5 variable
        for var_name in ['PM25_WEIGHTED', 'PM25', 'pm25', 'PM2_5', 'pm2_5']:
            if var_name in dataset.variables:
                pm25_var = var_name
                break
        
        # Find time variable
        for var_name in ['time', 't']:
            if var_name in dataset.variables:
                time_var = var_name
                break
        
        print(f"Found variables: lat={lat_var}, lon={lon_var}, pm25={pm25_var}, time={time_var}")
        
        if not all([lat_var, lon_var, pm25_var]):
            print("Error: Required variables not found")
            return False
        
        # Read coordinate data
        lats = dataset.variables[lat_var][:]
        lons = dataset.variables[lon_var][:]
        
        print(f"Latitude range: {np.min(lats):.2f} to {np.max(lats):.2f}")
        print(f"Longitude range: {np.min(lons):.2f} to {np.max(lons):.2f}")
        print(f"Grid size: {len(lats)} x {len(lons)}")
        
        # Read PM2.5 data
        pm25_data = dataset.variables[pm25_var]
        print(f"PM2.5 data shape: {pm25_data.shape}")
        print(f"PM2.5 data dimensions: {pm25_data.dimensions}")
        
        # Determine 2022 data index
        if time_var and time_var in dataset.variables:
            times = dataset.variables[time_var][:]
            print(f"Time dimension length: {len(times)}")
            
            # Assume last time step is 2022
            time_index = len(times) - 1
            print(f"Using time index: {time_index} (assumed to be 2022)")
            
            # Extract 2022 data
            # Data dimensions are (latitude, longitude, time)
            pm25_2022 = pm25_data[:, :, time_index]
        else:
            print("Time dimension not found, using all data")
            if len(pm25_data.shape) == 2:  # [lat, lon]
                pm25_2022 = pm25_data[:, :]
            else:
                print("Data dimensions do not match expectations")
                return False
        
        # Convert to numpy array and handle missing values
        pm25_2022 = np.array(pm25_2022)
        
        # Replace invalid values with None
        pm25_2022_clean = np.where(
            np.isnan(pm25_2022) | np.isinf(pm25_2022) | (pm25_2022 < 0),
            None,
            pm25_2022
        )
        
        print(f"2022 PM2.5 data shape: {pm25_2022_clean.shape}")
        
        # Calculate valid data statistics
        valid_data = pm25_2022_clean[pm25_2022_clean != None]
        if len(valid_data) > 0:
            print(f"Valid data points: {len(valid_data)} / {pm25_2022_clean.size}")
            print(f"PM2.5 range: {np.min(valid_data):.2f} to {np.max(valid_data):.2f}")
        
        # To reduce file size, we can lower the resolution
        # Sample every few points
        downsample_factor = 4  # This value can be adjusted
        
        lat_indices = np.arange(0, len(lats), downsample_factor)
        lon_indices = np.arange(0, len(lons), downsample_factor)
        
        lats_sampled = lats[lat_indices]
        lons_sampled = lons[lon_indices]
        pm25_sampled = pm25_2022_clean[np.ix_(lat_indices, lon_indices)]
        
        print(f"Grid size after downsampling: {len(lats_sampled)} x {len(lons_sampled)}")
        
        # Create output data structure
        output_data = {
            'metadata': {
                'description': 'PM2.5 concentration data for 2022',
                'units': 'µg/m³',
                'source': 'concat_weighted_output.nc',
                'lat_range': [float(np.min(lats_sampled)), float(np.max(lats_sampled))],
                'lon_range': [float(np.min(lons_sampled)), float(np.max(lons_sampled))],
                'grid_size': [len(lats_sampled), len(lons_sampled)],
                'downsample_factor': downsample_factor
            },
            'coordinates': {
                'lats': lats_sampled.tolist(),
                'lons': lons_sampled.tolist()
            },
            'data': []
        }
        
        # Convert data to sparse format to save space
        # Only save valid data points
        for i, lat in enumerate(lats_sampled):
            for j, lon in enumerate(lons_sampled):
                value = pm25_sampled[i, j]
                if value is not None and not np.isnan(value):
                    output_data['data'].append({
                        'lat': float(lat),
                        'lon': float(lon),
                        'value': float(value)
                    })
        
        print(f"Number of valid data points: {len(output_data['data'])}")
        
        # Save as JSON file
        print(f"Saving to {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        # Check file size
        file_size = os.path.getsize(output_file)
        print(f"Output file size: {file_size / 1024 / 1024:.2f} MB")
        
        dataset.close()
        print("Data extraction complete!")
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = extract_pm25_2022()
    sys.exit(0 if success else 1) 