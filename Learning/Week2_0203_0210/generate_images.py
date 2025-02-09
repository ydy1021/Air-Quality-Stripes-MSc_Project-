import xarray as xr
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import os
import glob

# Set the directory containing NetCDF files (modify to your actual path)
data_dir = "E:/Master2/FYP/Global/Global/Annual"  # NetCDF folder
output_dir = "E:/Master2/FYP/Global/Global/Annual_figures"  # Output image folder
os.makedirs(output_dir, exist_ok=True)  # Ensure the output folder exists

# Match all NetCDF files following the naming pattern (199801-199812 to 202301-202312)
nc_files = sorted(glob.glob(os.path.join(data_dir, "V5GL0502.HybridPM25c_0p05.Global.??????-??????.nc")))

# Color levels (non-uniform)
levels = [0, 5, 10, 15, 20, 30, 40, 50, 70, 90]
cmap = plt.get_cmap("plasma")

# Process each NetCDF file
for nc_file in nc_files:
    # Extract the year (assuming a fixed file name format)
    year = nc_file.split(".")[-2][:4]  # Parse "1998" from "199801-199812"

    # Load the dataset
    ds = xr.open_dataset(nc_file)

    # Extract PM2.5 data and longitude/latitude
    pm25 = ds["GWRPM25"]
    lon = ds["lon"]
    lat = ds["lat"]

    # Set up the color mapping (custom non-uniform levels)
    norm = mcolors.BoundaryNorm(levels, cmap.N)

    # Plot the map
    plt.figure(figsize=(12, 6))
    plt.pcolormesh(lon, lat, pm25, shading='auto', cmap=cmap, norm=norm)
    plt.colorbar(label="PM2.5 Concentration (µg/m³)", ticks=levels)
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.title(f"Global PM2.5 Concentration ({year})")

    # Save the image
    output_file = os.path.join(output_dir, f"{year}.png")
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    plt.close()  # Close the figure to free memory

    print(f"✅ Saved: {output_file}")

print("🎉 All images have been successfully generated and saved!")
