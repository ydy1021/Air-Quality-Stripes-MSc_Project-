import pandas as pd

#  Read PM2.5 data for all cities (Excel file)
#    Assume the first column is "Year", followed by columns for each city (column names are city names)
city_data = pd.read_excel("V1pt6_Cities_Data_PM2pt5.xlsx", engine="openpyxl")
print("Years in Excel:", city_data["Year"].unique())
print("Cities in Excel:", list(city_data.columns[1:]))

#  Read the bubble text pivot table (CSV file)
#    CSV structure: first column is Year, followed by cities; cells contain bubble text (non-empty means bubble exists)
bubble_text = pd.read_csv("bubbles_text.csv", index_col=0)
print("Years in CSV (row index):", list(bubble_text.index))
print("Cities in CSV (columns):", list(bubble_text.columns))

#  Define a function to retrieve PM2.5 value from city_data based on city and year
def get_pm25(city, year):
    row = city_data[city_data["Year"] == year]
    if not row.empty:
        return row[city].values[0]
    else:
        return None

#  Define a heuristic function to determine bubble offset based on PM2.5 value
def compute_offset(pm25):
    # Horizontal offset is fixed at 5
    offset_x = 5
    # If PM2.5 > 60, consider it high and place the bubble below the line (-10); otherwise above the line (+10)
    offset_y = -10 if pm25 > 60 else 10
    return offset_x, offset_y

# Create a new DataFrame to store offsets, same structure as bubble_text
offset_df = bubble_text.copy()

# iterate through each year (row index) and each city (column) to compute bubble offsets
for year in offset_df.index:
    try:
        y_int = int(str(year).strip())
    except ValueError:
        print(f"Row index {year} could not be converted to integer. Skipping this row.")
        continue
    for city in offset_df.columns:
        bubble = offset_df.loc[year, city]
        # Only calculate offset if the cell contains bubble text
        if pd.notnull(bubble) and str(bubble).strip() != "":
            pm25 = get_pm25(city, y_int)
            if pm25 is not None:
                ox, oy = compute_offset(pm25)
                offset_df.loc[year, city] = f"{ox},{oy}"
                print(f"Processing {city} {y_int}: PM2.5={pm25} -> Offset=({ox},{oy})")
            else:
                print(f"No PM2.5 data found for {city} in {y_int}.")
                offset_df.loc[year, city] = ""
        else:
            # Keep cell empty if no bubble text
            offset_df.loc[year, city] = ""


offset_df.to_csv("bubbles_offset.csv", encoding="utf-8-sig")
print("bubbles_offset.csv has been saved.")
