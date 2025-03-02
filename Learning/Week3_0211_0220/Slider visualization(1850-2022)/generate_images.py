import xarray as xr
import pandas as pd
import cftime
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os


def check_and_visualize_pm25(file_path, output_dir):
    # Open NetCDF file
    ds = xr.open_dataset(file_path)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Automatically detect PM2.5 variable name
    pm25_var = "PM25_WEIGHTED"

    if pm25_var not in ds.variables:
        print("❌ PM2.5 variable not found. Please check the NetCDF file.")
        print("Available variables:", list(ds.variables.keys()))
        return

    # Automatically detect longitude and latitude variables
    lon_var = "longitude"
    lat_var = "latitude"

    if lon_var not in ds.variables or lat_var not in ds.variables:
        print("❌ Longitude or latitude variable not found. Please check the NetCDF file.")
        print("Available variables:", list(ds.variables.keys()))
        return

    # Get time variable
    time_var = "time"
    if time_var not in ds.variables:
        print("Time dimension not found. Please check the file structure.")
        return

    # Retrieve time data
    time_values = ds[time_var].values

    # Handle CF-time date format
    if isinstance(time_values[0], cftime.datetime):
        time_values = [pd.Timestamp(t.strftime("%Y-%m-%d")) for t in time_values]
    else:
        time_values = pd.to_datetime(time_values)

    # Retrieve PM2.5 data and geographic coordinates
    pm25 = ds[pm25_var]
    lon = ds[lon_var]
    lat = ds[lat_var]

    # Define color levels (non-uniform)
    levels = [0, 5, 10, 15, 20, 30, 40, 50, 70, 90, 100]  # 100 as the upper limit to ensure >90 has a color
    cmap = plt.get_cmap("plasma")
    norm = mcolors.BoundaryNorm(levels, cmap.N)

    # Generate visualizations for each year
    years = sorted(set(t.year for t in time_values))
    for i, year in enumerate(years):
        plt.figure(figsize=(12, 6))
        plt.pcolormesh(lon, lat, pm25[..., i], shading='auto', cmap=cmap, norm=norm)

        # Customize color bar
        cbar = plt.colorbar(label="PM2.5 Concentration (µg/m³)", ticks=levels)
        cbar.set_ticks(levels[:-1] + [95])  # Use 95 to represent ">90"
        cbar.set_ticklabels([str(l) for l in levels[:-1]] + [">90"])

        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title(f"Global PM2.5 Concentration ({year})")

        # Save image
        output_file = os.path.join(output_dir, f"{year}.png")
        plt.savefig(output_file, dpi=300, bbox_inches="tight")
        plt.close()
        print(f"✅ Saved: {output_file}")

    print("🎉 All images have been successfully generated and saved!")

    ds.close()


if __name__ == "__main__":
    file_path = "concat_weighted_output.nc"
    output_dir = "E:/Master2/FYP/Global/Global/concat_weighted_figures"
    check_and_visualize_pm25(file_path, output_dir)
