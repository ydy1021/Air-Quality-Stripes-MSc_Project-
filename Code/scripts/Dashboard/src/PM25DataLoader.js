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
      
      // Create grid data structure for fast lookup
      this.createGridLookup();
      this.isLoaded = true;
      return true;
      
    } catch (error) {
      console.error('Error loading PM2.5 data:', error);
      return false;
    }
  }

  createGridLookup() {
    // Create a coordinate-based lookup table
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

    // Try exact match first
    const exactKey = `${lat.toFixed(2)}_${lon.toFixed(2)}`;
    if (this.gridData.has(exactKey)) {
      return this.gridData.get(exactKey);
    }

    // If no exact match, find the nearest point
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
      
      // If distance is very small, return immediately
      if (distance < 0.1) {
        break;
      }
    }

    // Only return values within reasonable distance (less than 1 degree)
    return minDistance < 1.0 ? closestValue : null;
  }

  // Get data statistics
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