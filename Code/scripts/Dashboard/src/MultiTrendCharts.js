import React, { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

const PM25_CSV = 'V1pt6_Cities_Data_PM2pt5.csv';

// 色阶区间和颜色，与 10_cities_vis.py 保持一致
const bounds = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 99999];
const c_list = [
  'rgb(164,255,255)',  // 0 - 5
  'rgb(176,218,233)',  // 5 - 10
  'rgb(176,206,237)',  // 10 - 15
  'rgb(249,224,71)',   // 15 - 20
  'rgb(242,200,75)',   // 20 - 30
  'rgb(241,166,63)',   // 30 - 40
  'rgb(233,135,37)',   // 40 - 50
  'rgb(175,69,83)',    // 50 - 60
  'rgb(134,59,71)',    // 60 - 70
  'rgb(103,58,61)',    // 70 - 80
  'rgb(70,47,48)',     // 80 - 90
  'rgb(37,36,36)',     // 90+
];

function getColor(val) {
  for (let i = 0; i < bounds.length - 1; ++i) {
    if (val >= bounds[i] && val < bounds[i + 1]) return c_list[i];
  }
  return c_list[c_list.length - 1];
}

function SingleTrend({ city, country, data, years }) {
  const svgRef = useRef();

  useEffect(() => {
    if (!data || !city || !country) return;
    const width = 350, height = 250, margin = {top: 40, right: 20, bottom: 40, left: 50};
    const svg = d3.select(svgRef.current)
      .attr('width', width)
      .attr('height', height);
    svg.selectAll('*').remove();

    const col = `${city}, ${country}`;
    const y = data.map(row => +row[col]);
    if (!y.length || y.some(isNaN)) return;

    // 1. 色带背景
    const bandHeight = height - margin.top - margin.bottom;
    const bandY = margin.top;
    const bandWidth = (width - margin.left - margin.right) / years.length;
    years.forEach((year, i) => {
      svg.append('rect')
        .attr('x', margin.left + i * bandWidth)
        .attr('y', bandY)
        .attr('width', bandWidth)
        .attr('height', bandHeight)
        .attr('fill', getColor(y[i]))
        .attr('stroke', 'none');
    });

    // 2. Y轴范围固定 0~120
    const x = d3.scaleLinear().domain([years[0], years[years.length-1]+1]).range([margin.left, width - margin.right]);
    const yScale = d3.scaleLinear().domain([0, 120]).range([height - margin.bottom, margin.top]);

    // 3. 白色粗折线
    const line = d3.line()
      .x((d, i) => x(years[i] + 0.5))
      .y(d => yScale(d));
    svg.append('path')
      .datum(y)
      .attr('fill', 'none')
      .attr('stroke', 'white')
      .attr('stroke-width', 2)
      .attr('d', line);

    // 4. 坐标轴
// 控制最多显示 8 个刻度
const tickCount = 8;
const tickInterval = Math.ceil(years.length / tickCount);

// 选择固定间隔的年份作为刻度
const tickVals = [];
for (let i = 0; i < years.length; i += tickInterval) {
  tickVals.push(years[i]);
}

// 确保最后一年始终存在于刻度中
const lastYear = years[years.length - 1];
if (!tickVals.includes(lastYear)) {
  tickVals.push(lastYear);
}

// 去重，防止重复刻度导致重叠
const uniqueTickVals = Array.from(new Set(tickVals));

    
    svg.append('g')
      .attr('transform', `translate(0,${height - margin.bottom})`)
      .call(d3.axisBottom(x).tickFormat(d3.format('d')).tickValues(uniqueTickVals));
    svg.append('g')
      .attr('transform', `translate(${margin.left},0)`)
      .call(d3.axisLeft(yScale).ticks(6));

    // 5. 标题
    svg.append('text')
      .attr('x', width / 2)
      .attr('y', margin.top / 2)
      .attr('text-anchor', 'middle')
      .attr('font-size', 15)
      .attr('font-weight', 'bold')
      .text(`${city}, ${country}\n`);

    // 6. Y轴标签（右侧，白色）
    svg.append('text')
      .attr('x', width - margin.right + 5)
      .attr('y', margin.top)
      .attr('text-anchor', 'start')
      .attr('font-size', 12)
      .attr('fill', 'white')
      .attr('font-weight', 'bold')
      .attr('transform', `rotate(-90,${width - margin.right + 5},${margin.top + bandHeight/2})`)
     // .text('PM2.5 concentration (µg/m³)');

    // 7. 去除边框
    svg.selectAll('rect.background').remove();
  }, [data, years, city, country]);

  return <svg ref={svgRef} style={{background: 'white', borderRadius: 8, boxShadow: '0 2px 8px #0001'}}></svg>;
}

function MultiTrendCharts({ selectedCities }) {
  const [data, setData] = useState(null);
  const [years, setYears] = useState([]);

  useEffect(() => {
    d3.csv(PM25_CSV).then(raw => {
      setYears(raw.map(row => +row['Year']));
      setData(raw);
    });
  }, []);

  if (!selectedCities.length) return <div style={{textAlign: 'center', margin: 32, color: '#888'}}>Click the cities to see the trends</div>;

  return (
    <div style={{display: 'flex', justifyContent: 'center', gap: 24}}>
      {selectedCities.slice(0, 3).map((c, idx) =>
        <SingleTrend key={idx} city={c.city} country={c.country} data={data} years={years} />
      )}
    </div>
  );
}

export default MultiTrendCharts; 