import React, { useState } from 'react';
import Map from './Map';
import TrendChart from './TrendChart';
import MultiTrendCharts from './MultiTrendCharts';
import ColorLegend from './ColorLegend';
import './App.css';

function App() {
  const [selectedCities, setSelectedCities] = useState([]);
  const [mode, setMode] = useState('compare'); // 'compare' or 'multi'

  // Select or deselect a city
  const handleCitySelect = (city) => {
    setSelectedCities(prev => {
      const exists = prev.find(c => c.city === city.city && c.country === city.country);
      if (exists) {
        // If already selected, remove it
        return prev.filter(c => !(c.city === city.city && c.country === city.country));
      }
      const max = mode === 'multi' ? 3 : 2;
      if (prev.length === max) return prev;
      return [...prev, city];
    });
  };

  // Clear selected cities when switching modes
  const handleModeChange = (newMode) => {
    setMode(newMode);
    setSelectedCities([]);
  };

  return (
    <div className="App">
      <h1>World PM2.5 Trend</h1>
      <div style={{ position: 'relative' }}>
        <div style={{textAlign: 'center', marginBottom: 16}}>
          <button onClick={() => handleModeChange('compare')} disabled={mode === 'compare'}>Compare Mode</button>
          <button onClick={() => handleModeChange('multi')} disabled={mode === 'multi'}>Multi Mode</button>
        </div>
        <ColorLegend />
        <div style={{ marginTop: '80px' }}> {/* Container to move the map down */}
          <Map onCitySelect={handleCitySelect} selectedCities={selectedCities} maxCities={mode === 'multi' ? 3 : 2} />
          {mode === 'compare'
            ? <TrendChart selectedCities={selectedCities} />
            : <MultiTrendCharts selectedCities={selectedCities} />}
        </div>
      </div>
    </div>
  );
}

export default App; 