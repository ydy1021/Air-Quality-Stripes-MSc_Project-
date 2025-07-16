#!/usr/bin/env python3
"""
Script to check PM2.5 data structure
"""

import json
import sys

def check_data_structure():
    """Check the structure of PM2.5 data"""
    
    try:
        with open('public/pm25_2022_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("=== PM2.5 Data Structure Analysis ===")
        print(f"Top-level keys: {list(data.keys())}")
        
        # Check metadata
        if 'metadata' in data:
            print("\n--- Metadata ---")
            for key, value in data['metadata'].items():
                print(f"{key}: {value}")
        
        # Check coordinates
        if 'coordinates' in data:
            print("\n--- Coordinate Information ---")
            if 'lats' in data['coordinates']:
                lats = data['coordinates']['lats']
                print(f"Number of latitudes: {len(lats)}")
                print(f"Latitude range: {min(lats):.2f} to {max(lats):.2f}")
            
            if 'lons' in data['coordinates']:
                lons = data['coordinates']['lons']
                print(f"Number of longitudes: {len(lons)}")
                print(f"Longitude range: {min(lons):.2f} to {max(lons):.2f}")
        
        # Check data
        if 'data' in data:
            print("\n--- Data Point Information ---")
            data_points = data['data']
            print(f"Total number of data points: {len(data_points)}")
            
            if len(data_points) > 0:
                print(f"Data point structure: {list(data_points[0].keys())}")
                print("\nFirst 5 data points example:")
                for i, point in enumerate(data_points[:5]):
                    print(f"  {i+1}: lat={point['lat']:.2f}, lon={point['lon']:.2f}, value={point['value']:.2f}")
                
                # Calculate data distribution statistics
                values = [point['value'] for point in data_points]
                print(f"\nPM2.5 Value Statistics:")
                print(f"  Minimum: {min(values):.2f}")
                print(f"  Maximum: {max(values):.2f}")
                print(f"  Average: {sum(values)/len(values):.2f}")
                
                # Check geographical distribution
                lats = [point['lat'] for point in data_points]
                lons = [point['lon'] for point in data_points]
                print(f"\nActual Data Geographical Distribution:")
                print(f"  Latitude range: {min(lats):.2f} to {max(lats):.2f}")
                print(f"  Longitude range: {min(lons):.2f} to {max(lons):.2f}")
        
        print("\n=== Data Unit Description ===")
        print("This data represents global PM2.5 concentration on a grid basis, not by country or city.")
        print("Each data point represents the PM2.5 concentration (unit: µg/m³) at a latitude-longitude grid point.")
        print("When coloring the map, the PM2.5 value is obtained by finding the nearest grid point for each geographical location.")
        
        return True
        
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = check_data_structure()
    sys.exit(0 if success else 1) 