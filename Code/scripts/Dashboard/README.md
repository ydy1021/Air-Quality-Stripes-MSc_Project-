# Air Quality Dashboard

This dashboard is an extension of the Air Quality Stripes project, providing interactive visualizations and analysis tools for PM2.5 data across global cities.

## Data Sources

The dashboard utilizes data from the Air Quality Stripes project:
- `V1pt6_Cities_Data_PM2pt5.csv`: Contains historical PM2.5 data for various cities
- `concat_weighted_output.nc`: A NetCDF file containing comprehensive air quality data

## Project Structure

### Data Processing Scripts

1. `extract_pm25_2022.py`
   - Extracts and processes PM2.5 data for the year 2022
   - Updates the dataset with the latest available information
   - Ensures data consistency and handles missing values

2. `generate_cities_with_coords_new.py`
   - Generates a JSON file containing city coordinates
   - Maps cities from the PM2.5 dataset to their geographical coordinates
   - Uses the `worldcities.csv` database for accurate location data
   - Output: `cities_with_coords.json` for map visualization

3. `check_data_structure.py`
   - Validates data structure and integrity
   - Performs quality checks on the input data
   - Ensures compatibility with the visualization components

### Web Dashboard Implementation

The dashboard is built using React and includes several key components:

#### Core Components

- `App.js`: Main application component and routing
- `Map.js`: Interactive world map visualization using GeoJSON
- `PM25Canvas.js`: PM2.5 data visualization canvas
- `MultiTrendCharts.js` & `TrendChart.js`: Time series trend visualization
- `ColorLegend.js`: Color scale legend for PM2.5 levels
- `ErrorBoundary.js`: Error handling component

#### Key Features

1. **Interactive World Map**
   - Displays global PM2.5 data distribution
   - City-level data points with color-coded indicators
   - Zoom and pan capabilities

2. **Time Series Visualization**
   - Historical PM2.5 trends for selected cities
   - Color-coded stripes indicating pollution levels
   - Interactive timeline navigation

3. **Data Analysis Tools**
   - Statistical analysis of PM2.5 trends
   - City comparison capabilities
   - Data export functionality

## Technical Stack

- **Frontend**: React.js
- **Data Visualization**: D3.js, Mapbox GL
- **Data Processing**: Python with pandas, numpy
- **Styling**: CSS Modules

## Deployment and Setup

1. **Prerequisites**
   ```bash
   # Install Python dependencies
   pip install pandas numpy matplotlib

   # Install Node.js dependencies
   cd Dashboard
   npm install
   ```

2. **Data Preparation**
   ```bash
   # Run data processing scripts
   python extract_pm25_2022.py
   python generate_cities_with_coords_new.py
   python check_data_structure.py
   ```

3. **Starting the Dashboard**
   ```bash
   # Development mode
   npm start

   # Production build
   npm run build
   ```

The dashboard will be available at `http://localhost:3000` by default.

## Configuration

Key configuration files:
- `src/constants.js`: Global constants and API endpoints
- `package.json`: Project dependencies and scripts
- `public/index.html`: HTML template

## Browser Compatibility

The dashboard is optimized for modern browsers:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Contributing

When contributing to this project:
1. Ensure data processing scripts are run before making changes
2. Test visualizations across different screen sizes
3. Verify data integrity with `check_data_structure.py` 