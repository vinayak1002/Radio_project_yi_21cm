import numpy as np
import matplotlib.pyplot as plt

# 1. Physical Parameters
fs = 2400000
nfft = 2048
f_rest = 1420.405751

# 2. Load the Day 2 files (Matching hardware, temperature, and standing wave)
# Make sure the filenames match your actual .dat files
on_data_full = np.fromfile('day2_30min_cygnus.dat', dtype=np.float32).reshape(-1, nfft)
off_data_full = np.fromfile('day2_30min_cold.dat', dtype=np.float32).reshape(-1, nfft)

# 3. The Time-Slice Fix
# The power drop happened at roughly 800 seconds in the cold file.
# We slice the first 600 rows (10 minutes) of BOTH files to keep integration time equal.
on_data_clean = on_data_full[:600]
off_data_clean = off_data_full[:600]

# 4. Compute the time-averaged spectra using ONLY the clean 600 seconds
on_mean = np.mean(on_data_clean, axis=0)
off_mean = np.mean(off_data_clean, axis=0)

# 5. Apply the standard empirical calibration formula
calibrated_spectrum = (on_mean - off_mean) / off_mean

# 6. Generate the Plot
fig, ax = plt.subplots(figsize=(10, 6))
x_axis = np.linspace(-fs/2, fs/2, nfft) / 1e6 + 1420.405

ax.plot(x_axis, calibrated_spectrum, lw=1.5, color='tab:red')
ax.axvline(f_rest, color='black', linestyle='--', alpha=0.7, label='Rest Frequency (0 km/s)')

# Dynamically set Y-limits with 10% padding
y_min = np.min(calibrated_spectrum)
y_max = np.max(calibrated_spectrum)
padding = (y_max - y_min) * 0.1
ax.set_ylim(y_min - padding, y_max + padding)

ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Calibrated Intensity (ON-OFF)/OFF')
ax.set_title('Cygnus Transit - Sliced Day 2 Calibration')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

plt.savefig('cygnus_sliced_calibration.png', dpi=300)
print("Sliced Calibration complete. Saved as cygnus_sliced_calibration.png")
