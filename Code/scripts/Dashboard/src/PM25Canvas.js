import { bounds, c_list } from './constants';

function getColor(val) {
  if (val === null || val === undefined || isNaN(val)) return '#e0e0e0';
  for (let i = 0; i < bounds.length - 1; ++i) {
    if (val >= bounds[i] && val < bounds[i + 1]) return c_list[i];
  }
  return c_list[c_list.length - 1];
}

// 将RGB字符串转换为RGB数组
function parseRGB(rgbString) {
  const match = rgbString.match(/rgb\((\d+),(\d+),(\d+)\)/);
  if (match) {
    return [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
  }
  return [224, 224, 224]; // 默认灰色
}

class PM25Canvas {
  static renderPM25Data(ctx, gridData, projection, transform, cities, width, height) {
    if (!ctx || !gridData || !projection) return;

    // 清空画布
    ctx.clearRect(0, 0, width, height);
    
    let renderedCount = 0;
    
    // 创建城市点位置集合，用于避让
    const cityPositions = cities.map(city => {
      const projected = projection([city.lng, city.lat]);
      if (!projected) return null;
      
      // 应用缩放变换
      const transformedX = projected[0] * transform.k + transform.x;
      const transformedY = projected[1] * transform.k + transform.y;
      
      return { x: transformedX, y: transformedY };
    }).filter(pos => pos !== null);
    
    // 创建ImageData对象用于批量像素操作
    const imageData = ctx.createImageData(width, height);
    const data = imageData.data;
    
    // 网格大小（根据缩放级别调整）
    const baseGridSize = 2;
    const gridSize = Math.max(1, Math.round(baseGridSize * transform.k));
    const cityAvoidRadius = 8; // 城市点周围的避让半径
    
    // 渲染每个网格点
    for (const point of gridData) {
      const projected = projection([point.lon, point.lat]);
      if (!projected) continue;
      
      // 应用缩放变换
      const transformedX = projected[0] * transform.k + transform.x;
      const transformedY = projected[1] * transform.k + transform.y;
      
      // 视口裁剪
      if (transformedX < -gridSize || transformedX >= width + gridSize || 
          transformedY < -gridSize || transformedY >= height + gridSize) continue;
      
      // 检查是否与城市点冲突
      const tooCloseToCity = cityPositions.some(cityPos => {
        const distance = Math.sqrt(
          Math.pow(transformedX - cityPos.x, 2) + 
          Math.pow(transformedY - cityPos.y, 2)
        );
        return distance < cityAvoidRadius;
      });
      
      if (tooCloseToCity) continue; // 跳过城市点附近的网格
      
      // 获取颜色
      const color = getColor(point.value);
      const [r, g, b] = parseRGB(color);
      
      // 增强颜色饱和度
      const enhancedR = Math.min(255, Math.round(r * 1.1));
      const enhancedG = Math.min(255, Math.round(g * 1.1));
      const enhancedB = Math.min(255, Math.round(b * 1.1));
      
      // 绘制网格点（小矩形）
      const startX = Math.max(0, Math.floor(transformedX - gridSize/2));
      const endX = Math.min(width - 1, Math.floor(transformedX + gridSize/2));
      const startY = Math.max(0, Math.floor(transformedY - gridSize/2));
      const endY = Math.min(height - 1, Math.floor(transformedY + gridSize/2));
      
      for (let px = startX; px <= endX; px++) {
        for (let py = startY; py <= endY; py++) {
          const index = (py * width + px) * 4;
          data[index] = enhancedR;     // Red
          data[index + 1] = enhancedG; // Green
          data[index + 2] = enhancedB; // Blue
          data[index + 3] = 180; // Alpha
        }
      }
      
      renderedCount++;
    }
    
    // 将ImageData绘制到canvas
    ctx.putImageData(imageData, 0, 0);
    
    console.log(`Canvas rendered ${renderedCount} grid points at scale ${transform.k.toFixed(2)}`);
  }
}

export default PM25Canvas; 