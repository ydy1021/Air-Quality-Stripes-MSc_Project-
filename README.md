# PM2.5 Air Quality Data Visualization Project

A comprehensive MSc Project focused on PM2.5 air quality data processing, analysis, and interactive visualization. This project is an extension of the [Air Quality Stripes](https://airqualitystripes.info/) project, which visualizes PM2.5 air pollution changes from 1850 to 2021 using stripe images inspired by Climate Stripes. 

Building upon this foundation, our project combines advanced data science techniques with modern web technologies to create more comprehensive and interactive visualizations of global air quality trends, offering enhanced analytical capabilities and user interaction features.

## 📋 Table of Contents

- [Overview](#overview)
- [Project Structure](#project-structure)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Components](#components)
  - [Data Processing Scripts](#data-processing-scripts)
  - [Static Visualization](#static-visualization)
  - [Interactive Dashboard](#interactive-dashboard)
  - [Animation Features](#animation-features)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Project Development](#project-development)
- [Contributing](#contributing)

## 🌍 Overview

This project provides a complete solution for PM2.5 (particulate matter ≤ 2.5 micrometers) air quality data analysis and visualization. It includes tools for:

- Processing raw NetCDF climate data files
- Generating static visualizations and charts
- Creating interactive web-based dashboards
- Animating temporal air quality changes
- Analyzing global air quality trends from 1980-2022

## 📁 Project Structure

```
├── 📂 Code/                    # Main implementation code
│   └── 📂 scripts/
│       ├── 📂 air-quality-static-ui/     # Static visualization generator
│       ├── 📂 air-quality-animation/     # Animation components
│       └── 📂 Dashboard/                 # Interactive React dashboard
├── 📂 Learning/                # Weekly project progress records
│   ├── 📂 Week1_0127_0203/
│   ├── 📂 Week2_0203_0210/
│   └── 📂 ...                  # Additional weekly progress
├── 📂 Work plan/               # Project planning and Gantt charts
├── 📂 Weekly meeting/          # Meeting records and discussions
└── 📄 README.md               # This file
```

## 🛠 Technology Stack

### Backend & Data Processing
- **Python 3.x** - Core data processing
- **xarray** - NetCDF data manipulation
- **numpy** - Numerical computations
- **matplotlib** - Static plotting

### Frontend & Visualization
- **React.js** - Interactive dashboard framework
- **D3.js** - Advanced data visualization
- **netcdfjs** - Client-side NetCDF file handling
- **topojson-client** - Geographic data processing

## 🚀 Quick Start

### Prerequisites
- [Node.js](https://nodejs.org/) (v14 or higher)
- [Python](https://python.org/) (v3.7 or higher)
- [Git](https://git-scm.com/)

### Clone the Repository
```bash
git clone <repository-url>
cd s2504850
```

## 🧩 Components

### 1. Data Processing Scripts

Core Python scripts for PM2.5 data processing:
- **`get_avg.py`** - Calculate annual mean from monthly data
- **`get_info.py`** - Inspect NetCDF file contents
- **`compare.py`** - Compare datasets and calculate differences

These scripts handle NetCDF climate data files and prepare processed data for visualization components.

### 2. Static Visualization
**Location**: `Code/scripts/air-quality-static-ui/`

Generate static PM2.5 visualizations and charts:
- City-specific air quality trends
- Global air quality maps
- Statistical analysis plots

**Features**:
- PNG export functionality
- Customizable time ranges
- Multiple visualization types

### 3. Interactive Dashboard
**Location**: `Code/scripts/Dashboard/`

A React-based interactive dashboard for exploring PM2.5 data:

**Setup & Run**:
```bash
cd Code/scripts/Dashboard/
npm install
npm start
```

**Features**:
- Real-time data filtering
- Interactive maps with D3.js
- Responsive design
- Time-series analysis tools

**View Dashboard**: Open [http://localhost:3000](http://localhost:3000) after running `npm start`

### 4. Animation Features
**Location**: `Code/scripts/air-quality-animation/`

Animated visualizations showing temporal changes in air quality.

## 💻 Installation & Setup

### 1. Python Environment Setup
```bash
# Install Python dependencies
pip install xarray numpy matplotlib pandas netcdf4
```

### 2. Node.js Dashboard Setup
```bash
# Navigate to dashboard directory
cd Code/scripts/Dashboard/

# Install dependencies
npm install

# Start development server
npm start
```

### 3. Data Requirements
- PM2.5 NetCDF data files
- City coordinates data (`worldcities/` directory)
- PM2.5 cities dataset (`V1pt6_Cities_Data_PM2pt5.csv`)

## 📖 Usage

### Running Data Processing
```bash
# Data processing scripts are available for:
# - Inspecting NetCDF data structure
# - Calculating annual averages from monthly data
# - Comparing different datasets
```

### Generating Static Visualizations
```bash
cd Code/scripts/air-quality-static-ui/
python static_pm25_visualizer.py
```

### Launching Interactive Dashboard
```bash
cd Code/scripts/Dashboard/
npm start
```

## 📈 Project Development


### Work Planning
Project timeline and milestones are documented in the `Work plan/` directory, including Gantt charts and deliverable schedules.

### Meeting Records
Weekly progress meetings and discussions are recorded in the `Weekly meeting/` directory.

## 📊 Data Sources

- Global PM2.5 concentration data (1850-2022)
- World cities geographical coordinates
- Climate data in NetCDF format
- Population and demographic data

## 🤝 Contributing

This is a MSc Project repository. The codebase in `Code/` represents the main implementation, while `Learning/` contains development progress for reference.

### Development Workflow
1. Main implementation: `Code/scripts/`
2. Progress tracking: `Learning/`
3. Planning: `Work plan/`
4. Documentation: `Weekly meeting/`

## 📄 License

This project is developed as part of a MSc Project for academic purposes.

## 📧 Contact

For questions about this project, please refer to the weekly meeting records or project documentation.

---

**Note**: The `Learning/` directory contains the author's personal development notes and progress records, mirroring the implementation found in `Code/`. Both directories contain similar content but serve different purposes in the project documentation workflow. 
