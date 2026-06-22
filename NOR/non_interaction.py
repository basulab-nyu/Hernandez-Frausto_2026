import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
import seaborn as sns
from scipy.stats import sem
import random

def extract_non_interaction_epochs(individual_dfs, signal_trace, epoch_duration=20, gap_after_exit=5):
    """
    Extracts continuous epochs of a specified duration from periods of non-interaction.

    """
    df_en_a, df_en_b, df_ex_a, df_ex_b = individual_dfs

    # Combine all interaction timestamps into a single series and sort them
    all_interactions = pd.concat([
        df_en_a['timestamps'],
        df_en_b['timestamps'],
        df_ex_a['timestamps'],
        df_ex_b['timestamps']
    ]).dropna().sort_values().reset_index(drop=True)

    # print(f"All interactions: {all_interactions}")

    
    # Combine all exit timestamps
    all_exits = pd.concat([df_ex_a['timestamps'], df_ex_b['timestamps']]).dropna().sort_values()

    non_interaction_epochs = []
    signal_time = signal_trace['time'].values

    previous_epoch = None  # initialize once before loop

    for exit_time in all_exits:
        # Define the start of the non-interaction window
        window_start = exit_time + gap_after_exit

        # --- Use np.searchsorted to find where window_start fits ---
        idx = np.searchsorted(all_interactions.values, window_start)
        if idx < len(all_interactions):
            window_end = all_interactions.iloc[idx]
        else:
            window_end = signal_time[-1]

        # --- Generate 20-second epochs within this non-interaction window ---
        current_time = window_start
        while current_time + epoch_duration <= window_end:
            epoch_end_time = current_time + epoch_duration

            # Extract the signal for this epoch
            epoch_df = signal_trace[
                (signal_trace['time'] >= current_time) & 
                (signal_trace['time'] < epoch_end_time)
            ]

            if not epoch_df.empty:
                # Only add if this epoch doesn’t overlap or duplicate the last one
                if (
                    previous_epoch is None or 
                    epoch_df['time'].iloc[0] > previous_epoch['time'].iloc[-1]
                ):
                    print(f"Here's the extracted epoch: {epoch_df}\n")
                    non_interaction_epochs.append(epoch_df)
                    previous_epoch = epoch_df

            current_time += epoch_duration
    print(f"hello {non_interaction_epochs}")

    print("Finished extracting non-interaction epochs.")


    return non_interaction_epochs
    
def randomizer(comparsion_epochs, trace, mouse, zscore, group, condition, epoch_name):
    """
    Pit a random non-interaction time stamp with an averaged trace of a mouse
    """ 
    # --- Compute averaged trace and SEM ---
    trace_mean = np.mean((np.array(trace[group][condition]['A']) + np.array(trace[group][condition]['B'])) / 2, axis=0)
    trace_sem = sem((np.array(trace[group][condition]['A']) + np.array(trace[group][condition]['B'])) / 2, axis=0)

    # --- Pick a random non-interaction epoch ---
    randomized_epoch = random.choice(comparsion_epochs)
    randomized_trace = randomized_epoch['df/f'].values

    # --- Build consistent time axis for both traces (epoch_duration seconds) ---
    epoch_duration = 20.0
    samples_trace = len(trace_mean)
    samples_random = len(randomized_trace)

    # Create time axes spanning 0 .. epoch_duration (same scale for both traces)
    time_axis = np.linspace(0, epoch_duration, samples_trace, endpoint=False)
    randomized_time = np.linspace(0, epoch_duration, samples_random, endpoint=False)

    fig, axs = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    y_label = 'z-score' if zscore else 'df/f'

    # Plot averaged interaction trace
    axs[0].plot(time_axis, trace_mean, label='Avg Trace', color='blue')
    axs[0].fill_between(time_axis, trace_mean - trace_sem, trace_mean + trace_sem, color='blue', alpha=0.3)
    axs[0].set_ylabel(y_label)
    axs[0].set_title(f'{group} {condition} - Averaged Interaction {mouse}')

    # Plot randomized non-interaction trace (aligned to same 0..epoch_duration axis)
    axs[1].plot(randomized_time, randomized_trace, color='green', label=f'Random {epoch_name}')
    axs[1].set_xlabel('Time (s)')
    axs[1].set_ylabel(y_label)
    axs[1].set_title(f'Random {epoch_name} Epoch {mouse}')

    # Format axes and enforce 0..epoch_duration limits
    for ax in axs:
        ax.set_xlim(0, epoch_duration)
        ax.spines[['top', 'right']].set_visible(False)
        ax.legend()

    plt.tight_layout()


        # --- Combined figure (both traces on one graph) ---
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    ax2.plot(time_axis, trace_mean, label='Averaged Interaction', color='blue', linewidth=1.5)
    ax2.fill_between(time_axis, trace_mean - trace_sem, trace_mean + trace_sem, color='blue', alpha=0.2)
    ax2.plot(randomized_time, randomized_trace, label='Random Non-Interaction', color='green', alpha=0.8, linewidth=1.5)

    ax2.set_xlim(0, epoch_duration)
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel(y_label)
    ax2.set_title(f'{group} {condition} | Averaged vs Randomized of {epoch_name} ({mouse})')

    ax2.spines[['top', 'right']].set_visible(False)
    ax2.legend()
    plt.tight_layout()

def corner_detection(individual_dfs, signal_trace, position_df, epoch_duration=20):
    """"
    similar to the non-interaction function but since we have to compare the frame of the position in addition to whether or not its colluding with entrance / exit 
    there is a new merge dataframe that combines the position and signal trace based on time.

    """

    df_en_a, df_en_b, df_ex_a, df_ex_b = individual_dfs
    corner_size = 50
    max_x, max_y = 500, 400
    corners = [
            ((0, corner_size), (0, corner_size)),
            ((max_x - corner_size, max_x), (0, corner_size)),
            ((0, corner_size), (max_y - corner_size, max_y)),
            ((max_x - corner_size, max_x), (max_y - corner_size, max_y))
        ]
    # Combine all interaction timestamps into a single series and sort them
    all_interactions = pd.concat([
        df_en_a['timestamps'],
        df_en_b['timestamps'],
        df_ex_a['timestamps'],
        df_ex_b['timestamps']
    ]).dropna().sort_values().reset_index(drop=True)


    for i, ((x_min, x_max), (y_min, y_max)) in enumerate(corners):
        corner_label = f'corner_{i+1}'
        position_df[corner_label] = (
            (position_df['x'] >= x_min) & (position_df['x'] <= x_max) &
            (position_df['y'] >= y_min) & (position_df['y'] <= y_max)
        ).astype(int)


    # Merge signal_trace with position_df to align timestamps
    merged_df = pd.merge_asof(
        signal_trace.sort_values('time'),
        position_df.sort_values('time'),
        on='time'
    )

    corner_epochs = []
    signal_time = merged_df['time'].values
    previous_epoch = None  # initialize once before loop

    for cornerlabel in [f'corner_{i+1}' for i in range(len(corners))]:
        entry_points = merged_df[(merged_df[cornerlabel].diff() == 1)]['time'].values

        for entry_time in entry_points:
            # Define the start of the corner visit window
            window_start = entry_time
            window_end = window_start + epoch_duration

            if window_end > signal_time[-1]:
                continue

            overlap = (all_interactions.between(window_start, window_end)).any()
            if overlap:
                continue

            epoch_df = signal_trace[
                (merged_df['time'] >= window_start) &
                (merged_df['time'] < window_end) &
                (merged_df[cornerlabel] == 1)
            ]



            if not epoch_df.empty:
                # Only add if this epoch doesn’t overlap or duplicate the last one
                if (
                    previous_epoch is None or 
                    epoch_df['time'].iloc[0] > previous_epoch['time'].iloc[-1]
                ):
                    corner_epochs.append(epoch_df)
                    previous_epoch = epoch_df
                    print(f"Corner epoch ({cornerlabel}): {epoch_df}\n")

    return corner_epochs



def locomotion_epochs(individual_dfs, signal_trace, location, pre_time=10.0, post_time=10.0, gap_after_exit=5):

    """
    Extract ±time windows from df around transitions from stationary → locomotion in location.

    Args:
        df (pd.DataFrame): DataFrame containing at least a 'time' column (e.g. fluorescence data).
        location (pd.DataFrame): DataFrame with 'time' and 'state' columns.
        pre_time (float): Seconds before the transition to include.
        post_time (float): Seconds after the transition to include.

    Returns:
        list of pd.DataFrame: Each DataFrame represents one locomotion epoch.
    """
    df_en_a, df_en_b, df_ex_a, df_ex_b = individual_dfs

    all_interactions = pd.concat([
        df_en_a['timestamps'],
        df_en_b['timestamps'],
        df_ex_a['timestamps'],
        df_ex_b['timestamps']
    ]).dropna().sort_values().reset_index(drop=True)


    # Sort both by time to ensure consistency
    df = signal_trace.sort_values("time").reset_index(drop=True)
    location = location.sort_values("time").reset_index(drop=True)

    # Find indices of stationary → locomotion transitions
    transitions = location.index[
        (location["state"].shift(1) == "stationary") & (location["state"] == "locomotion")
    ]

    # If no transitions are found
    if len(transitions) == 0:
        print("No locomotion transitions found.")
        return []

    time = df["time"].values
    epochs = []

    for idx in transitions:
        target_time = location.loc[idx, "time"]

        # Define time window
        start_time = max(time[0], target_time - pre_time)
        end_time = min(time[-1], target_time + post_time)

        # Find corresponding indices in df
        start_idx = np.searchsorted(time, start_time, side="left")
        end_idx = np.searchsorted(time, end_time, side="right")

        # Extract and store epoch
        epoch_df = df.iloc[start_idx:end_idx].copy()
        epoch_df["transition_time"] = target_time
        epoch_df["epoch_id"] = len(epochs) + 1
        epochs.append(epoch_df)

    return epochs

def stationary_epochs(df, location, pre_time=10.0, post_time=10.0):
    """
    Extract ±time windows from df around transitions from locomotion → stationary in location.
    """

    # Sort both by time
    df = df.sort_values("time").reset_index(drop=True)
    location = location.sort_values("time").reset_index(drop=True)

    # Find locomotion → stationary transitions
    transitions = location.index[
        (location["state"].shift(1) == "locomotion") & (location["state"] == "stationary")
    ]

    if len(transitions) == 0:
        print("No stationary transitions found.")
        return []

    time = df["time"].values
    epochs = []

    for idx in transitions:
        target_time = location.loc[idx, "time"]

        # Define window
        start_time = max(time[0], target_time - pre_time)
        end_time = min(time[-1], target_time + post_time)

        start_idx = np.searchsorted(time, start_time, side="left")
        end_idx = np.searchsorted(time, end_time, side="right")

        epoch_df = df.iloc[start_idx:end_idx].copy()
        epoch_df["transition_time"] = target_time
        epoch_df["epoch_id"] = len(epochs) + 1
        epochs.append(epoch_df)

    return epochs



def locomotion_epochs(df, location, pre_time=10.0, post_time=10.0):

    """
    Extract time windows from df around transitions from stationary → locomotion in location.

    Args:
        df (pd.DataFrame): DataFrame containing at least a 'time' column (e.g. fluorescence data).
        location (pd.DataFrame): DataFrame with 'time' and 'state' columns.
        pre_time (float): Seconds before the transition to include.
        post_time (float): Seconds after the transition to include.

    Returns:
        list of pd.DataFrame: Each DataFrame represents one locomotion epoch.
    """

    # Sort both by time to ensure consistency
    df = df.sort_values("time").reset_index(drop=True)
    location = location.sort_values("time").reset_index(drop=True)

    # Find indices of stationary → locomotion transitions
    transitions = location.index[
        (location["state"].shift(1) == "stationary") & (location["state"] == "locomotion")
    ]

    # If no transitions are found
    if len(transitions) == 0:
        print("No locomotion transitions found.")
        return []

    time = df["time"].values
    epochs = []

    for idx in transitions:
        target_time = location.loc[idx, "time"]

        # Define time window
        start_time = max(time[0], target_time - pre_time)
        end_time = min(time[-1], target_time + post_time)

        # Find corresponding indices in df
        start_idx = np.searchsorted(time, start_time, side="left")
        end_idx = np.searchsorted(time, end_time, side="right")

        # Extract and store epoch
        epoch_df = df.iloc[start_idx:end_idx].copy()
        epoch_df["transition_time"] = target_time
        epoch_df["epoch_id"] = len(epochs) + 1
        epochs.append(epoch_df)

    return epochs

def stationary_epochs(df, location, pre_time=10.0, post_time=10.0):
    """
    Extract ±time windows from df around transitions from locomotion → stationary in location.
    """

    # Sort both by time
    df = df.sort_values("time").reset_index(drop=True)
    location = location.sort_values("time").reset_index(drop=True)

    # Find locomotion → stationary transitions
    transitions = location.index[
        (location["state"].shift(1) == "locomotion") & (location["state"] == "stationary")
    ]

    if len(transitions) == 0:
        print("No stationary transitions found.")
        return []

    time = df["time"].values
    epochs = []

    for idx in transitions:
        target_time = location.loc[idx, "time"]

        # Define window
        start_time = max(time[0], target_time - pre_time)
        end_time = min(time[-1], target_time + post_time)

        start_idx = np.searchsorted(time, start_time, side="left")
        end_idx = np.searchsorted(time, end_time, side="right")

        epoch_df = df.iloc[start_idx:end_idx].copy()
        epoch_df["transition_time"] = target_time
        epoch_df["epoch_id"] = len(epochs) + 1
        epochs.append(epoch_df)

    return epochs



def baseline(traces_a, traces_b, comparison_epochs, mouse, zscore, group, condition, epoch_name, epoch_duration=20.0):
    """
    Compares an averaged primary trace against an averaged baseline/comparison trace.

    Args:
        traces_a (list of np.array): List of traces for mouse A.
        traces_b (list of np.array): List of traces for mouse B.
        comparison_epochs (list of pd.DataFrame): List of DataFrames, each representing a comparison epoch.
        mouse (str): Identifier for the mouse/session.
        zscore (bool): Whether the traces are z-scored (for y-axis label).
        group (str): Experimental group name.
        condition (str): Experimental condition name.
        epoch_name (str): Name for the comparison epochs (e.g., 'Non-Interaction').
        epoch_duration (float): The duration of the epochs in seconds for the time axis.
    """
    if not traces_a and not traces_b:
        print(f"No primary traces provided for {group} {condition} {mouse}. Skipping plot.")
        return

    if not comparison_epochs:
        print(f"No comparison epochs provided for {epoch_name}. Skipping plot.")
        return

    # --- Compute averaged primary trace and SEM ---
    all_traces = np.array(traces_a + traces_b)
    primary_trace_mean = np.mean(all_traces, axis=0)
    primary_trace_sem = sem(all_traces, axis=0)

    # --- Compute averaged comparison trace and SEM ---
    # Ensure all comparison traces are interpolated to the same length as the primary trace
    num_samples = len(primary_trace_mean)
    resampled_comparison_traces = []
    for epoch_df in comparison_epochs:
        trace_vals = epoch_df['df/f'].values
        # Create original and target time axes for interpolation
        original_time = np.linspace(0, epoch_duration, len(trace_vals))
        target_time = np.linspace(0, epoch_duration, num_samples)
        resampled_trace = np.interp(target_time, original_time, trace_vals)
        resampled_comparison_traces.append(resampled_trace)

    comparison_mean = np.mean(np.array(resampled_comparison_traces), axis=0)
    comparison_sem = sem(np.array(resampled_comparison_traces), axis=0)

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(10, 5))
    y_label = 'z-score' if zscore else 'df/f'
    time_axis = np.linspace(0, epoch_duration, num_samples, endpoint=False)

    # Plot averaged primary trace
    ax.plot(time_axis, primary_trace_mean, label='Averaged Interaction', color='blue', linewidth=1.5)
    ax.fill_between(time_axis, primary_trace_mean - primary_trace_sem, primary_trace_mean + primary_trace_sem, color='blue', alpha=0.2)

    # Plot averaged comparison trace
    ax.plot(time_axis, comparison_mean, label=f'Averaged {epoch_name}', color='gray', linestyle='--', linewidth=1.5)
    ax.fill_between(time_axis, comparison_mean - comparison_sem, comparison_mean + comparison_sem, color='gray', alpha=0.2)

    ax.set_xlim(0, epoch_duration)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel(y_label)
    ax.set_title(f'{group} {condition} | Averaged Interaction vs. Averaged {epoch_name} ({mouse})')
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend()
    plt.tight_layout()
    plt.show()

def z_score_normalization(non_interaction_epochs, corner_epochs, stationary_epochs, locomotion_epochs, epoch_duration=20.0, title_suffix=""):
    """
    Calculates the mean and standard deviation from non-interaction epochs and uses
    these statistics to Z-score normalize the mean traces of other behavioral epochs.

    Args:
        non_interaction_epochs (list of pd.DataFrame): Baseline epochs.
        corner_epochs (list of pd.DataFrame): Corner interaction epochs.
        stationary_epochs (list of pd.DataFrame): Stationary epochs.
        locomotion_epochs (list of pd.DataFrame): Locomotion epochs.
        epoch_duration (float): Duration of epochs in seconds for the time axis.
        title_suffix (str): Optional suffix to add to the plot title.
    """
    if not non_interaction_epochs:
        print("No non-interaction epochs for baseline. Skipping Z-score normalization.")
        return

    # 1. Calculate mu_random and sigma_random from ALL non-interaction data points
    all_non_interaction_traces = np.concatenate([epoch['df/f'].values for epoch in non_interaction_epochs])
    mu_random = np.mean(all_non_interaction_traces)
    sigma_random = np.std(all_non_interaction_traces)

    if sigma_random == 0:
        print("Standard deviation of non-interaction epochs is zero. Cannot perform Z-score normalization.")
        return

    epochs_to_process = {
        "Non-Interaction": non_interaction_epochs,
        "Corner": corner_epochs,
        "Stationary": stationary_epochs,
        "Locomotion": locomotion_epochs
    }

    # Determine a common length for interpolation
    # Using a high-resolution length based on a typical trace
    sample_lengths = [len(epoch['df/f']) for group in epochs_to_process.values() if group for epoch in group]
    if not sample_lengths:
        print("No epochs to process.")
        return
    
    # Let's standardize to a common length, e.g., 500 points for a 20s epoch
    num_samples = 500 
    time_axis = np.linspace(0, epoch_duration, num_samples)
    
    transformed_traces = {}

    for name, epochs in epochs_to_process.items():
        if not epochs:
            print(f"No epochs for {name}. Skipping.")
            continue

        # Resample each trace to the common length `num_samples` before averaging
        resampled_traces = []
        for epoch_df in epochs:
            trace_vals = epoch_df['df/f'].values
            original_time = np.linspace(0, epoch_duration, len(trace_vals))
            resampled_trace = np.interp(time_axis, original_time, trace_vals)
            resampled_traces.append(resampled_trace)
        
        # Calculate the mean trace from the resampled traces
        mean_trace = np.mean(resampled_traces, axis=0)
        
        # 2. Apply Z-score transformation
        z_scored_trace = (mean_trace - mu_random) / sigma_random
        transformed_traces[name] = z_scored_trace

    # 3. Plotting
    plt.figure(figsize=(12, 7))
    for name, z_scored_trace in transformed_traces.items():
        plt.plot(time_axis, z_scored_trace, label=name)

    plt.axhline(0, color='k', linestyle='--', linewidth=1) # The new baseline
    plt.title(f"Z-Score Normalized Epochs (Baseline: Non-Interaction) {title_suffix.strip()}")
    plt.xlabel("Time (s)")
    plt.ylabel("Z-score (Deviations from Non-Interaction Mean)")
    plt.legend()
    plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()