#!/usr/bin/env python3
"""
提取2022年PM2.5数据的脚本
从concat_weighted_output.nc文件中提取2022年的PM2.5数据，并保存为轻量级的JSON格式
"""

import netCDF4 as nc
import numpy as np
import json
import sys
import os

def extract_pm25_2022():
    """提取2022年的PM2.5数据"""
    
    # 输入和输出文件路径
    input_file = 'public/concat_weighted_output.nc'
    output_file = 'public/pm25_2022_data.json'
    
    if not os.path.exists(input_file):
        print(f"错误：找不到文件 {input_file}")
        return False
    
    try:
        print("正在读取NetCDF文件...")
        dataset = nc.Dataset(input_file, 'r')
        
        # 打印文件信息
        print("文件变量:", list(dataset.variables.keys()))
        print("文件维度:", list(dataset.dimensions.keys()))
        
        # 尝试找到坐标变量
        lat_var = None
        lon_var = None
        pm25_var = None
        time_var = None
        
        # 查找纬度变量
        for var_name in ['lat', 'latitude', 'y']:
            if var_name in dataset.variables:
                lat_var = var_name
                break
        
        # 查找经度变量
        for var_name in ['lon', 'longitude', 'x']:
            if var_name in dataset.variables:
                lon_var = var_name
                break
        
        # 查找PM2.5变量
        for var_name in ['PM25_WEIGHTED', 'PM25', 'pm25', 'PM2_5', 'pm2_5']:
            if var_name in dataset.variables:
                pm25_var = var_name
                break
        
        # 查找时间变量
        for var_name in ['time', 't']:
            if var_name in dataset.variables:
                time_var = var_name
                break
        
        print(f"找到的变量: lat={lat_var}, lon={lon_var}, pm25={pm25_var}, time={time_var}")
        
        if not all([lat_var, lon_var, pm25_var]):
            print("错误：未找到必需的变量")
            return False
        
        # 读取坐标数据
        lats = dataset.variables[lat_var][:]
        lons = dataset.variables[lon_var][:]
        
        print(f"纬度范围: {np.min(lats):.2f} 到 {np.max(lats):.2f}")
        print(f"经度范围: {np.min(lons):.2f} 到 {np.max(lons):.2f}")
        print(f"网格大小: {len(lats)} x {len(lons)}")
        
        # 读取PM2.5数据
        pm25_data = dataset.variables[pm25_var]
        print(f"PM2.5数据形状: {pm25_data.shape}")
        print(f"PM2.5数据维度: {pm25_data.dimensions}")
        
        # 确定2022年数据的索引
        if time_var and time_var in dataset.variables:
            times = dataset.variables[time_var][:]
            print(f"时间维度长度: {len(times)}")
            
            # 假设最后一个时间步是2022年
            time_index = len(times) - 1
            print(f"使用时间索引: {time_index} (假设为2022年)")
            
            # 提取2022年数据
            # 数据维度是 (latitude, longitude, time)
            pm25_2022 = pm25_data[:, :, time_index]
        else:
            print("未找到时间维度，使用所有数据")
            if len(pm25_data.shape) == 2:  # [lat, lon]
                pm25_2022 = pm25_data[:, :]
            else:
                print("数据维度不符合预期")
                return False
        
        # 转换为numpy数组并处理缺失值
        pm25_2022 = np.array(pm25_2022)
        
        # 替换无效值为None
        pm25_2022_clean = np.where(
            np.isnan(pm25_2022) | np.isinf(pm25_2022) | (pm25_2022 < 0),
            None,
            pm25_2022
        )
        
        print(f"2022年PM2.5数据形状: {pm25_2022_clean.shape}")
        
        # 计算有效数据统计
        valid_data = pm25_2022_clean[pm25_2022_clean != None]
        if len(valid_data) > 0:
            print(f"有效数据点: {len(valid_data)} / {pm25_2022_clean.size}")
            print(f"PM2.5范围: {np.min(valid_data):.2f} 到 {np.max(valid_data):.2f}")
        
        # 为了减小文件大小，我们可以降低分辨率
        # 每隔几个点采样一次
        downsample_factor = 4  # 可以调整这个值
        
        lat_indices = np.arange(0, len(lats), downsample_factor)
        lon_indices = np.arange(0, len(lons), downsample_factor)
        
        lats_sampled = lats[lat_indices]
        lons_sampled = lons[lon_indices]
        pm25_sampled = pm25_2022_clean[np.ix_(lat_indices, lon_indices)]
        
        print(f"降采样后网格大小: {len(lats_sampled)} x {len(lons_sampled)}")
        
        # 创建输出数据结构
        output_data = {
            'metadata': {
                'description': 'PM2.5 concentration data for 2022',
                'units': 'µg/m³',
                'source': 'concat_weighted_output.nc',
                'lat_range': [float(np.min(lats_sampled)), float(np.max(lats_sampled))],
                'lon_range': [float(np.min(lons_sampled)), float(np.max(lons_sampled))],
                'grid_size': [len(lats_sampled), len(lons_sampled)],
                'downsample_factor': downsample_factor
            },
            'coordinates': {
                'lats': lats_sampled.tolist(),
                'lons': lons_sampled.tolist()
            },
            'data': []
        }
        
        # 转换数据为稀疏格式以节省空间
        # 只保存有效的数据点
        for i, lat in enumerate(lats_sampled):
            for j, lon in enumerate(lons_sampled):
                value = pm25_sampled[i, j]
                if value is not None and not np.isnan(value):
                    output_data['data'].append({
                        'lat': float(lat),
                        'lon': float(lon),
                        'value': float(value)
                    })
        
        print(f"有效数据点数量: {len(output_data['data'])}")
        
        # 保存为JSON文件
        print(f"正在保存到 {output_file}...")
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        # 检查文件大小
        file_size = os.path.getsize(output_file)
        print(f"输出文件大小: {file_size / 1024 / 1024:.2f} MB")
        
        dataset.close()
        print("数据提取完成！")
        return True
        
    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = extract_pm25_2022()
    sys.exit(0 if success else 1) 