import os
import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.font_manager as fm

# ========== Configuration ==========
CSV_FILE = 'V1pt6_Cities_Data_PM2pt5.csv'
OUTPUT_DIR = os.path.abspath('.')

# ========== Color Scale and Color Map ==========
bounds = [0, 5, 10, 15, 20, 30, 40, 50, 60, 70, 80, 90, 99999]
c_list = [
    (164/255, 255/255, 255/255),  # 0 - 5    Very Good
    (176/255, 218/255, 233/255),  # 5 - 10   Fair(down)
    (176/255, 206/255, 237/255),  # 10 - 15  Fair(up)
    (249/255, 224/255, 71/255),   # 15 - 20  Moderate(down)
    (242/255, 200/255, 75/255),   # 20 - 30  Moderate(up)
    (241/255, 166/255, 63/255),   # 30 - 40  Poor(down)
    (233/255, 135/255, 37/255),   # 40 - 50  Poor(up)
    (175/255, 69/255, 83/255),    # 50 - 60  Very Poor(down)
    (134/255, 59/255, 71/255),    # 60 - 70  Very Poor(up)
    (103/255, 58/255, 61/255),    # 70 - 80  Extremely Poor(down)
    (70/255, 47/255, 48/255),     # 80 - 90  Extremely Poor(mid)
    (37/255, 36/255, 36/255),     # 90+      Extremely Poor(up)
]
cmap = mcolors.ListedColormap(c_list)
norm = mcolors.BoundaryNorm(bounds, cmap.N)

# ========== Calculate Years of Life Lost Function ==========
def calculate_years_of_life_lost(pm25_values):
    """
    Calculate Years of Life Lost (YLL)
    Based on research: For every 10μg/m³ increase in PM2.5, average life expectancy decreases by about 0.6 years
    """
    # WHO recommended safe level is 5μg/m³
    safe_level = 5.0
    # Calculate excess above safe level
    excess_pm25 = np.maximum(0, pm25_values - safe_level)
    # 0.6 years lost per 10μg/m³
    years_lost_per_year = excess_pm25 / 10.0 * 0.6
    # Cumulative years lost (assuming annual losses accumulate)
    total_years_lost = np.sum(years_lost_per_year)
    return total_years_lost

# ========== Generate Static Chart ==========
def create_static_chart(city_name, years, pm25_values, birth_year):
    """Generate static PM2.5 chart"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Set font for non-ASCII characters (if needed)
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Arial Unicode MS', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    # (A) Draw "stripe" using imshow
    ax.imshow(
        pm25_values.reshape(1, -1),
        aspect="auto",
        cmap=cmap,
        norm=norm,
        extent=[years[0], years[-1], 0, 1]
    )
    ax.set_yticks([])
    
    # (B) Overlay white line on second y-axis
    ax2 = ax.twinx()
    ax2.plot(years, pm25_values, color="white", linewidth=5)
    
    # Set x-axis range and format
    xlim = [years[0], years[-1]]
    ax.set_xlim(xlim)
    ax2.set_xlim(xlim)
    
    # Set x-axis tick format to integer
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: int(x)))
    
    ax2.set_ylabel("PM2.5 concentration (µg/m³)", color="white", fontweight='bold')
    
    # Force right Y-axis range to 0 ~ 120
    ax2.set_ylim([0, 120])
    
    # Add birth year marker
    if birth_year in years:
        birth_idx = np.where(years == birth_year)[0][0]
        birth_pm25 = pm25_values[birth_idx]
        ax2.axvline(x=birth_year, color='white', linestyle='--', linewidth=2, alpha=0.8)
        ax2.annotate(f'Birth Year\n{birth_year}', 
                    xy=(birth_year, birth_pm25), 
                    xytext=(birth_year + 5, birth_pm25 + 20),
                    arrowprops=dict(arrowstyle='->', color='white', lw=2),
                    color='black', fontweight='bold', fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.8))
    
    # (C) Set title and appearance
    ax.set_title(
        f"{city_name}\nAir pollution (PM2.5) concentrations since your birth",
        fontsize=14, fontweight="bold", pad=20
    )
    ax.set_xlabel("Year", fontweight='bold')
    ax.set_facecolor("white")
    for spine in ax.spines.values():
        spine.set_visible(False)
    
    # Add subtitle and URL in top-left corner
    fig.text(0.02, 0.98, "Air Quality Stripes", 
             fontsize=10, fontweight='bold', 
             ha='left', va='top')
    fig.text(0.02, 0.96, "https://airqualitystripes.info/", 
             fontsize=8, color='gray', 
             ha='left', va='top')
    
    plt.tight_layout()
    return fig

# ========== Main Window Class ==========
class StaticPM25Visualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Static PM2.5 Visualization - Birth Year Analysis")
        self.root.geometry("1000x800")
        
        # Read CSV data
        try:
            self.df = pd.read_csv(CSV_FILE)
            self.years = self.df["Year"].to_numpy()
            self.city_columns = [col for col in self.df.columns if col != "Year"]
        except Exception as e:
            messagebox.showerror("Error", f"Cannot read data file: {e}")
            return
        
        self.setup_ui()
    
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Left control panel
        control_frame = ttk.LabelFrame(main_frame, text="Control Panel", padding=10)
        control_frame.pack(side='left', fill='y', padx=(0, 10))
        
        # City search
        ttk.Label(control_frame, text="Search City:").pack(anchor='w')
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=30)
        self.search_entry.pack(fill='x', pady=(0, 5))
        self.search_entry.bind('<KeyRelease>', self.on_search)
        
        # City list
        ttk.Label(control_frame, text="Select City:").pack(anchor='w', pady=(10, 0))
        
        list_frame = ttk.Frame(control_frame)
        list_frame.pack(fill='both', expand=True, pady=(0, 10))
        
        self.city_listbox = tk.Listbox(list_frame, height=15, width=35)
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.city_listbox.yview)
        self.city_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.city_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        self.city_listbox.bind('<<ListboxSelect>>', self.on_city_select)
        
        # Birth year input
        ttk.Label(control_frame, text="Birth Year:").pack(anchor='w', pady=(10, 0))
        self.birth_year_var = tk.StringVar()
        birth_year_frame = ttk.Frame(control_frame)
        birth_year_frame.pack(fill='x', pady=(0, 10))
        
        self.birth_year_entry = ttk.Entry(birth_year_frame, textvariable=self.birth_year_var, width=15)
        self.birth_year_entry.pack(side='left')
        
        ttk.Label(birth_year_frame, text=f" ({self.years[0]}-{self.years[-1]})").pack(side='left')
        
        # Generate button
        self.generate_btn = ttk.Button(control_frame, text="Generate Analysis", command=self.generate_analysis)
        self.generate_btn.pack(pady=10)
        
        # Save button
        self.save_btn = ttk.Button(control_frame, text="Save Chart", command=self.save_chart)
        self.save_btn.pack(pady=(0, 10))
        self.save_btn.config(state='disabled')
        
        # Right display area
        display_frame = ttk.LabelFrame(main_frame, text="Analysis Results", padding=10)
        display_frame.pack(side='right', fill='both', expand=True)
        
        # Chart area
        self.chart_frame = ttk.Frame(display_frame)
        self.chart_frame.pack(fill='both', expand=True)
        
        # Statistics area
        self.stats_frame = ttk.LabelFrame(display_frame, text="Statistics", padding=10)
        self.stats_frame.pack(fill='x', pady=(10, 0))
        
        # Create text widget with larger font and better spacing
        self.stats_text = tk.Text(self.stats_frame, 
                                height=12,  # Increased height
                                wrap='word', 
                                font=('Arial', 12),  # Larger font
                                padx=10,    # Horizontal padding
                                pady=5)     # Vertical padding
        stats_scrollbar = ttk.Scrollbar(self.stats_frame, orient='vertical', command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scrollbar.set)
        
        self.stats_text.pack(side='left', fill='both', expand=True)
        stats_scrollbar.pack(side='right', fill='y')
        
        # Initialize city list
        self.populate_city_list(self.city_columns)
        
        # Store current chart
        self.current_figure = None
        self.current_city = None
        self.current_birth_year = None
    
    def populate_city_list(self, cities):
        """Populate city list"""
        self.city_listbox.delete(0, tk.END)
        for city in cities:
            self.city_listbox.insert(tk.END, city)
    
    def on_search(self, event=None):
        """Search cities"""
        search_term = self.search_var.get().lower()
        if not search_term:
            filtered_cities = self.city_columns
        else:
            filtered_cities = [city for city in self.city_columns 
                             if search_term in city.lower()]
        self.populate_city_list(filtered_cities)
    
    def on_city_select(self, event=None):
        """City selection event"""
        selection = self.city_listbox.curselection()
        if selection:
            city_name = self.city_listbox.get(selection[0])
            self.current_city = city_name
    
    def generate_analysis(self):
        """Generate analysis"""
        if not self.current_city:
            messagebox.showwarning("Warning", "Please select a city first")
            return
        
        try:
            birth_year = int(self.birth_year_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid birth year")
            return
        
        if birth_year < self.years[0] or birth_year > self.years[-1]:
            messagebox.showerror("Error", f"Birth year must be between {self.years[0]} and {self.years[-1]}")
            return
        
        self.current_birth_year = birth_year
        
        # Get city data from birth year
        city_data = self.df[self.current_city].values
        
        # Find birth year index
        birth_index = np.where(self.years == birth_year)[0]
        if len(birth_index) == 0:
            messagebox.showerror("Error", f"No data found for {birth_year}")
            return
        
        birth_index = birth_index[0]
        
        # Get data from birth year
        years_from_birth = self.years[birth_index:]
        pm25_from_birth = city_data[birth_index:]
        
        # Filter out NaN values
        valid_mask = ~np.isnan(pm25_from_birth)
        years_from_birth = years_from_birth[valid_mask]
        pm25_from_birth = pm25_from_birth[valid_mask]
        
        if len(pm25_from_birth) == 0:
            messagebox.showerror("Error", "No valid PM2.5 data found")
            return
            
        # Ensure data range is correct
        max_year = 2022  # Set maximum year to 2022
        if years_from_birth[-1] > max_year:
            # If data exceeds 2022, truncate to 2022
            valid_years_mask = years_from_birth <= max_year
            years_from_birth = years_from_birth[valid_years_mask]
            pm25_from_birth = pm25_from_birth[valid_years_mask]
        elif years_from_birth[-1] < max_year:
            # If data is less than 2022, extend to 2022
            years_to_add = np.arange(years_from_birth[-1] + 1, max_year + 1)
            years_from_birth = np.append(years_from_birth, years_to_add)
            pm25_from_birth = np.append(pm25_from_birth, [pm25_from_birth[-1]] * len(years_to_add))
        
        # Generate chart
        self.display_chart(years_from_birth, pm25_from_birth)
        
        # Calculate statistics
        self.calculate_and_display_stats(years_from_birth, pm25_from_birth, birth_year)
        
        # Enable save button
        self.save_btn.config(state='normal')
    
    def display_chart(self, years, pm25_values):
        """Display chart"""
        # Clear previous chart
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        # Create new chart
        self.current_figure = create_static_chart(self.current_city, years, pm25_values, self.current_birth_year)
        
        # Display chart in Tkinter
        canvas = FigureCanvasTkAgg(self.current_figure, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def calculate_and_display_stats(self, years, pm25_values, birth_year):
        """Calculate and display statistics"""
        # Clear previous statistics
        self.stats_text.delete(1.0, tk.END)
        
        # Basic statistics
        birth_pm25 = pm25_values[0]
        latest_pm25 = pm25_values[-1]
        avg_pm25 = np.mean(pm25_values)
        std_pm25 = np.std(pm25_values)
        min_pm25 = np.min(pm25_values)
        max_pm25 = np.max(pm25_values)
        
        # Change percentage
        if birth_pm25 != 0:
            change_percent = ((latest_pm25 - birth_pm25) / birth_pm25) * 100
        else:
            change_percent = 0
        
        # Years of life lost
        years_lost = calculate_years_of_life_lost(pm25_values)
        
        # WHO standard comparison
        who_standard = 5.0
        avg_excess = max(0, avg_pm25 - who_standard)
        
        # Generate statistics report
        stats_text = f"""📊 {self.current_city} PM2.5 Analysis Report
Data analysis from {birth_year} to {years[-1]}

🎂 Birth PM2.5 Concentration: {birth_pm25:.1f} μg/m³
📅 Latest PM2.5 Concentration: {latest_pm25:.1f} μg/m³

📈 Change Trend:
• PM2.5 Concentration Change: {change_percent:+.1f}%
{'• Air Quality Improved ✅' if change_percent < 0 else '• Air Quality Worsened ❌' if change_percent > 0 else '• Air Quality Unchanged ➖'}

📊 Statistics:
• Average Concentration: {avg_pm25:.1f} μg/m³
• Standard Deviation: {std_pm25:.1f} μg/m³
• Minimum Concentration: {min_pm25:.1f} μg/m³
• Maximum Concentration: {max_pm25:.1f} μg/m³

🏥 Health Impact Assessment:
• Estimated Years of Life Lost: {years_lost:.2f} years
• WHO Standard (5 μg/m³): Average Excess {avg_excess:.1f} μg/m³
• Data Range: {years[0]} - {years[-1]} ({len(years)} years)

💡 Note:
Years of life lost based on research: PM2.5 increase of 10μg/m³ reduces average lifespan by about 0.6 years
WHO recommends PM2.5 annual average concentration not exceeding 5μg/m³
"""
        
        self.stats_text.insert(1.0, stats_text)
        self.stats_text.config(state='disabled')
    
    def save_chart(self):
        """Save chart"""
        if self.current_figure is None:
            messagebox.showwarning("Warning", "No chart to save")
            return
        
        filename = f"{self.current_city.replace(', ', '_')}_{self.current_birth_year}_to_{self.years[-1]}.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        try:
            self.current_figure.savefig(filepath, dpi=150, bbox_inches='tight')
            messagebox.showinfo("Success", f"Chart saved to:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {e}")

# ========== Main Program Entry ==========
if __name__ == '__main__':
    # Check if data file exists
    if not os.path.exists(CSV_FILE):
        print(f"Error: Data file {CSV_FILE} not found")
        print("Please ensure the file is in the current directory")
        exit(1)
    
    root = tk.Tk()
    app = StaticPM25Visualizer(root)
    root.mainloop() 