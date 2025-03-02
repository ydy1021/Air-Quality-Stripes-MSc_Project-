import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

# ====== 1) Read the CSV file, assuming it's in the same directory ======
df = pd.read_csv("selected_cities_pm25.csv")

# ====== 2) Define the output folder for saving images ======
output_dir = r"E:\Master2\FYP\Global\Global\cities_figures"
os.makedirs(output_dir, exist_ok=True)

# ====== 3) Define the color scale (BoundaryNorm) and discrete color map (ListedColormap) ======
#     Colors and PM2.5 concentration intervals are strictly defined as specified
bounds = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 99999]
c_list = [
    (164 / 255, 255 / 255, 255 / 255),  # 0 - 5    Very Good
    (176 / 255, 218 / 255, 233 / 255),  # 5 - 10   Fair (low)
    (176 / 255, 206 / 255, 237 / 255),  # 10 - 15  Fair (high)
    (249 / 255, 224 / 255, 71 / 255),   # 15 - 20  Moderate (low)
    (242 / 255, 200 / 255, 75 / 255),   # 20 - 30  Moderate (high)
    (241 / 255, 166 / 255, 63 / 255),   # 30 - 40  Poor (low)
    (233 / 255, 135 / 255, 37 / 255),   # 40 - 50  Poor (high)
    (175 / 255, 69 / 255, 83 / 255),    # 50 - 60  Very Poor (low)
    (134 / 255, 59 / 255, 71 / 255),    # 60 - 70  Very Poor (high)
    (103 / 255, 58 / 255, 61 / 255),    # 70 - 80  Extremely Poor (low)
    (70 / 255, 47 / 255, 48 / 255),     # 80 - 90  Extremely Poor (mid)
    (37 / 255, 36 / 255, 36 / 255),     # 90+      Extremely Poor (high)
]
cmap = mcolors.ListedColormap(c_list)
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# ====== 4) Extract the "Year" column and the list of cities ======
#    Assuming the first column in the CSV file is named "Year"
years = df["Year"].to_numpy()
city_cols = [col for col in df.columns if col != "Year"]

# ====== 5) Loop through each city column, generate plots, and save images ======
for city_name in city_cols:
    pm25_values = df[city_name].to_numpy()  # PM2.5 concentration values for the city

    # --- Create the figure ---
    fig, ax = plt.subplots(figsize=(12, 6))

    # (A) Use imshow to draw the "color strip"
    ax.imshow(
        pm25_values.reshape(1, -1),
        aspect="auto",
        cmap=cmap,
        norm=norm,
        extent=[years[0], years[-1] + 1, 0, 1]
    )
    ax.set_yticks([])
    ax.set_xlim([years[0], years[-1] + 1])

    # (B) Overlay a white trend line on the second Y-axis
    ax2 = ax.twinx()
    ax2.plot(years + 0.5, pm25_values, color="white", linewidth=5)
    ax2.set_xlim([years[0], years[-1] + 1])
    ax2.set_ylabel("PM2.5 concentration (µg/m³)", color="white")

    # ***** Key setting: Force the right Y-axis range to be fixed at 0 ~ 120 *****
    ax2.set_ylim([0, 120])

    # (C) Set title and appearance
    ax.set_title(
        f"{city_name}\nAir pollution (PM2.5) concentrations",
        fontsize=14, fontweight="bold", pad=20
    )
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)

    plt.tight_layout()

    # (D) Save to the specified folder with the city name as the filename
    save_path = os.path.join(output_dir, f"{city_name}.png")
    plt.savefig(save_path, dpi=150, bbox_inches="tight")
    plt.close(fig)

print("Done! All city figures saved to:", output_dir)
