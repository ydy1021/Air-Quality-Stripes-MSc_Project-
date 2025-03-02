import os
import tkinter as tk
from PIL import Image, ImageTk

# Image storage directory (modify to your actual path)
image_dir = "E:\Master2\FYP\Global\Global\concat_weighted_figures2"  # Directory where your images are stored

# Set the range of years (e.g., 1850-2022)
years = list(range(1850, 2023))

# Initialize the Tkinter window
root = tk.Tk()
root.title("Generated Image Viewer")
root.geometry("1000x650")  # Set window size

# Load the first image initially
initial_year = years[0]
img_path = os.path.join(image_dir, f"{initial_year}.png")
if os.path.exists(img_path):
    img = Image.open(img_path)
    img = img.resize((800, 450), Image.Resampling.LANCZOS)
    img_tk = ImageTk.PhotoImage(img)
else:
    img_tk = None

# Create a Canvas to display the image
canvas = tk.Label(root, image=img_tk)
canvas.pack(pady=20)

# Create a label to display the selected year
year_label = tk.Label(root, text=str(initial_year), font=("Arial", 16, "bold"))
year_label.pack()

# Function to update the image and year label
def update_image(value):
    year = int(float(value))
    img_path = os.path.join(image_dir, f"{year}.png")
    if os.path.exists(img_path):
        img = Image.open(img_path)
        img = img.resize((800, 450), Image.Resampling.LANCZOS)
        img_tk = ImageTk.PhotoImage(img)
        canvas.config(image=img_tk)
        canvas.image = img_tk  # Prevent garbage collection issue
    year_label.config(text=str(year))

# Create a slider to switch images by year
slider = tk.Scale(
    root, from_=min(years), to=max(years), orient="horizontal",
    length=850, resolution=1, tickinterval=10, showvalue=False, command=update_image
)
slider.set(initial_year)
slider.pack(pady=10)

# Run the Tkinter main loop
root.mainloop()
