import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';
import PM25DataLoader from './PM25DataLoader';
import PM25Canvas from './PM25Canvas';
const WORLD_GEOJSON_URL = 'world-110m.geojson';
const CITIES_JSON = 'cities_with_coords.json';

import { bounds, c_list } from './constants';

function getColor(val) {
  if (val === null || val === undefined || isNaN(val)) return '#e0e0e0';
  for (let i = 0; i < bounds.length - 1; ++i) {
    if (val >= bounds[i] && val < bounds[i + 1]) return c_list[i];
  }
  return c_list[c_list.length - 1];
}

function Map({ onCitySelect, selectedCities, maxCities = 2 }) {
  const svgRef = useRef();
  const canvasRef = useRef();
  const [cities, setCities] = useState([]);
  const [world, setWorld] = useState(null);
  const [pm25Loader, setPm25Loader] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [transform, setTransform] = useState({ k: 1, x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [lastMouse, setLastMouse] = useState({ x: 0, y: 0 });
  const projectionRef = useRef(null);

  // Get PM2.5 value for a geographic location
  const getPM25ForLocation = (lat, lon) => {
    if (!pm25Loader) return null;
    return pm25Loader.getPM25Value(lat, lon);
  };

  // Load data
  useEffect(() => {
    const loadData = async () => {
      try {
        setIsLoading(true);
        
        const [worldData, citiesData] = await Promise.all([
          d3.json(WORLD_GEOJSON_URL),
          d3.json(CITIES_JSON)
        ]);
        
        if (worldData && worldData.features) {
          setWorld(worldData);
        }
        if (citiesData && Array.isArray(citiesData)) {
          setCities(citiesData);
        }

        // Load PM2.5 data
        const loader = new PM25DataLoader();
        const success = await loader.loadData();
        if (success) {
          setPm25Loader(loader);
          console.log('PM2.5 data stats:', loader.getDataStats());
        } else {
          console.warn('PM2.5 data loading failed, using default colors');
        }
        
      } catch (error) {
        console.error('Error loading data:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadData();
  }, []);

  // Mouse event handlers
  const handleMouseDown = (event) => {
    setIsDragging(true);
    setLastMouse({ x: event.clientX, y: event.clientY });
    event.preventDefault();
  };

  const handleMouseMove = (event) => {
    if (!isDragging) return;
    
    const deltaX = event.clientX - lastMouse.x;
    const deltaY = event.clientY - lastMouse.y;
    
    setTransform(prev => ({
      ...prev,
      x: prev.x + deltaX,
      y: prev.y + deltaY
    }));
    
    setLastMouse({ x: event.clientX, y: event.clientY });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  const handleWheel = (event) => {
    event.preventDefault();
    const rect = svgRef.current.getBoundingClientRect();
    const mouseX = event.clientX - rect.left;
    const mouseY = event.clientY - rect.top;
    
    const scale = event.deltaY > 0 ? 0.9 : 1.1;
    const newK = Math.min(Math.max(transform.k * scale, 0.5), 8);
    
    if (newK !== transform.k) {
      const factor = newK / transform.k;
      setTransform(prev => ({
        k: newK,
        x: mouseX - factor * (mouseX - prev.x),
        y: mouseY - factor * (mouseY - prev.y)
      }));
    }
  };

  // Zoom control functions
  const handleZoomIn = () => {
    setTransform(prev => ({
      ...prev,
      k: Math.min(prev.k * 1.5, 8)
    }));
  };

  const handleZoomOut = () => {
    setTransform(prev => ({
      ...prev,
      k: Math.max(prev.k / 1.5, 0.5)
    }));
  };

  const handleReset = () => {
    setTransform({ k: 1, x: 0, y: 0 });
  };

  // Render map
  useEffect(() => {
    if (!world || !world.features || !cities.length || isLoading || !svgRef.current || !canvasRef.current) return;
    
    try {
      const width = 1000, height = 500;
      const svg = d3.select(svgRef.current);
      
      // Clear previous content
      svg.selectAll('*').remove();
      
      // Set SVG dimensions
      svg.attr('width', width).attr('height', height);

      // Projection
      const mapProjection = d3.geoNaturalEarth1().fitSize([width, height], world);
      const path = d3.geoPath().projection(mapProjection);
      projectionRef.current = mapProjection;

      // Create main g element for zoom transformation
      const g = svg.append('g').attr('class', 'map-group');

      // Draw countries
      g.append('g')
        .attr('class', 'countries')
        .selectAll('path')
        .data(world.features)
        .enter()
        .append('path')
        .attr('d', path)
        .attr('fill', '#f0f0f0')
        .attr('stroke', '#666')
        .attr('stroke-width', 0.5)
        .style('pointer-events', 'all')
        .append('title')
        .text(d => {
          if (!d || !d.properties) return 'Unknown';
          const countryName = d.properties.NAME || d.properties.name || 'Unknown';
          try {
            const centroid = d3.geoCentroid(d);
            if (centroid && centroid.length >= 2) {
              const [lon, lat] = centroid;
              const pm25Value = getPM25ForLocation(lat, lon);
              return pm25Value !== null 
                ? `${countryName}\nCenter PM2.5 (2022): ${pm25Value.toFixed(1)} µg/m³`
                : `${countryName}`;
            }
          } catch (error) {
            console.warn('Error calculating centroid for country:', countryName, error);
          }
          return countryName;
        });

      // Draw city points
      const citiesGroup = g.append('g').attr('class', 'cities');
      
      cities.forEach(city => {
        const projected = mapProjection([city.lng, city.lat]);
        if (projected) {
          citiesGroup.append('circle')
            .attr('cx', projected[0])
            .attr('cy', projected[1])
            .attr('r', 5)
            .attr('fill', selectedCities.find(c => c.city === city.city && c.country === city.country) ? '#d32f2f' : '#1976d2')
            .attr('fill-opacity', 0.7)  // Set fill opacity to 70%
            .attr('stroke', '#fff')
            .attr('stroke-width', 2)
            .attr('stroke-opacity', 0.9)  // Set stroke opacity to 90%
            .style('cursor', 'pointer')
            .on('click', () => {
              if (onCitySelect) onCitySelect(city);
            })
            .append('title')
            .text(() => {
              const pm25Value = getPM25ForLocation(city.lat, city.lng);
              return pm25Value !== null 
                ? `${city.city}, ${city.country}\nPM2.5 (2022): ${pm25Value.toFixed(1)} µg/m³`
                : `${city.city}, ${city.country}\nPM2.5: No data`;
            });
        }
      });

      // Apply transformation
      g.attr('transform', `translate(${transform.x}, ${transform.y}) scale(${transform.k})`);
      
      // Adjust element sizes
      if (transform.k > 0) {
        citiesGroup.selectAll('circle')
          .attr('r', 5 / transform.k)
          .attr('stroke-width', 2 / transform.k);
        
        g.selectAll('.countries path')
          .attr('stroke-width', 0.5 / transform.k);
      }

      // Add zoom control buttons
      const controls = svg.append('g')
        .attr('class', 'zoom-controls')
        .raise();  // Move control buttons group to the top of SVG
      
      const buttonData = [
        { text: '+', action: handleZoomIn, title: 'Zoom in' },
        { text: '−', action: handleZoomOut, title: 'Zoom out' },
        { text: '⌂', action: handleReset, title: 'Reset' }
      ];

      buttonData.forEach((btn, i) => {
        const button = controls.append('g')
          .attr('class', 'zoom-button')
          .attr('transform', `translate(20, ${20 + i * 35})`)
          .style('cursor', 'pointer')
          .on('click', btn.action);

        button.append('rect')
          .attr('width', 30)
          .attr('height', 30)
          .attr('fill', 'white')
          .attr('stroke', '#ccc')
          .attr('rx', 3);

        button.append('text')
          .attr('x', 15)
          .attr('y', 20)
          .attr('text-anchor', 'middle')
          .attr('font-size', 16)
          .attr('font-weight', 'bold')
          .text(btn.text);

        button.append('title').text(btn.title);
      });

      // Initial Canvas render
      if (canvasRef.current && pm25Loader && pm25Loader.data) {
        try {
          const canvas = canvasRef.current;
          const ctx = canvas.getContext('2d');
          if (!ctx) {
            console.error('Failed to get canvas context');
            return;
          }
          PM25Canvas.renderPM25Data(ctx, pm25Loader.data.data, mapProjection, transform, cities, width, height);
        } catch (error) {
          console.error('Error rendering PM2.5 data:', error);
        }
      }
      
    } catch (error) {
      console.error('Error rendering map:', error);
    }
  }, [world, cities, selectedCities, onCitySelect, isLoading, transform, pm25Loader]);

  // Add global mouse event listeners
  useEffect(() => {
    const handleGlobalMouseMove = (event) => handleMouseMove(event);
    const handleGlobalMouseUp = () => handleMouseUp();

    if (isDragging) {
      document.addEventListener('mousemove', handleGlobalMouseMove);
      document.addEventListener('mouseup', handleGlobalMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleGlobalMouseMove);
      document.removeEventListener('mouseup', handleGlobalMouseUp);
    };
  }, [isDragging, lastMouse]);

  // Add wheel event listener
  useEffect(() => {
    const svg = svgRef.current;
    if (!svg) return;

    svg.addEventListener('wheel', handleWheel, { passive: false });

    return () => {
      svg.removeEventListener('wheel', handleWheel);
    };
  }, []);

  if (isLoading) {
    return (
      <div style={{ textAlign: 'center', margin: 20, color: '#666' }}>
        Loading PM2.5 data and map...
      </div>
    );
  }

  return (
    <div style={{ textAlign: 'center' }}>
      <div style={{ position: 'relative', display: 'inline-block' }}>
        <svg 
          ref={svgRef} 
          style={{ cursor: isDragging ? 'grabbing' : 'grab' }}
          onMouseDown={handleMouseDown}
        />
        
        {/* Canvas for rendering PM2.5 grid */}
        <canvas
          ref={canvasRef}
          width={1000}
          height={500}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            pointerEvents: 'none',
            zIndex: 1
          }}
        />
      </div>
    </div>
  );
}

export default Map; 