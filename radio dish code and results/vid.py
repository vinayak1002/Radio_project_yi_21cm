import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# 1. Physical Parameters
fs = 2400000
nfft = 2048

# 2. Load pre-processed spectra
data = np.fromfile('milky_way_data_10mins.dat', dtype=np.float32)
spectra_matrix = data.reshape(-1, nfft)
num_frames = spectra_matrix.shape[0]

print(f"Total video frames (seconds): {num_frames}")

# 3. Setup plot layout
fig, ax = plt.subplots(figsize=(10, 6))
x_axis = np.linspace(-fs/2, fs/2, nfft) / 1e6 + 1420.405

# NO FFTSHIFT: Read the row directly
initial_data = spectra_matrix[0]
line, = ax.plot(x_axis, initial_data, lw=1.5, color='tab:blue')

# Dynamic Y-axis limits with 10% padding
y_min = np.min(spectra_matrix)
y_max = np.max(spectra_matrix)
padding = (y_max - y_min) * 0.1
ax.set_ylim(y_min - padding, y_max + padding)

ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Relative Power')
ax.set_title('Galactic Center Transit - 10 Minute Time Lapse')
ax.grid(True, linestyle='--', alpha=0.6)

# 4. Animation loop
def update(frame):
    # NO FFTSHIFT: Read row directly
    frame_data = spectra_matrix[frame]
    line.set_ydata(frame_data)
    return line,

# 5. Render video
ani = animation.FuncAnimation(fig, update, frames=num_frames, blit=True)
ani.save('sagittarius_transit.mp4', writer='ffmpeg', fps=30)
print("Render complete: saved as sagittarius_transit.mp4")
