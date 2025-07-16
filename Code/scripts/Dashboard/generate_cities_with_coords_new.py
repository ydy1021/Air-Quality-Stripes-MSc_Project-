import csv
import json

# File paths
cities_data_path = "V1pt6_Cities_Data_PM2pt5.csv"
worldcities_path = "worldcities/worldcities.csv"
output_path = "cities_with_coords.json"

# Step 1: Build (city, country) to (lat, lng) mapping from worldcities.csv
city_coords = {}

with open(worldcities_path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        city = row["city"].strip()
        country = row["country"].strip()
        lat = float(row["lat"])
        lng = float(row["lng"])
        city_coords[(city, country)] = {"lat": lat, "lng": lng}

# Step 2: Extract cities and countries from PM2.5 data file (headers are city-country combinations)
with open(cities_data_path, encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)

# Extract all (city, country) pairs, skip first column "Year"
city_country_pairs = []
for header in headers[1:]:
    if "," in header:
        parts = header.strip().rsplit(",", 1)
        if len(parts) == 2:
            city = parts[0].strip()
            country = parts[1].strip()
            city_country_pairs.append((city, country))

# Step 3: Match coordinates
matched_cities = []
unmatched_cities = []

for city, country in city_country_pairs:
    key = (city, country)
    if key in city_coords:
        matched_cities.append({
            "city": city,
            "country": country,
            "lat": city_coords[key]["lat"],
            "lng": city_coords[key]["lng"]
        })
    else:
        unmatched_cities.append((city, country))

# Step 4: Write to JSON file
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(matched_cities, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote to {output_path}, total matched cities: {len(matched_cities)}")
print(f"Number of unmatched cities: {len(unmatched_cities)}")

# Print list of unmatched cities
if unmatched_cities:
    print("List of unmatched cities:")
    for city, country in unmatched_cities:
        print(f"{city}, {country}")
