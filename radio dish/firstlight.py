import virgo
import time
# Define the observation parameters
obs_parameters = {
    'dev_args': 'rtl=0',
    'rf_gain': 40,
    'if_gain': 20,
    'bb_gain': 20,
    'frequency': 1420405000,
    'bandwidth': 2400000,
    'channels': 2048,
    't_sample': 1,
    'duration': 900,
    'loc': 'Bengaluru',
    'ra_dec': '',
    'az_alt': ''  # You can leave this as an empty string '' or update it to your actual dish tilt
}
time.sleep(10)
# Run the observation

print("observation will start in 10sec")
virgo.observe(obs_parameters=obs_parameters, obs_file='day3_15min_scrutum_cold.dat')
