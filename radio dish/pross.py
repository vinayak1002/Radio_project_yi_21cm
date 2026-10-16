import virgo

obs_parameters = {
    'dev_args': 'rtl=0',
    'rf_gain': 40,
    'if_gain': 20,
    'bb_gain': 20,
    'frequency': 1420405000,
    'bandwidth': 2400000,
    'channels': 2048,
    't_sample': 1,
    'duration': 60,
    'loc': 'Bengaluru',
    'ra_dec': '',
    'az_alt': ''
}

# This runs the FFT, calibrates the baseline, and generates the graph
virgo.plot(obs_parameters=obs_parameters, n=20, m=35, f_rest=1420405751, obs_file='day3_15min_scrutum_cold.dat', plot_file='day3_15min_scrutum_cold.png')
