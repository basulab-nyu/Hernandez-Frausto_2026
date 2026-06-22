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
    ev_in_bev = events_within_action_window(grouped_dfs, events_auc) 
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

    return means_a, means_b, relates, total_events_a, total_events_b

def events_within_action_window(grouped_dfs, events_auc): 
    """
    events that occured between entrance and exit

    ev_in_bev an array of A and B with all the events and their auc
    """
    ev_in_bev = []
    for i in range(len(grouped_dfs)): # entrance and exit
        ev_in = []
        for j in range(len(grouped_dfs[i])): # going to iterate through each of action
            
            start = grouped_dfs[i].iloc[j]["timestamps"].iloc[0] # since we're just using the interaction window we can just extract them from the array
            end = grouped_dfs[i].iloc[j]["timestamps"].iloc[1]
            if math.isnan(start) or math.isnan(end):
                continue  # Skip this iteration if timestamps are invalid

            current_events_in_range = events_auc[
                (events_auc['time'] >= start) & (events_auc['time'] <= end) # if the time at which an event occured is within the event window we're gonna keep it in mind
            ]

            if not current_events_in_range.empty: # becaue its not empty we're going to add the event to an array
             #   print(f"Found {len(current_events_in_range)} events in range {start} to {end}")
                ev_in.append(current_events_in_range.reset_index(drop=True))

        ev_in_bev.append(ev_in)
        

    return ev_in_bev  # Assuming the function should return something



def compute_session_auc_means(grouped_dfs, signal_trace, events_auc):
    """
        auc_means_a: list of mean AUCs for A (per session)
        auc_means_b: list of mean AUCs for B (per session)
        total_events_a: total number of events for A (per session)
        total_events_b: total number of events for B (per session)
    """
    ev_in_bev = events_within_action_window(grouped_dfs, events_auc)
    auc_means_a = []
    auc_means_b = []
    total_events_a = 0
    total_events_b = 0

    # ar[0] = A, ar[1] = B
    # ev_in_bev[0] = A, ev_in_bev[1] = B
    # Loop through sessions for A and B separately
    for idx, ev_session in enumerate(ev_in_bev):
        auc_means = []
        total_events = 0
        for event_window in ev_session:
            if not event_window.empty:
                aucs = event_window["auc"]
                auc_means.append(aucs.mean())
                total_events += len(aucs)
        # If there are events in this session, take mean of means; else nan
        if auc_means:
            session_mean = np.nanmean(auc_means)
        else:
            session_mean = np.nan
        if idx == 0:
            auc_means_a.append(session_mean)
            total_events_a += total_events
        elif idx == 1:
            auc_means_b.append(session_mean)
            total_events_b += total_events

    return auc_means_a, auc_means_b, total_events_a, total_events_b

def extract_action_window(individual_dfs, signal_trace):
    """
        the df/f 10 seconds before and 40 seconds after the action
        
        beh_dfs, an array of entrance, exit of both A and B for between 10 seconds before and 40 seconds after an action is done
    """
        
    # Hardcoded based on ~60.24Hz sampling rate to match utils.py assumptions
    # 10 seconds pre-event, 40 seconds post-event
    PRE_FRAMES = 603
    POST_FRAMES = 2410

  
    beh_dfs = []
    for i in range(len(individual_dfs)):
        beh_df = []
        for j in range(len(individual_dfs[i])):
            target = individual_dfs[i].iloc[j]['timestamps']
            if pd.isna(target):
                continue
            closest_idx = (signal_trace['time'] - target).abs().idxmin()
            start_idx = closest_idx - PRE_FRAMES
            end_idx = closest_idx + POST_FRAMES
            
            # Calculate valid slice indices
            valid_start = max(0, start_idx)
            valid_end = min(len(signal_trace), end_idx)
            
            new_df = signal_trace.iloc[valid_start:valid_end].copy()
            
            # Pad with NaNs if the window goes out of bounds to maintain alignment
            pad_before = valid_start - start_idx
            pad_after = end_idx - valid_end
            
            if pad_before > 0:
                padding = pd.DataFrame(np.nan, index=range(pad_before), columns=new_df.columns)
                new_df = pd.concat([padding, new_df], ignore_index=True)
            
            if pad_after > 0:
                padding = pd.DataFrame(np.nan, index=range(pad_after), columns=new_df.columns)
                new_df = pd.concat([new_df, padding], ignore_index=True)

            beh_df.append(new_df)
        beh_dfs.append(beh_df) # 10 seconds before and 40 seconds after an action

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

    