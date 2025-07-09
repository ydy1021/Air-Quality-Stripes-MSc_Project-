class PM25DataLoader {
  constructor() {
    this.data = null;
    this.gridData = null;
    this.isLoaded = false;
  }

  async loadData(url = 'pm25_2022_data.json') {
    try {
      console.log('Loading PM2.5 data from:', url);
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      this.data = await response.json();
      console.log('PM2.5 data loaded successfully');
      console.log('Data points:', this.data.data.length);
      console.log('Grid info:', this.data.metadata);
      
      // 创建快速查找的网格数据结构
      this.createGridLookup();
      this.isLoaded = true;
      return true;
      
    } catch (error) {
      console.error('Error loading PM2.5 data:', error);
      return false;
    }
  }

  createGridLookup() {
    // 创建一个基于坐标的快速查找表
    this.gridData = new Map();
    
    for (const point of this.data.data) {
      const key = `${point.lat.toFixed(2)}_${point.lon.toFixed(2)}`;
      this.gridData.set(key, point.value);
    }
    
    console.log('Grid lookup created with', this.gridData.size, 'points');
  }

  getPM25Value(lat, lon) {
    if (!this.isLoaded || !this.gridData) {
      return null;
    }

    // 首先尝试精确匹配
    const exactKey = `${lat.toFixed(2)}_${lon.toFixed(2)}`;
    if (this.gridData.has(exactKey)) {
      return this.gridData.get(exactKey);
    }

    // 如果没有精确匹配，找最近的点
    let minDistance = Infinity;
    let closestValue = null;

    for (const point of this.data.data) {
      const distance = Math.sqrt(
        Math.pow(point.lat - lat, 2) + Math.pow(point.lon - lon, 2)
      );
      
      if (distance < minDistance) {
        minDistance = distance;
        closestValue = point.value;
      }
      
      // 如果距离很小，直接返回
      if (distance < 0.1) {
        break;
      }
    }

    // 只返回距离合理的值（不超过1度）
    return minDistance < 1.0 ? closestValue : null;
  }

  // 获取数据统计信息
  getDataStats() {
    if (!this.isLoaded) return null;
    
    const values = this.data.data.map(d => d.value);
    return {
      min: Math.min(...values),
      max: Math.max(...values),
      count: values.length,
      metadata: this.data.metadata
    };
  }
}

export default PM25DataLoader; 