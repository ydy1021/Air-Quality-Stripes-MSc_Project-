import os
import tkinter as tk
from PIL import Image, ImageTk

# Directory where images are stored
image_dir = "E:/Master2/FYP/Global/Global/Annual_figures"

# Generate the range of years (1998-2023)
years = list(range(1998, 2024))  # 1998 → 2023

# Initialize the Tkinter window
root = tk.Tk()
root.title("PM2.5 Concentration Viewer")
root.geometry("1000x650")  # Increase window size

# Load the first image initially
initial_year = years[0]
img_path = os.path.join(image_dir, f"{initial_year}.png")
img = Image.open(img_path)
img = img.resize((800, 450), Image.Resampling.LANCZOS)  # Resize image
img_tk = ImageTk.PhotoImage(img)

# Add a Canvas to the Tkinter window
canvas = tk.Label(root, image=img_tk)
canvas.pack(pady=20)

# Create a label to display the selected year
year_label = tk.Label(root, text=str(initial_year), font=("Arial", 16, "bold"))
year_label.pack()

# Update the image and year label
def update_image(value):
    year = int(float(value))  # Ensure the year is an integer
    img_path = os.path.join(image_dir, f"{year}.png")
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img = img.resize((800, 450), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        canvas.config(image=img_tk)
        canvas.image = img_tk  # Prevent garbage collection
    year_label.config(text=str(year))  # Update the year label

# Create a slider (increments by 1 year)
slider = tk.Scale(
    root, from_=min(years), to=max(years), orient="horizontal",
    length=850, resolution=1, tickinterval=5, showvalue=False, command=update_image
)
slider.set(initial_year)
slider.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
