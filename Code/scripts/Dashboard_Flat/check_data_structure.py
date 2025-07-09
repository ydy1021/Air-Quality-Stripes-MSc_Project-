#!/usr/bin/env python3
"""
检查PM2.5数据结构的脚本
"""

import json
import sys

def check_data_structure():
    """检查PM2.5数据的结构"""
    
    try:
        with open('public/pm25_2022_data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("=== PM2.5数据结构分析 ===")
        print(f"顶级键: {list(data.keys())}")
        
        # 检查metadata
        if 'metadata' in data:
            print("\n--- 元数据 ---")
            for key, value in data['metadata'].items():
                print(f"{key}: {value}")
        
        # 检查coordinates
        if 'coordinates' in data:
            print("\n--- 坐标信息 ---")
            if 'lats' in data['coordinates']:
                lats = data['coordinates']['lats']
                print(f"纬度数量: {len(lats)}")
                print(f"纬度范围: {min(lats):.2f} 到 {max(lats):.2f}")
            
            if 'lons' in data['coordinates']:
                lons = data['coordinates']['lons']
                print(f"经度数量: {len(lons)}")
                print(f"经度范围: {min(lons):.2f} 到 {max(lons):.2f}")
        
        # 检查data
        if 'data' in data:
            print("\n--- 数据点信息 ---")
            data_points = data['data']
            print(f"总数据点数量: {len(data_points)}")
            
            if len(data_points) > 0:
                print(f"数据点结构: {list(data_points[0].keys())}")
                print("\n前5个数据点示例:")
                for i, point in enumerate(data_points[:5]):
                    print(f"  {i+1}: lat={point['lat']:.2f}, lon={point['lon']:.2f}, value={point['value']:.2f}")
                
                # 统计数据分布
                values = [point['value'] for point in data_points]
                print(f"\nPM2.5值统计:")
                print(f"  最小值: {min(values):.2f}")
                print(f"  最大值: {max(values):.2f}")
                print(f"  平均值: {sum(values)/len(values):.2f}")
                
                # 检查地理分布
                lats = [point['lat'] for point in data_points]
                lons = [point['lon'] for point in data_points]
                print(f"\n实际数据地理分布:")
                print(f"  纬度范围: {min(lats):.2f} 到 {max(lats):.2f}")
                print(f"  经度范围: {min(lons):.2f} 到 {max(lons):.2f}")
        
        print("\n=== 数据单位说明 ===")
        print("这个数据是基于网格的全球PM2.5浓度数据，不是按国家或城市划分的。")
        print("每个数据点代表一个经纬度网格点的PM2.5浓度值（单位：µg/m³）。")
        print("地图着色时，会根据每个地理位置找到最近的网格点来获取PM2.5值。")
        
        return True
        
    except Exception as e:
        print(f"错误: {e}")
        return False

if __name__ == "__main__":
    success = check_data_structure()
    sys.exit(0 if success else 1) 