import React from 'react';
import * as d3 from 'd3';
import { bounds, c_list } from './constants';

function ColorLegend() {
  return (
    <div style={{
      position: 'absolute',
      top: '20px',
      right: '20px',
      background: 'white',
      padding: '10px',
      borderRadius: '5px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      border: '1px solid #ccc'
    }}>
      <svg width={320} height={70}>
        <text
          x={10}
          y={15}
          fontSize={12}
          fontWeight="bold"
        >
          PM2.5 Concentration (µg/m³) 
        </text>
        
        {/* Color bars */}
        {c_list.slice(0, -1).map((color, i) => (
          <rect
            key={i}
            x={10 + (i * (300 / (c_list.length - 1)))}
            y={25}
            width={300 / (c_list.length - 1)}
            height={20}
            fill={color}
          />
        ))}

        {/* Value labels */}
        {[0, 10, 20, 30, 50, 70, 90].map((value) => {
          const index = bounds.findIndex(b => b >= value);
          return (
            <text
              key={value}
              x={10 + (index * (300 / (bounds.length - 2)))}
              y={60}
              fontSize={10}
              textAnchor="middle"
            >
              {value}
            </text>
          );
        })}
      </svg>
    </div>
  );
}

export default ColorLegend; 