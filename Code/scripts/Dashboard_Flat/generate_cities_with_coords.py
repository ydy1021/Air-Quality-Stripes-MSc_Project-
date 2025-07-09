import csv
import json
import os

# 文件路径
CITIES_PM25_CSV = 'V1pt6_Cities_Data_PM2pt5.csv'
WORLD_CITIES_CSV = os.path.join('worldcities', 'worldcities.csv')
OUTPUT_JSON = 'cities_with_coords.json'

# 1. 读取 worldcities.csv，建立 (city, country) -> (lat, lng) 映射
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

# 2. 读取 PM2.5 CSV 的表头，提取所有城市名和国家名
def extract_cities_from_pm25(filepath):
    with open(filepath, encoding='utf-8') as f:
        header = f.readline().strip()
    # 去掉 Year
    city_fields = header.split(',')[1:]
    city_country_list = []
    for field in city_fields:
        # 去除引号和多余空格
        field = field.strip().strip('"').strip()
        # 以最后一个逗号分割为城市和国家
        if ',' in field:
            parts = field.rsplit(',', 1)
            city = parts[0].strip()
            country = parts[1].strip()
            city_country_list.append((city, country))
        else:
            city_country_list.append((field.strip(), ''))
    return city_country_list

# 3. 匹配经纬度并生成 json
def main():
    city_dict = load_worldcities(WORLD_CITIES_CSV)
    city_country_list = extract_cities_from_pm25(CITIES_PM25_CSV)
    result = []
    missed = []
    for city, country in city_country_list:
        key = (city.lower(), country.lower())
        if key in city_dict:
            lat, lng = city_dict[key]
            matched_country = country  # 用原始 country
        else:
            # 尝试只用城市名匹配
            found = False
            for (c, co), (lat, lng) in city_dict.items():
                if c == city.lower():
                    matched_country = co.title()  # 用 worldcities.csv 里的 country
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
    # 输出 json
    with open(OUTPUT_JSON, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f'共匹配到 {len(result)} 个城市，未匹配到 {len(missed)} 个城市。')
    if missed:
        print('未匹配到的城市：')
        for m in missed:
            print(m)

if __name__ == '__main__':
    main() 