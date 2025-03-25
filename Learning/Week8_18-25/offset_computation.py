import pandas as pd

city_data = pd.read_excel("V1pt6_Cities_Data_PM2pt5.xlsx", engine="openpyxl")
print("Excel中的年份：", city_data["Year"].unique())
print("Excel中的城市：", list(city_data.columns[1:]))

bubble_text = pd.read_csv("bubbles_text.csv", index_col=0)
print("CSV中的年份（行索引）：", list(bubble_text.index))
print("CSV中的城市（列）：", list(bubble_text.columns))

def get_pm25(city, year):
    row = city_data[city_data["Year"] == year]
    if not row.empty:
        return row[city].values[0]
    else:
        return None

def compute_offset(pm25):
    offset_x = 5
    offset_y = -10 if pm25 > 60 else 10
    return offset_x, offset_y

offset_df = bubble_text.copy()

for year in offset_df.index:
    try:
        y_int = int(str(year).strip())
    except ValueError:
        print(f"行索引 {year} 无法转换为整数，跳过该行。")
        continue
    for city in offset_df.columns:
        bubble = offset_df.loc[year, city]
        if pd.notnull(bubble) and str(bubble).strip() != "":
            pm25 = get_pm25(city, y_int)
            if pm25 is not None:
                ox, oy = compute_offset(pm25)
                offset_df.loc[year, city] = f"{ox},{oy}"
                print(f"处理 {city} {y_int}: PM2.5={pm25} -> Offset=({ox},{oy})")
            else:
                print(f"{city} 在 {y_int} 找不到 PM2.5 数据。")
                offset_df.loc[year, city] = ""
        else:
            offset_df.loc[year, city] = ""

offset_df.to_csv("bubbles_offset.csv", encoding="utf-8-sig")
print("bubbles_offset.csv 已保存。")
