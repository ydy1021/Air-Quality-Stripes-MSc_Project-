import os
import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import matplotlib.animation as animation
import re

# ====== 1) Set the directory for city JSON files ======
cities_json_dir = "cities_json"

# ====== 2) Specify the target city ======
target_city = "London, United Kingdom"

# ====== 3) Specify the output folder for the animation ======
output_dir = "."  # Current directory
os.makedirs(output_dir, exist_ok=True)

# ====== 4) Locate the corresponding JSON file ======
# Split city and country
city_name, country = target_city.split(", ")

# Same safe filename function as in split_cities.py
def safe(s):
    # Remove all non-alphanumeric characters, spaces, underscores, and hyphens
    tmp = re.sub(r'[^\w\-\s]', '', s)
    # Replace spaces with underscores
    return tmp.replace(' ', '_')

# Generate filename
safe_city = safe(city_name)
safe_country = safe(country)
json_filename = f"{safe_city}_{safe_country}.json"
json_file_path = os.path.join(cities_json_dir, json_filename)

# Check if file exists
if not os.path.exists(json_file_path):
    # If not found, try to list and fuzzy-match in the directory
    print(f"Exact file not found: {json_filename}")
    found = False

    for filename in os.listdir(cities_json_dir):
        if filename.endswith('.json'):
            parts = filename.replace('.json', '').split('_')
            if len(parts) >= 2:
                file_country = parts[-1]
                file_city = '_'.join(parts[:-1])
                if (file_city.lower() == safe_city.lower() and 
                    file_country.lower() == safe_country.lower()):
                    json_filename = filename
                    json_file_path = os.path.join(cities_json_dir, filename)
                    print(f"Matched file found: {filename}")
                    found = True
                    break

    if not found:
        raise FileNotFoundError(f"JSON file for city '{target_city}' not found")

# ====== 5) Read JSON data ======
with open(json_file_path, 'r', encoding='utf-8') as f:
    city_data = json.load(f)

# ====== 6) Extract year and PM2.5 values ======
data_points = city_data['data']
years = np.array([point['year'] for point in data_points])
pm25_values = np.array([point['value'] for point in data_points if point['value'] is not None])

# Ensure consistency (handle None values)
valid_indices = [i for i, point in enumerate(data_points) if point['value'] is not None]
years = np.array([data_points[i]['year'] for i in valid_indices])

# ====== 7) Define color scale and colormap ======
bounds = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 99999]
c_list = [
    (164/255, 255/255, 255/255),  # 0 - 5    Very Good
    (176/255, 218/255, 233/255),  # 5 - 10   Fair (lower)
    (176/255, 206/255, 237/255),  # 10 - 15  Fair (upper)
    (249/255, 224/255, 71/255),   # 15 - 20  Moderate (lower)
    (242/255, 200/255, 75/255),   # 20 - 30  Moderate (upper)
    (241/255, 166/255, 63/255),   # 30 - 40  Poor (lower)
    (233/255, 135/255, 37/255),   # 40 - 50  Poor (upper)
    (175/255, 69/255, 83/255),    # 50 - 60  Very Poor (lower)
    (134/255, 59/255, 71/255),    # 60 - 70  Very Poor (upper)
    (103/255, 58/255, 61/255),    # 70 - 80  Extremely Poor (lower)
    (70/255, 47/255, 48/255),     # 80 - 90  Extremely Poor (mid)
    (37/255, 36/255, 36/255),     # 90+      Extremely Poor (upper)
]
cmap = mcolors.ListedColormap(c_list)
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# ====== 8) Define text wrapping function ======
def wrap_text_to_two_lines(text):
    """
    Wrapping logic:
    - If length < 80, wrap at nearest space around midpoint;
    - If length >= 80, wrap at roughly one-third and two-thirds for three lines.
    """
    text = text.strip()
    n = len(text)
    if n == 0:
        return text
    if n < 80:
        target = int(n / 2)
        pos = text.rfind(" ", 0, target+1)
        if pos == -1:
            pos = target
        return text[:pos].rstrip() + "\n" + text[pos:].lstrip()
    else:
        target1 = int(n / 3)
        target2 = int(2 * n / 3)
        pos1 = text.rfind(" ", 0, target1+1)
        if pos1 == -1:
            pos1 = target1
        pos2 = text.rfind(" ", 0, target2+1)
        if pos2 == -1 or pos2 <= pos1:
            pos2 = target2
        line1 = text[:pos1].rstrip()
        line2 = text[pos1:pos2].lstrip().rstrip()
        line3 = text[pos2:].lstrip()
        return line1 + "\n" + line2 + "\n" + line3

# ====== 9) Extract bubble information from JSON ======
bubble_info = []

if 'bubbles' in city_data:
    for bubble in city_data['bubbles']:
        year = bubble.get('year')
        text = bubble.get('text')
        offset_x = bubble.get('offset_x', 0)
        offset_y = bubble.get('offset_y', 0)

        if year and text:
            wrapped_text = wrap_text_to_two_lines(text)
            bubble_info.append((year, wrapped_text, offset_x, offset_y))

# Fallback to CSV if no bubbles found (backward compatibility)
if not bubble_info and os.path.exists("bubbles_text.csv") and os.path.exists("bubbles_offset.csv"):
    try:
        import pandas as pd
        bubbles_text_df = pd.read_csv("bubbles_text.csv", index_col=0, encoding="utf-8-sig")
        bubbles_offset_df = pd.read_csv("bubbles_offset.csv", index_col=0, encoding="utf-8-sig")

        all_years_in_text = bubbles_text_df.index.intersection(bubbles_offset_df.index)

        for y in all_years_in_text:
            try:
                year_int = int(y)
            except ValueError:
                continue

            text_val = bubbles_text_df.get(target_city, pd.Series(dtype='object')).get(y, None)
            offset_val = bubbles_offset_df.get(target_city, pd.Series(dtype='object')).get(y, None)

            if pd.notnull(text_val) and str(text_val).strip() != "" and \
               pd.notnull(offset_val) and str(offset_val).strip() != "":
                wrapped_text = wrap_text_to_two_lines(str(text_val).strip())
                try:
                    ox_str, oy_str = offset_val.split(",")
                    ox, oy = float(ox_str), float(oy_str)
                except Exception:
                    continue
                bubble_info.append((year_int, wrapped_text, ox, oy))
    except Exception as e:
        print(f"Failed to read bubble CSV files: {e}")

bubble_info.sort(key=lambda x: x[0])

# ====== 10) Define function to generate animation with bubbles ======
def create_animation_for_city(city_name, country, years, pm25_values, output_path):
    fig, ax = plt.subplots(figsize=(12, 6))

    # (A) Draw background color stripe
    ax.imshow(
        pm25_values.reshape(1, -1),
        aspect="auto",
        cmap=cmap,
        norm=norm,
        extent=[years[0], years[-1] + 1, 0, 1]
    )
    ax.set_yticks([])
    ax.set_xlim([years[0], years[-1] + 5])

    # (B) Add white line using a second y-axis
    ax2 = ax.twinx()
    line, = ax2.plot([], [], color="white", linewidth=5, zorder=10)
    ax2.set_xlim([years[0], years[-1] + 1])
    ax2.set_ylim([0, 120])

    # (C) Set title and background
    ax.set_title(
        f"{city_name}, {country}\nAir pollution (PM2.5) concentrations",
        fontsize=14, fontweight="bold", pad=20
    )
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)

    added_annotations = {}

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
                    bbox=dict(boxstyle="round,pad=0.5", fc=(1, 1, 1, 0.5), ec="black", lw=1),
                    fontsize=9,
                    color="black",
                    zorder=11
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

# ====== 11) Generate and save animation ======
city_name_display = city_data.get('city', city_name)
country_display = city_data.get('country', country)
save_path = os.path.join(output_dir, f"{city_name_display}_{country_display}.mp4")
create_animation_for_city(city_name_display, country_display, years, pm25_values, save_path)
print(f"Animation saved to: {save_path}")
if bubble_info:
    print(f"{len(bubble_info)} bubble annotations added.")
else:
    print("Warning: No bubble annotations found.")
