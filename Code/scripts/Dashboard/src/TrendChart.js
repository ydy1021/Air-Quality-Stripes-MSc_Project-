import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

const PM25_CSV = 'V1pt6_Cities_Data_PM2pt5.csv';

function TrendChart({ selectedCities }) {
  const svgRef = useRef();
  const [data, setData] = useState(null);
  const [years, setYears] = useState([]);

  useEffect(() => {
    d3.csv(PM25_CSV).then(raw => {
      // First column is year, followed by cities
      const years = raw.map(row => +row['Year']);
      setYears(years);
      setData(raw);
    });
  }, []);

  useEffect(() => {
    if (!data || selectedCities.length !== 2) return;
    const width = 700, height = 350, margin = {top: 40, right: 40, bottom: 40, left: 60};
    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);
    svg.selectAll('*').remove();

    // Get city name format
    const getCol = c => `${c.city}, ${c.country}`;
    const city1 = getCol(selectedCities[0]);
    const city2 = getCol(selectedCities[1]);
    const y1 = data.map(row => +row[city1]);
    const y2 = data.map(row => +row[city2]);
    
    // Debug prints
    console.log('city1', city1);
    console.log('city2', city2);
    console.log('headers', Object.keys(data[0]));
    console.log('sample row', data[0]);

    // x/y axes
    const x = d3.scaleLinear().domain(d3.extent(years)).range([margin.left, width - margin.right]);
    const y = d3.scaleLinear().domain([0, d3.max([...y1, ...y2]) * 1.1]).range([height - margin.bottom, margin.top]);

    // Draw lines
    const line = d3.line()
      .x((d, i) => x(years[i]))
      .y(d => y(d));

    svg.append('path')
      .datum(y1)
      .attr('fill', 'none')
      .attr('stroke', '#1976d2')
      .attr('stroke-width', 2.5)
      .attr('d', line);
    svg.append('path')
      .datum(y2)
      .attr('fill', 'none')
      .attr('stroke', '#d32f2f')
      .attr('stroke-width', 2.5)
      .attr('d', line);

    // Draw points
    svg.selectAll('.dot1')
      .data(y1)
      .enter()
      .append('circle')
      .attr('class', 'dot1')
      .attr('cx', (d, i) => x(years[i]))
      .attr('cy', d => y(d))
      .attr('r', 3)
      .attr('fill', '#1976d2');
    svg.selectAll('.dot2')
      .data(y2)
      .enter()
      .append('circle')
      .attr('class', 'dot2')
      .attr('cx', (d, i) => x(years[i]))
      .attr('cy', d => y(d))
      .attr('r', 3)
      .attr('fill', '#d32f2f');

    // Axes
    svg.append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).tickFormat(d3.format('d')));
    svg.append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(y));

    // Title and legend
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', margin.top / 2)
      .attr('text-anchor', 'middle')
      .attr('font-size', 18)
      .attr('font-weight', 'bold')
      .text(`${city1} vs ${city2} `);

    // Legend distributed vertically, aligned to top-right
    const legendX = width - margin.right - 150; // Move left to avoid overflow
    const legendY1 = margin.top; // First row
    const legendY2 = margin.top + 25; // Second row
    const legendSpacing = 18;

    // First legend item
    svg.append('circle')
      .attr('cx', legendX)
      .attr('cy', legendY1)
      .attr('r', 6)
      .attr('fill', '#1976d2');
    svg.append('text')
      .attr('x', legendX + legendSpacing)
      .attr('y', legendY1 + 2)
      .text(city1)
      .attr('alignment-baseline', 'middle')
      .attr('font-size', 13)
      .attr('text-anchor', 'start');

    // Second legend item
    svg.append('circle')
      .attr('cx', legendX)
      .attr('cy', legendY2)
      .attr('r', 6)
      .attr('fill', '#d32f2f');
    svg.append('text')
      .attr('x', legendX + legendSpacing)
      .attr('y', legendY2 + 2)
      .text(city2)
      .attr('alignment-baseline', 'middle')
      .attr('font-size', 13)
      .attr('text-anchor', 'start');
  }, [data, years, selectedCities]);

  if (selectedCities.length !== 2) {
    return <div style={{textAlign: 'center', margin: 32, color: '#888'}}>Please select two cities for comparison</div>;
  }

  return (
    <div style={{textAlign: 'center'}}>
      <svg ref={svgRef}></svg>
    </div>
  );
}

export default TrendChart; 