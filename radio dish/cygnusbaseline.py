import numpy as np
import matplotlib.pyplot as plt

# 1. Physical Parameters
fs = 2400000
nfft = 2048
f_rest = 1420.405751

# 2. Define your files
# ONLY include your clean cold sky files here. DO NOT include files with massive power drops.
cold_files = [
    'day2_10min_cold.dat', 
    'day2_10min_cold2.dat'
    # Add any other clean cold .dat files here
]
target_file = 'day2_30min_cygnus.dat' # Your target ON observation

# 3. Stack the Cold Sky Data (Combine them into a Master Baseline)
stacked_cold_data = []
for file in cold_files:
    # Load and reshape each clean file
    data = np.fromfile(file, dtype=np.float32).reshape(-1, nfft)
    stacked_cold_data.append(data)

# Vertically stack all arrays into one massive time-frequency matrix and calculate the mean
combined_cold_matrix = np.vstack(stacked_cold_data)
master_off_mean = np.mean(combined_cold_matrix, axis=0)

# 4. Apply Polynomial Mask to the Master OFF to remove stray hydrogen
x_axis = np.linspace(-fs/2, fs/2, nfft) / 1e6 + 1420.405

# Mask out the center frequencies where stray hydrogen lives
signal_mask = (x_axis > 1420.2) & (x_axis < 1420.6)
baseline_mask = ~signal_mask 

# Fit a polynomial (degree 4) to the pure noise edges of the Master OFF
poly_coeffs = np.polyfit(x_axis[baseline_mask], master_off_mean[baseline_mask], 4)
synthetic_master_off = np.polyval(poly_coeffs, x_axis)

# 5. Load and process the Target ON data
on_data = np.fromfile(target_file, dtype=np.float32).reshape(-1, nfft)
on_mean = np.mean(on_data, axis=0)

# 6. Final Calibration: (ON - Synthetic Master OFF) / Synthetic Master OFF
calibrated_spectrum = (on_mean - synthetic_master_off) / synthetic_master_off

# 7. Generate the Plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(x_axis, calibrated_spectrum, lw=1.5, color='tab:red')
ax.axvline(f_rest, color='black', linestyle='--', alpha=0.7, label='Rest Frequency (0 km/s)')

# Dynamically set Y-limits with 10% padding
y_min = np.min(calibrated_spectrum)
y_max = np.max(calibrated_spectrum)
padding = (y_max - y_min) * 0.1
ax.set_ylim(y_min - padding, y_max + padding)

ax.set_xlabel('Frequency (MHz)')
ax.set_ylabel('Calibrated Intensity (ON-OFF)/OFF')
ax.set_title('Master Calibrated 21 cm Spectrum (Cygnus)')
ax.grid(True, linestyle='--', alpha=0.6)
ax.legend()

plt.savefig('cygnus_master_calibrated.png', dpi=300)
print("Master Calibration complete. Saved as cygnus_master_calibrated.png")
