# PM2.5 Visualization and Animation

## Overview
This repository contains two Python scripts for visualizing PM2.5 air pollution trends in multiple cities. The scripts generate animated visualizations to show changes in PM2.5 concentrations over time.

## Features

### 1️⃣ Interactive PM2.5 Animation (`local_animation.ipynb`)
- Generates an interactive **PM2.5 trend animation** for a selected city.
- Uses a **color-coded background** to represent air pollution levels.
- Displays a **progressive white line** to illustrate changes over time.
- Runs inside **Jupyter Notebook** (`%matplotlib notebook`).

### 2️⃣ Batch Animation Generator (`save_as_mp4.py`)
- Processes **multiple cities** from `selected_cities_pm25.csv`.
- Creates **MP4 animations** for each city.
- Saves the videos to the specified folder (`Videos_of_Vis`).

## Requirements
### Python Libraries
Install dependencies using:
```bash
pip install numpy pandas matplotlib ipympl

