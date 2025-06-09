import os
import json
import pandas as pd
import re

# —— Configuration ——
csv_path = 'V1pt6_Cities_Data_PM2pt5.csv'  # Use full path if not in the same directory
output_dir = 'cities_json'  # Output directory
# —— end Configuration ——

# 1. Read CSV
df = pd.read_csv(csv_path)

# 2. Confirm the column name for "year"
year_col = 'Year'

# 3. Prepare the output directory
os.makedirs(output_dir, exist_ok=True)

# 4. Iterate through all city columns (skip the year column)
for col in df.columns:
    if col == year_col:
        continue
    # col format example: "Accra, Ghana" or "Abidjan, Côte d'Ivoire"
    # Split by the last comma
    city_raw, country_raw = col.rsplit(',', 1)
    city = city_raw.strip()
    country = country_raw.strip()

    # Extract year-value pairs for this column
    records = []
    for yr, val in zip(df[year_col], df[col]):
        if pd.isna(val):
            value = None
        else:
            value = float(val)
        records.append({
            "year": int(yr),
            "value": value
        })

    # Construct JSON object
    out_obj = {
        "city": city,
        "country": country,
        "data": records
    }

    # Generate a valid filename: city_country.json
    # Keep only alphanumeric characters, underscores, and hyphens
    def safe(s):
        # Remove all non-alphanumeric, non-space, non-underscore, and non-hyphen characters
        tmp = re.sub(r'[^\w\-\s]', '', s)
        # Replace spaces with underscores
        return tmp.replace(' ', '_')

    safe_city = safe(city)
    safe_country = safe(country)
    filename = f"{safe_city}_{safe_country}.json"

    out_path = os.path.join(output_dir, filename)
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(out_obj, f, ensure_ascii=False, indent=2)

print(f"Done: Generated JSON files for {len(df.columns) - 1} cities, saved in '{output_dir}/' directory.")
