import os
import sys

# Set environment variables before any other imports
os.environ['MPLBACKEND'] = 'TkAgg'

import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use('TkAgg', force=True)

print(f"Python version: {sys.version}")
print(f"Matplotlib version: {matplotlib.__version__}")
print(f"Backend being used: {matplotlib.get_backend()}")

# Now import the rest of the required modules
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class SimpleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Clean Test")
        
        # Create a simple frame
        frame = ttk.Frame(root, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create a figure and axis
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        
        # Create some data
        x = np.linspace(0, 2 * np.pi, 100)
        y = np.sin(x)
        
        # Plot the data
        self.ax.plot(x, y)
        self.ax.set_title("Simple Test Plot")
        self.ax.grid(True)
        
        # Create the canvas and add it to the frame
        self.canvas = FigureCanvasTkAgg(self.fig, master=frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Add a quit button
        quit_btn = ttk.Button(frame, text="Quit", command=root.quit)
        quit_btn.pack(pady=10)
        
        print("Application initialized successfully")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = SimpleApp(root)
        print("Starting main loop...")
        root.mainloop()
        print("Application closed successfully")
    except Exception as e:
        print(f"Error: {str(e)}")
        raise
