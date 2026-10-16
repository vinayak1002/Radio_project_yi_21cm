import numpy as np
import matplotlib.pyplot as plt

# 1. Physical Parameters
fs = 2400000
nfft = 2048
f_rest = 1420.405751

# 2. File definitions
on_file = 'day3_15min_scrutum_v2.dat'  # Your Sagittarius A* observation
off_file = 'day3_15min_scrutum_cold.dat' # Your 10-minute cold sky observation

# 3. Load the binary data (float32) and reshape into time-frequency matrices
on_data = np.fromfile(on_file, dtype=np.float32).reshape(-1, nfft)
off_data = np.fromfile(off_file, dtype=np.float32).reshape(-1, nfft)
# Slice from row 60 to the end, skipping the first 1 minute of data


# Calculate the mean using only the clean data
off_mean = np.mean(off_data, axis=0)
# 4. Compute the time-averaged power spectrum for both scans
on_mean = np.mean(on_data, axis=0)

# 5. Apply the baseline quotient formula
calibrated_spectrum = (on_mean - off_mean) / off_mean

# 6. Generate the Plot
fig, ax = plt.subplots(figsize=(10, 6))
x_axis = np.linspace(-fs/2, fs/2, nfft) / 1e6 + 1420.405

ax.plot(x_axis, calibrated_spectrum, lw=1.5, color='tab:red')

# Add a vertical marker for the rest frequency
ax.axvline(f_rest, color='black', linestyle='--', alpha=0.7, label='Rest Frequency (0 km/s)')

ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Calibrated Intensity (ON-OFF)/OFF')
ax.set_title('Baseline-Subtracted 21 cm Hydrogen Spectrum')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

plt.savefig('calibrated_scrutum_day3_v2.png', dpi=300)
print("Calibration complete. Saved as calibrated_hydrogen_withoutdip.png")
