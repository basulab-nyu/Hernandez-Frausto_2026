import pandas as pd
import numpy as np
import math

def session_event_related_means(grouped_dfs, relate, events_auc):

    #ambigiously use for any event related data
    """
        auc_means_a: list of mean AUCs for A (per session)
        auc_means_b: list of mean AUCs for B (per session)
        total_events_a: total number of events for A (per session)
        total_events_b: total number of events for B (per session)
    """
    ev_in_bev, duration = events_within_action_window(grouped_dfs, events_auc) 
    means_a = []
    means_b = []
    total_events_a = 0
    total_events_b = 0


    # ar[0] = A, ar[1] = B
    # ev_in_bev[0] = A, ev_in_bev[1] = B
    # Loop through sessions for A and B separately
    for idx, ev_session in enumerate(ev_in_bev):

        # anything that says related has to do with an event datatype ex: AUC, Duration, etc
        related_means = []
        relates = []
        total_events = 0
        for event_window in ev_session:
            if not event_window.empty:
                related = event_window[relate].values


                relates.extend(related.tolist())

                related_means.append(related.mean())
                total_events += len(related)


        # If there are events in this session, take mean of means; else nan

        if related_means:
            session_mean = np.nanmean(related_means)
        else:
            session_mean = np.nan
        
        if idx == 0: # object A related mean
            means_a.append(session_mean)
            total_events_a += total_events
        elif idx == 1: # object B related mean
            means_b.append(session_mean)
            total_events_b += total_events

    return means_a, means_b, relates, total_events_a, total_events_b, duration


def events_within_action_window(grouped_dfs, events_auc): 
    """
    events that occurred between entrance and exit
    """
    ev_in_bev = []
    durations = []

    for i in range(len(grouped_dfs)):  # entrance and exit
        ev_in = []
        dur_in = []

        for j in range(len(grouped_dfs[i])):  
            start = grouped_dfs[i].iloc[j]["timestamps"].iloc[0]
            end = grouped_dfs[i].iloc[j]["timestamps"].iloc[1]

            if math.isnan(start) or math.isnan(end):
                continue  

            current_events_in_range = events_auc[
                (events_auc['time'] >= start) & (events_auc['time'] <= end)
            ]

            if not current_events_in_range.empty:  
                ev_in.append(current_events_in_range.reset_index(drop=True))
                dur_in.append(end - start)  # save duration

        ev_in_bev.append(ev_in)
        durations.append(dur_in)

    return ev_in_bev, durations
    
def extract_action_window(individual_dfs, signal_trace, pre_time, post_time):
    """
    Extract df/f signal around behavior timestamps:
    - pre_time seconds before
    - post_time seconds after
    """
    beh_dfs = []

    # Ensure time column is numeric array for speed
    time_values = signal_trace['time'].values  

    for i in range(len(individual_dfs)): 
        beh_df = []
        for j in range(len(individual_dfs[i])):  
            target = individual_dfs[i].iloc[j]['timestamps']
            if pd.isna(target):
                continue

            # Compute start and end times in seconds
            start_time = max(time_values[0], target - pre_time)
            end_time   = min(time_values[-1], target + post_time)

            # Find indices for start/end times using binary search for efficiency
            start_idx = np.searchsorted(time_values, start_time, side="left")
            end_idx   = np.searchsorted(time_values, end_time, side="right")

            new_df = signal_trace.iloc[start_idx:end_idx]
            beh_df.append(new_df)

        beh_dfs.append(beh_df)

    return beh_dfs

def event_action_window(individual_dfs, events_auc, pre_time, post_time):
    """
    Extracts events from events_auc that fall within a time window around behavior timestamps.

    Args:
        individual_dfs (list of pd.DataFrame): List of DataFrames, each containing 'timestamps' of behavioral events.
        events_auc (pd.DataFrame): DataFrame containing event data with a sorted 'time' column.
        pre_time (float): Seconds before the timestamp to start the window.
        post_time (float): Seconds after the timestamp to end the window.

    Returns:
        list: A nested list of DataFrames. Each inner list corresponds to a DataFrame in
              individual_dfs and contains DataFrames of events inside the window for each timestamp.
    """
    beh_dfs = []
    time_values = events_auc['time'].values

    for i in range(len(individual_dfs)):
        beh_df = []
        for j in range(len(individual_dfs[i])):
            target = individual_dfs[i].iloc[j]['timestamps']
            if pd.isna(target):
                continue

            start_time = max(time_values[0], target - pre_time)
            end_time = min(time_values[-1], target + post_time)

            start_idx = np.searchsorted(time_values, start_time, side="left")
            end_idx = np.searchsorted(time_values, end_time, side="right")

            # Extract peri-event window
            new_df = events_auc.iloc[start_idx:end_idx].copy()

            # Compute relative time centered at the event
            new_df['relative_time'] = new_df['time'] - target

            beh_df.append(new_df)

        beh_dfs.append(beh_df)

    return beh_dfs


import numpy as np
import pandas as pd

def locomotion_epochs(df, location, pre_time=10.0, post_time=10.0):

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

def separate_traces_by_state(beh_dfs, individual_dfs, positional_with_state):
    """
    Separates event-related traces into 'locomotion' and 'stationary' based on the
    animal's state at the time of the event.

    Args:
        beh_dfs (list of lists of pd.DataFrame): Nested list of signal traces around events.
            (e.g., beh_dfs[0] is a list of traces for entrance A events).
        individual_dfs (list of pd.DataFrame): List of DataFrames with event 'timestamps'.
        positional_with_state (pd.DataFrame): DataFrame containing 'time' and 'state'
            ('locomotion' or 'stationary') columns, sorted by time.

    Returns:
        tuple: A tuple containing two lists (locomotion_traces, stationary_traces).
               Each is a nested list structured like beh_dfs.
    """
    locomotion_traces = [[], [], [], []]  # For en_a, en_b, ex_a, ex_b
    stationary_traces = [[], [], [], []]  # For en_a, en_b, ex_a, ex_b

    # Prepare positional data for efficient lookup
    pos_df = positional_with_state.sort_values('time').copy()

    # Iterate through each behavior type (en_a, en_b, ex_a, ex_b)
    for i in range(len(individual_dfs)):
        timestamps = individual_dfs[i]['timestamps'].dropna().tolist()
        traces = beh_dfs[i]

        # Ensure we have a 1-to-1 mapping of timestamps to traces
        if len(timestamps) != len(traces):
            print(f"Warning: Mismatch between number of timestamps ({len(timestamps)}) and traces ({len(traces)}) for behavior index {i}. Skipping.")
            continue

        for timestamp, trace in zip(timestamps, traces):
            # Find the closest state in time to the event timestamp
            # Find the index of the time in pos_df closest to the event timestamp
            closest_idx = (pos_df['time'] - timestamp).abs().idxmin()
            closest_state_row = pos_df.loc[closest_idx]
            state = closest_state_row['state']

            if state == 'locomotion':
                locomotion_traces[i].append(trace)
            else:  # 'stationary'
                stationary_traces[i].append(trace)

    return locomotion_traces, stationary_traces