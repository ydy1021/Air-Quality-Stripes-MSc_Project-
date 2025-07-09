import csv
import json

# 文件路径
cities_data_path = "V1pt6_Cities_Data_PM2pt5.csv"
worldcities_path = "worldcities/worldcities.csv"
output_path = "cities_with_coords.json"

# 第一步：从 worldcities.csv 中建立 (city, country) 到 (lat, lng) 的映射
city_coords = {}

with open(worldcities_path, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        city = row["city"].strip()
        country = row["country"].strip()
        lat = float(row["lat"])
        lng = float(row["lng"])
        city_coords[(city, country)] = {"lat": lat, "lng": lng}

# 第二步：从 PM2.5 数据文件中提取城市和国家（表头就是城市和国家组合）
with open(cities_data_path, encoding="utf-8") as f:
    reader = csv.reader(f)
    headers = next(reader)

# 提取所有的 (city, country) 对，跳过第一列 "Year"
city_country_pairs = []
for header in headers[1:]:
    if "," in header:
        parts = header.strip().rsplit(",", 1)
        if len(parts) == 2:
            city = parts[0].strip()
            country = parts[1].strip()
            city_country_pairs.append((city, country))

# 第三步：匹配经纬度
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

# 第四步：写入 JSON 文件
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(matched_cities, f, indent=2, ensure_ascii=False)

print(f"成功写入 {output_path}，共匹配城市数量：{len(matched_cities)}")
print(f"未匹配城市数量：{len(unmatched_cities)}")

# 打印未匹配的城市列表
if unmatched_cities:
    print("未匹配城市列表：")
    for city, country in unmatched_cities:
        print(f"{city}, {country}")
