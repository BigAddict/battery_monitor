import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.animation import FuncAnimation
import numpy as np

# --- Load Data ---
df = pd.read_csv('battery_log.csv', names=['timestamp', 'percent', 'plugged'], header=0)

# --- Prepare Plot ---
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Space for the slider

# Convert timestamp to datetime (for better x-axis labels)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Plot initial data
line, = ax.plot(df['timestamp'], df['percent'], lw=2)
ax.set_ylabel('Battery %')
ax.set_xlabel('Timestamp')
ax.set_title('Battery Percentage Over Time')
ax.grid(True)

# Set initial view limits
window_size = 50  # Number of points visible at once
start_idx = 0
end_idx = min(window_size, len(df))

ax.set_xlim(df['timestamp'][start_idx], df['timestamp'][end_idx - 1])

# --- Add a Scroll Slider ---
ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(
    ax=ax_slider,
    label='Scroll',
    valmin=0,
    valmax=max(1, len(df) - window_size),
    valinit=0,
    valstep=1
)

# Update function for slider movement
def update(val):
    pos = int(slider.val)
    ax.set_xlim(df['timestamp'][pos], df['timestamp'][pos + window_size - 1])
    fig.canvas.draw_idle()

slider.on_changed(update)

# --- Live Data Simulation ---
# This function simulates new data coming in and updates the plot
def update_live(frame):
    global df
    # Simulate new data arriving by appending random values
    new_data = {
        'timestamp': pd.Timestamp.now(),
        'percent': np.random.randint(0, 100),  # Random battery percent
        'plugged': np.random.choice([True, False])  # Random plugged status
    }
    
    # Convert new data to DataFrame and concatenate it with the existing DataFrame
    new_df = pd.DataFrame([new_data])
    df = pd.concat([df, new_df], ignore_index=True)
    
    # Update the plot with the new data
    line.set_data(df['timestamp'], df['percent'])
    
    # Update the slider max value to allow for the extended dataset
    slider.valmax = len(df) - window_size
    slider.valinit = max(0, slider.val)

    # Re-set the x-axis limits based on the slider position
    pos = int(slider.val)
    ax.set_xlim(df['timestamp'][pos], df['timestamp'][pos + window_size - 1])

    return line,  # Return updated plot elements

# Create the animation
ani = FuncAnimation(fig, update_live, interval=1000)  # Update every 1 second

# Show the plot
plt.show()