import React, { useState } from 'react';
import Map from './Map';
import TrendChart from './TrendChart';
import MultiTrendCharts from './MultiTrendCharts';
import './App.css';

function App() {
  const [selectedCities, setSelectedCities] = useState([]);
  const [mode, setMode] = useState('compare'); // 'compare' or 'multi'

  // 选择或取消城市
  const handleCitySelect = (city) => {
    setSelectedCities(prev => {
      const exists = prev.find(c => c.city === city.city && c.country === city.country);
      if (exists) {
        // 如果已选，点击则移除
        return prev.filter(c => !(c.city === city.city && c.country === city.country));
      }
      const max = mode === 'multi' ? 3 : 2;
      if (prev.length === max) return prev;
      return [...prev, city];
    });
  };

  // 切换模式时清空已选城市
  const handleModeChange = (newMode) => {
    setMode(newMode);
    setSelectedCities([]);
  };

  return (
    <div className="App">
      <h1>World PM2.5 Trend</h1>
      <div style={{textAlign: 'center', marginBottom: 16}}>
        <button onClick={() => handleModeChange('compare')} disabled={mode === 'compare'}>Compare Mode</button>
        <button onClick={() => handleModeChange('multi')} disabled={mode === 'multi'}>Multi Mode</button>
      </div>
      <Map onCitySelect={handleCitySelect} selectedCities={selectedCities} maxCities={mode === 'multi' ? 3 : 2} />
      {mode === 'compare'
        ? <TrendChart selectedCities={selectedCities} />
        : <MultiTrendCharts selectedCities={selectedCities} />}
    </div>
  );
}

export default App; 