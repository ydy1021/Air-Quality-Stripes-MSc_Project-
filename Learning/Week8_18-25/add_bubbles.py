import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation

# ====== 1) Read the main CSV file, named "V1pt6_Cities_Data_PM2pt5.csv" ======
df = pd.read_csv("V1pt6_Cities_Data_PM2pt5.csv", encoding="utf-8-sig")

# ====== 2) Specify the target city, e.g., "Beijing, China" ======
target_city = "Beijing, China"

# ====== 3) Output folder for saving the animation ======
output_dir = r"E:\Master2\FYP\Global\Global\bubbles"
os.makedirs(output_dir, exist_ok=True)

# ====== 4) Read the bubble text and offset CSV files ======
#     Assumed structure:
#     - First column: Year
#     - Following columns: city names (matching the main CSV)
#     - Row index: years; each cell contains either text or offset or is empty
bubbles_text_df = pd.read_csv("bubbles_text.csv", index_col=0, encoding="utf-8-sig")
bubbles_offset_df = pd.read_csv("bubbles_offset.csv", index_col=0, encoding="utf-8-sig")

# ====== 5) Define color boundaries (BoundaryNorm) and discrete colormap (ListedColormap) ======
bounds = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 99999]
c_list = [
    (164 / 255, 255 / 255, 255 / 255),  # 0 - 5    Very Good
    (176 / 255, 218 / 255, 233 / 255),  # 5 - 10   Fair (down)
    (176 / 255, 206 / 255, 237 / 255),  # 10 - 15  Fair (up)
    (249 / 255, 224 / 255, 71 / 255),   # 15 - 20  Moderate (down)
    (242 / 255, 200 / 255, 75 / 255),   # 20 - 30  Moderate (up)
    (241 / 255, 166 / 255, 63 / 255),   # 30 - 40  Poor (down)
    (233 / 255, 135 / 255, 37 / 255),   # 40 - 50  Poor (up)
    (175 / 255, 69 / 255, 83 / 255),    # 50 - 60  Very Poor (down)
    (134 / 255, 59 / 255, 71 / 255),    # 60 - 70  Very Poor (up)
    (103 / 255, 58 / 255, 61 / 255),    # 70 - 80  Extremely Poor (down)
    (70 / 255, 47 / 255, 48 / 255),     # 80 - 90  Extremely Poor (mid)
    (37 / 255, 36 / 255, 36 / 255),     # 90+      Extremely Poor (up)
]
cmap = mcolors.ListedColormap(c_list)
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# ====== 6) Extract year column and PM2.5 values for the target city ======
years = df["Year"].to_numpy()
if target_city not in df.columns:
    raise ValueError(f"Target city {target_city} not found in the CSV file!")
pm25_values = df[target_city].to_numpy()

# ====== 7) Extract bubble text and offset data for the target city ======
#     Structure: index=Year, columns=City names => cell=text/offset
#     To display bubbles in the animation only for the appropriate years,
#     first extract all valid years with non-empty content
bubble_info = []  # Will store tuples: (year, text, offset_x, offset_y)
all_years_in_text = bubbles_text_df.index.intersection(bubbles_offset_df.index)

for y in all_years_in_text:
    try:
        year_int = int(y)
    except ValueError:
        continue

    text_val = bubbles_text_df.loc[y, target_city] if target_city in bubbles_text_df.columns else None
    offset_val = bubbles_offset_df.loc[y, target_city] if target_city in bubbles_offset_df.columns else None

    if pd.notnull(text_val) and str(text_val).strip() != "" and \
       pd.notnull(offset_val) and str(offset_val).strip() != "":
        try:
            ox_str, oy_str = offset_val.split(",")
            ox, oy = float(ox_str), float(oy_str)
        except:
            continue

        bubble_info.append((year_int, str(text_val).strip(), ox, oy))

bubble_info.sort(key=lambda x: x[0])  # Sort by year


# ====== 8) Define a function to generate the animation with bubbles ======
def create_animation_for_city(city_name, years, pm25_values, output_path):
    """
    city_name: str, name of the city
    years: 1D array-like, list of years
    pm25_values: 1D array-like, PM2.5 concentrations
    output_path: str, final .mp4 output file path
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    # (A) Draw the color strip using imshow
    ax.imshow(
        pm25_values.reshape(1, -1),
        aspect="auto",
        cmap=cmap,
        norm=norm,
        extent=[years[0], years[-1] + 1, 0, 1]
    )
    ax.set_yticks([])
    ax.set_xlim([years[0], years[-1] + 5])

    # (B) Overlay a white line on a second Y axis
    ax2 = ax.twinx()
    line, = ax2.plot([], [], color="white", linewidth=5, zorder=10)
    ax2.set_xlim([years[0], years[-1] + 1])
    ax2.set_ylim([0, 120])

    # (C) Set title
    ax.set_title(
        f"{city_name}\nAir pollution (PM2.5) concentrations",
        fontsize=14, fontweight="bold", pad=20
    )
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)

    added_annotations = {}  # Keep track of added annotations by year

    def init():
        line.set_data([], [])
        return (line,)

    def update(frame):
        xdata = years[:frame + 1]
        ydata = pm25_values[:frame + 1]
        line.set_data(xdata, ydata)

        current_year = years[frame]

        for (y_int, text_val, ox, oy) in bubble_info:
            if current_year >= y_int and y_int not in added_annotations:
                idx = np.where(years == y_int)[0]
                if len(idx) == 0:
                    continue
                idx = idx[0]
                bubble_yval = pm25_values[idx]

                ann = ax2.annotate(
                    text_val,
                    xy=(y_int, bubble_yval),
                    xytext=(y_int + ox, bubble_yval + oy),
                    arrowprops=dict(arrowstyle="->", color='black'),
                    bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="black", lw=1),
                    fontsize=9,
                    color="black",
                    zorder=11  # Make sure it's above the white line
                )
                added_annotations[y_int] = ann

        return (line,)

    anim = animation.FuncAnimation(
        fig, update,
        init_func=init,
        frames=len(years),
        interval=100,
        blit=True
    )

    anim.save(output_path, fps=10, dpi=150)
    plt.close(fig)


# ====== 9) Generate and save the animation ======
save_path = os.path.join(output_dir, f"{target_city}.mp4")
create_animation_for_city(target_city, years, pm25_values, save_path)
print("Animation for", target_city, "saved to:", save_path)
