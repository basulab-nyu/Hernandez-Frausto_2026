import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter1d
import csv
import matplotlib.pyplot as plt
# action determines whether or not the figures will be compiling entrance or exit
# if action is true then entrance
def process(beh_dfs, action, value):
    
    #from the beh_dfs function we're then creating a dataframe that has all the aligned events within one session and removing their timestamps
    if action:

        
        traces_A = pd.DataFrame([df[value].reset_index(drop=True) for df in beh_dfs[0]]).T
        traces_B = pd.DataFrame([df[value].reset_index(drop=True) for df in beh_dfs[1]]).T



    else:

        traces_A = pd.DataFrame([df[value].reset_index(drop=True) for df in beh_dfs[2]]).T
        traces_B = pd.DataFrame([df[value].reset_index(drop=True) for df in beh_dfs[3]]).T
        
    return traces_A, traces_B

def combined_process(beh_dfs, action):
    """
    Combines peri-event dataframes for all events, keeping all parameter columns.
    """
    all_event_properties = ['relative_time', 'auc', 'auc_rate', 'duration', 'width', 'amplitude']

    if action: 
        combined_df = pd.concat(
        [df[all_event_properties] for group in [beh_dfs[0], beh_dfs[1]] for df in group if df is not None],
        ignore_index=True)

    else:
        combined_df = pd.concat(
        [df[all_event_properties] for group in [beh_dfs[2], beh_dfs[3]] for df in group if df is not None],
        ignore_index=True)
    
    return combined_df



def mouse_speed(positional, window_size=1.0, sigma=2):
    """
    Calculates speed from position data over a rolling time window.
    
    For each point in time 't', it looks back to 't - window_size' to
    calculate displacement and speed. This provides a smoother and more
    stable speed estimate than instantaneous frame-to-frame calculation.
    
    Args:
        positional (pd.DataFrame): DataFrame with position data. Must have columns
                                   'time', 'x', and 'y', and be sorted by time.
        session (dict): The session dictionary, used here to create a unique
                        filename for the output CSV.
        window_size (float): The time window in seconds to look back for
                             calculating speed (e.g., 1.0s).
        sigma (int): Sigma for optional Gaussian smoothing of the speed data.
                     Set to 0 or None to disable.
    
    Returns:
        pd.DataFrame: The input DataFrame with a new 'speed' column.
    """
    if not positional['time'].is_monotonic_increasing:
        positional = positional.sort_values(by='time').reset_index(drop=True)
    
    # Create a dataframe shifted in time by window_size
    df_past = positional[['time', 'x', 'y']].copy()
    df_past.rename(columns={
        'time': 'time_past',
        'x': 'x_past',
        'y': 'y_past'
    }, inplace=True)
    df_past['time_target'] = df_past['time_past'] + window_size
    
    # Merge the original df with the time-shifted one.
    # For each row in df, this finds the row in df_past where 'time_past'
    # is closest to 'time' - window_size.
    merged_df = pd.merge_asof(
        positional, df_past, left_on='time', right_on='time_target', direction='nearest'
    )
    
    # Calculate displacement and time difference
    dx = merged_df['x'] - merged_df['x_past']
    dy = merged_df['y'] - merged_df['y_past']
    dt = merged_df['time'] - merged_df['time_past']
    
    # Calculate speed, avoiding division by zero
    speed = np.sqrt(dx**2 + dy**2) / dt.replace(0, np.nan)
    
    if sigma:
        speed = gaussian_filter1d(speed.fillna(0), sigma=sigma)
    
    positional['speed'] = speed

    threshold = positional["speed"].mean() + 1 * positional["speed"].std()
    positional['state'] = np.where(positional['speed'] > threshold, 'locomotion', 'stationary')

    positional.to_csv("/Users/tenzinsamchok/Downloads/hello.csv", index=False)
    
    plt.hist(positional["speed"], bins=30, edgecolor='black')
    
    # Add threshold line
    plt.axvline(threshold, color='red', linestyle='--', label=f'Threshold = {threshold} m/s')

    plt.xlabel("Speed (m/s)")
    plt.ylabel("Frequency")
    plt.title("Speed Distribution with Threshold Cutoff")
    plt.legend()




    return positional


# z score
def get_zscore_traces(
    
        traces_a,
        traces_b,
        signal
):
    mean_val = signal.mean().values[0]

    std_val = signal.std().values[0]

    traces_a = (traces_a - mean_val) / std_val 
    traces_b = (traces_b - mean_val) / std_val

    return traces_a, traces_b
