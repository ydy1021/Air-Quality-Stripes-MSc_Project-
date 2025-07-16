import { bounds, c_list } from './constants';

function getColor(val) {
  if (val === null || val === undefined || isNaN(val)) return '#e0e0e0';
  for (let i = 0; i < bounds.length - 1; ++i) {
    if (val >= bounds[i] && val < bounds[i + 1]) return c_list[i];
  }
  return c_list[c_list.length - 1];
}

// Convert RGB string to RGB array
function parseRGB(rgbString) {
  const match = rgbString.match(/rgb\((\d+),(\d+),(\d+)\)/);
  if (match) {
    return [parseInt(match[1]), parseInt(match[2]), parseInt(match[3])];
  }
  return [224, 224, 224]; // Default gray
}

class PM25Canvas {
  static renderPM25Data(ctx, gridData, projection, transform, cities, width, height) {
    if (!ctx || !gridData || !projection) return;

    // Clear canvas
    ctx.clearRect(0, 0, width, height);
    
    let renderedCount = 0;
    
    // Create city position set for avoidance
    const cityPositions = cities.map(city => {
      const projected = projection([city.lng, city.lat]);
      if (!projected) return null;
      
      // Apply zoom transformation
      const transformedX = projected[0] * transform.k + transform.x;
      const transformedY = projected[1] * transform.k + transform.y;
      
      return { x: transformedX, y: transformedY };
    }).filter(pos => pos !== null);
    
    // Create ImageData object for batch pixel operations
    const imageData = ctx.createImageData(width, height);
    const data = imageData.data;
    
    // Grid size (adjusted based on zoom level)
    const baseGridSize = 2;
    const gridSize = Math.max(1, Math.round(baseGridSize * transform.k));
    const cityAvoidRadius = 8; // Radius around city points to avoid
    
    // Render each grid point
    for (const point of gridData) {
      const projected = projection([point.lon, point.lat]);
      if (!projected) continue;
      
      // Apply zoom transformation
      const transformedX = projected[0] * transform.k + transform.x;
      const transformedY = projected[1] * transform.k + transform.y;
      
      // Viewport clipping
      if (transformedX < -gridSize || transformedX >= width + gridSize || 
          transformedY < -gridSize || transformedY >= height + gridSize) continue;
      
      // Check for collision with city points
      const tooCloseToCity = cityPositions.some(cityPos => {
        const distance = Math.sqrt(
          Math.pow(transformedX - cityPos.x, 2) + 
          Math.pow(transformedY - cityPos.y, 2)
        );
        return distance < cityAvoidRadius;
      });
      
      if (tooCloseToCity) continue; // Skip grid points near cities
      
      // Get color
      const color = getColor(point.value);
      const [r, g, b] = parseRGB(color);
      
      // Enhance color saturation
      const enhancedR = Math.min(255, Math.round(r * 1.1));
      const enhancedG = Math.min(255, Math.round(g * 1.1));
      const enhancedB = Math.min(255, Math.round(b * 1.1));
      
      // Draw grid point (small rectangle)
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
    
    // Draw ImageData to canvas
    ctx.putImageData(imageData, 0, 0);
    
    console.log(`Canvas rendered ${renderedCount} grid points at scale ${transform.k.toFixed(2)}`);
  }
}

export default PM25Canvas; 