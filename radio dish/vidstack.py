import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
nfft = 2048
fs = 2400000

# Load and reshape each dataset individually
data1 = np.fromfile('milky_way_data_10mins.dat', dtype=np.float32).reshape(-1, nfft)
data2 = np.fromfile('milky_way_data_5mins_v2.dat', dtype=np.float32).reshape(-1, nfft)
data3 = np.fromfile('milky_way_data_10mins_v2.dat', dtype=np.float32).reshape(-1, nfft)
data4 = np.fromfile('milky_way_data_10mins_v3.dat', dtype=np.float32).reshape(-1, nfft)

# Stack them sequentially into one massive timeline matrix
combined_spectra = np.vstack((data1, data2, data3, data4))

# Update your frame count dynamically based on the total combined rows
num_frames = combined_spectra.shape[0]
print(f"Total video frames (seconds): {num_frames}")
fig, ax = plt.subplots(figsize=(10, 6))
x_axis = np.linspace(-fs/2, fs/2, nfft) / 1e6 + 1420.405
# Calculate the true minimum and maximum across all 4 datasets
y_min = np.min(combined_spectra)
y_max = np.max(combined_spectra)

# Apply a 10% visual buffer to the top and bottom of the frame
padding = (y_max - y_min) * 0.1
ax.set_ylim(y_min - padding, y_max + padding)
# Initialize the plot using the first second of the combined timeline
initial_data = combined_spectra[0]
line, = ax.plot(x_axis, initial_data, lw=1.5, color='tab:blue')
def update(frame):
    # Dynamically pull the next second of data as the video plays
    frame_data = combined_spectra[frame]
    line.set_ydata(frame_data)
    return line,
# Compile the video and export via ffmpeg
ani = animation.FuncAnimation(fig, update, frames=num_frames, blit=True)
ani.save('sagittarius_full_transit.mp4', writer='ffmpeg', fps=30)
