import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# ---------------------------------------------------------
# 1. Physical & Hardware Parameters
# ---------------------------------------------------------
fs = 2400000
nfft = 2048
f_rest = 1420.405751

x_axis = np.linspace(-fs/2, fs/2, nfft) / 1e6 + 1420.405

# ---------------------------------------------------------
# 2. Data Loading & Time-Averaging (The 20s Chunking)
# ---------------------------------------------------------
print("Loading data arrays...")

# Load the entire 30-minute Cygnus observation 
on_data_full = np.fromfile('day2_30min_cygnus.dat', dtype=np.float32).reshape(-1, nfft)

# We want 20 seconds per frame
chunk_size = 10
num_full_chunks = on_data_full.shape[0] // chunk_size

# Drop any trailing seconds that don't fit perfectly into a 20s block
truncated_on_data = on_data_full[:num_full_chunks * chunk_size]

# Reshape into (Number of Frames, 20 seconds, 2048 frequencies) and average the 20s blocks
chunked_on_data = truncated_on_data.reshape(num_full_chunks, chunk_size, nfft)
averaged_on_data = np.mean(chunked_on_data, axis=1)

num_frames = averaged_on_data.shape[0]

# Load the cold sky data and create the clean, 10-minute static baseline
off_data_full = np.fromfile('day2_30min_cold.dat', dtype=np.float32).reshape(-1, nfft)
off_mean_clean = np.mean(off_data_full[:600], axis=0)

# ---------------------------------------------------------
# 3. Figure Setup & Initialization
# ---------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))

line, = ax.plot(x_axis, np.zeros(nfft), lw=1.5, color='tab:red')

# Lock the Y-axis for the zero-centered signal
ax.set_ylim(-0.02, 0.12)  # Tightened limits slightly since the noise will be much lower

ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Calibrated Intensity (Relative)')
ax.set_title('Cygnus Transit - 10s Averaged Time-Lapse')
ax.grid(True, linestyle='--', alpha=0.6)
ax.axvline(f_rest, color='black', linestyle='--', alpha=0.7, label='Rest Frequency (0 km/s)')
ax.legend(loc='upper right')

# ---------------------------------------------------------
# 4. The Animation Loop
# ---------------------------------------------------------
print(f"Total smoothed frames to render: {num_frames}")

def update(frame):
    # Grab the pre-averaged 20-second chunk
    raw_frame = averaged_on_data[frame]
    
    # Apply calibration
    calibrated_frame = (raw_frame - off_mean_clean) / off_mean_clean
    
    # Calculate noise floor and zero-center
    baseline_level = np.median(calibrated_frame[x_axis < 1420.0])
    final_frame = calibrated_frame - baseline_level
    
    line.set_ydata(final_frame)
    
    if frame % 10 == 0:
        print(f"Rendering frame {frame}/{num_frames}...")
        
    return line,

# ---------------------------------------------------------
# 5. Compile and Export
# ---------------------------------------------------------
print("Starting render process...")

ani = animation.FuncAnimation(fig, update, frames=num_frames, blit=True)

# Save at the requested 24 fps
ani.save('cygnus_transit_smooth_10savg_24fps.mp4', writer='ffmpeg', fps=24)

print("Render complete! Saved as cygnus_transit_smooth_24fps.mp4")
