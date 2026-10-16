import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fs = 2400000
nfft = 2048

# 1. Load the empty sky reference you will record on Saturday
off_data = np.fromfile('day2_10min_cold.dat', dtype=np.float32).reshape(-1, nfft)
off_mean = np.mean(off_data, axis=0) # This creates the 1D background dome to subtract

# 2. Load and stack your 35 minutes of Sagittarius transit data
data1 = np.fromfile('day2_10min.dat', dtype=np.float32).reshape(-1, nfft)
data2 = np.fromfile('day2_10min2.dat', dtype=np.float32).reshape(-1, nfft)
data3 = np.fromfile('day2_10min3.dat', dtype=np.float32).reshape(-1, nfft)

combined_spectra = np.vstack((data1, data2, data3))

num_frames = combined_spectra.shape[0]

# 3. Apply the calibration math to the ENTIRE 35-minute matrix at once
# Formula: (ON - OFF) / OFF
calibrated_matrix = (combined_spectra - off_mean) / off_mean

# 4. Setup Plot
fig, ax = plt.subplots(figsize=(10, 6))
x_axis = np.linspace(-fs/2, fs/2, nfft) / 1e6 + 1420.405

# Initialize with the first calibrated frame
line, = ax.plot(x_axis, calibrated_matrix[0], lw=1.5, color='tab:red')

# Set a much tighter Y-axis now that the massive dome is gone
ax.set_ylim(-0.05, 0.25)  
ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Calibrated Intensity (ON-OFF)/OFF')
ax.set_title('Sagittarius A* Transit - Calibrated')
ax.grid(True, linestyle='--', alpha=0.6)
ax.axvline(1420.405751, color='black', linestyle='--', alpha=0.7)

# 5. Animate
def update(frame):
    line.set_ydata(calibrated_matrix[frame])
    return line,

ani = animation.FuncAnimation(fig, update, frames=num_frames, blit=True)
ani.save('sagittarius_calibrated_transit.mp4', writer='ffmpeg', fps=30)
print("Render complete!")
