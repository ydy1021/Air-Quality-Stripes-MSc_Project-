import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation

# ====== 1) Read the CSV file (assuming it's in the same directory) ======
df = pd.read_csv("selected_cities_pm25.csv")

# ====== 2) Specify the folder for saving the animations ======
output_dir = r"E:\Master2\FYP\Global\Global\cities_animations"
os.makedirs(output_dir, exist_ok=True)

# ====== 3) Define color scale (BoundaryNorm) and discrete colors (ListedColormap) ======
bounds = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 99999]
c_list = [
    (164 / 255, 255 / 255, 255 / 255),  # 0 - 5    Very Good
    (176 / 255, 218 / 255, 233 / 255),  # 5 - 10   Fair(down)
    (176 / 255, 206 / 255, 237 / 255),  # 10 - 15  Fair(up)
    (249 / 255, 224 / 255, 71 / 255),   # 15 - 20  Moderate(down)
    (242 / 255, 200 / 255, 75 / 255),   # 20 - 30  Moderate(up)
    (241 / 255, 166 / 255, 63 / 255),   # 30 - 40  Poor(down)
    (233 / 255, 135 / 255, 37 / 255),   # 40 - 50  Poor(up)
    (175 / 255, 69 / 255, 83 / 255),    # 50 - 60  Very Poor(down)
    (134 / 255, 59 / 255, 71 / 255),    # 60 - 70  Very Poor(up)
    (103 / 255, 58 / 255, 61 / 255),    # 70 - 80  Extremely Poor(down)
    (70 / 255, 47 / 255, 48 / 255),     # 80 - 90  Extremely Poor(mid)
    (37 / 255, 36 / 255, 36 / 255),     # 90+      Extremely Poor(up)
]
cmap = mcolors.ListedColormap(c_list)
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# ====== 4) Retrieve the 'Year' column and the list of cities ======
years = df["Year"].to_numpy()
city_cols = [col for col in df.columns if col != "Year"]

# -- For demonstration: pack the animation-generation procedure into a function --
def create_animation_for_city(city_name, years, pm25_values, output_path):
    """
    city_name: str, name of the city
    years: 1D array-like, the years
    pm25_values: 1D array-like, PM2.5 concentration values
    output_path: str, the final .mp4 file path to be saved
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # (A) Use imshow to draw the 'strip' (a solid rectangle that remains unchanged)
    ax.imshow(
        pm25_values.reshape(1, -1),
        aspect="auto",
        cmap=cmap,
        norm=norm,
        extent=[years[0], years[-1] + 1, 0, 1]
    )
    ax.set_yticks([])
    ax.set_xlim([years[0], years[-1] + 1])

    # (B) Overlay a white line on the second y-axis, but initially empty
    ax2 = ax.twinx()
    line, = ax2.plot([], [], color="white", linewidth=5)
    ax2.set_xlim([years[0], years[-1] + 1])
    ax2.set_ylim([0, 120])  # fixed from 0 to 120

    # (C) Set the title
    ax.set_title(
        f"{city_name}\nAir pollution (PM2.5) concentrations",
        fontsize=14, fontweight="bold", pad=20
    )
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)

    # -- Define the init function for animation frames --
    def init():
        line.set_data([], [])
        return (line,)

    # -- Define the update function for each frame: show only the first i points --
    def update(frame):
        # frame goes from 0 to len(years) - 1
        xdata = years[:frame + 1]
        ydata = pm25_values[:frame + 1]
        line.set_data(xdata, ydata)
        return (line,)

    # -- Create the animation object: frames is the number of years, interval=100 means 100ms per frame --
    anim = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=len(years),
        interval=100,
        blit=True
    )

    # -- Use ffmpegwriter or the default writer to save to mp4 --
    #    Make sure ffmpeg is installed
    anim.save(output_path, fps=10, dpi=150)
    plt.close(fig)  # close promptly

# ====== 5) Iterate over city columns to create an animation mp4 for each city ======
for city_name in city_cols:
    pm25_values = df[city_name].to_numpy()

    # Output mp4 file name
    save_path = os.path.join(output_dir, f"{city_name}.mp4")

    create_animation_for_city(
        city_name,
        years,
        pm25_values,
        save_path
    )

print("All done! Animations saved to:", output_dir)
