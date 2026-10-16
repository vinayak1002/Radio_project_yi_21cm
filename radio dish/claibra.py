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
    'duration': 600,
    'loc': 'Bengaluru',
    'ra_dec': '',
    'az_alt': '180, 48'
}

# m=50 forces a higher-order polynomial subtraction to flatten the LNA curve
virgo.plot(
    obs_parameters=obs_parameters, 
    n=20, 
    m=50, 
    f_rest=1420405751, 
    obs_file='milky_way_data_10mins.dat', 
    plot_file='sagittarius_A_calibrated.png'
)
