import csv
import json
import os

# File paths
CITIES_PM25_CSV = 'V1pt6_Cities_Data_PM2pt5.csv'
WORLD_CITIES_CSV = os.path.join('worldcities', 'worldcities.csv')
OUTPUT_JSON = 'cities_with_coords.json'

# 1. Read worldcities.csv, build (city, country) -> (lat, lng) mapping
def load_worldcities(filepath):
    city_dict = {}
    with open(filepath, encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t') if '\t' in f.readline() else csv.DictReader(f)
        f.seek(0)
        for row in reader:
            city = row['city'].strip().lower()
            country = row['country'].strip().lower()
            lat = float(row['lat'])
            lng = float(row['lng'])
            city_dict[(city, country)] = (lat, lng)
    return city_dict

# 2. Read PM2.5 CSV header, extract all city and country names
def extract_cities_from_pm25(filepath):
    with open(filepath, encoding='utf-8') as f:
        header = f.readline().strip()
    # Remove Year
    city_fields = header.split(',')[1:]
    city_country_list = []
    for field in city_fields:
        # Remove quotes and extra spaces
        field = field.strip().strip('"').strip()
        # Split by the last comma into city and country
        if ',' in field:
            parts = field.rsplit(',', 1)
            city = parts[0].strip()
            country = parts[1].strip()
            city_country_list.append((city, country))
        else:
            city_country_list.append((field.strip(), ''))
    return city_country_list

# 3. Match coordinates and generate json
def main():
    city_dict = load_worldcities(WORLD_CITIES_CSV)
    city_country_list = extract_cities_from_pm25(CITIES_PM25_CSV)
    result = []
    missed = []
    for city, country in city_country_list:
        key = (city.lower(), country.lower())
        if key in city_dict:
            lat, lng = city_dict[key]
            matched_country = country  # Use original country
        else:
            # Try matching by city name only
            found = False
            for (c, co), (lat, lng) in city_dict.items():
                if c == city.lower():
                    matched_country = co.title()  # Use country from worldcities.csv
                    found = True
                    break
            if not found:
                missed.append(f'{city}, {country}')
                continue
        result.append({
            'city': city,
            'country': matched_country,
            'lat': lat,
            'lng': lng
        })
    # Output json
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f'Successfully matched {len(result)} cities, failed to match {len(missed)} cities.')
    if missed:
        print('Unmatched cities:')
        for m in missed:
            print(m)

if __name__ == '__main__':
    main() 