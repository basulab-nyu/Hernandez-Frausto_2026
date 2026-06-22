import pandas as pd
import numpy as np
from session_dict import session_dict # unused
import matplotlib.pyplot as plt
from plotting import stationary_locomotion
from preprocessing import mouse_speed
from event_related import event_action_window , session_event_related_means, extract_action_window, locomotion_epochs, stationary_epochs
from non_interaction import extract_non_interaction_epochs, corner_detection
import matplotlib.patches as patches
from scipy.ndimage import gaussian_filter


def load_session_data(session, save_file, group, condition):
    

    # using similar directory to open files that i didn't explicitely add to the dictionary
    session['behavior_time'] = session['behavior'].replace("_events.csv", "_analyzed_extracted.csv")
    session['duration'] = session['auc'].replace("auc", "duration")
    session['width'] = session['auc'].replace("auc", "width")
    session['ampltitude'] = session['auc'].replace("auc", "amplitude")
    session['posiiton'] = session['behavior'].replace("_events.csv", "_analyzed.csv")

    time = pd.read_csv(session['time'])
    signal = pd.read_csv(session['signal'])
    event = pd.read_csv(session['event'])
    behavior = pd.read_csv(session['behavior'])
    behavior_time = pd.read_csv(session['behavior_time'])
    position = pd.read_csv(session['posiiton'])

    auc = pd.read_csv(session['auc'])
    duration = pd.read_csv(session['duration'])
    width = pd.read_csv(session['width'])
    amplitude = pd.read_csv(session['ampltitude'])
    

    location = position.iloc[2:, [1,2, 3, 11, 12, 14, 15]]
    location.columns = ['time', 'x', 'y', 'objectA_x', 'objectA_y', 'objectB_x', 'objectB_y']
    location = location.apply(pd.to_numeric, errors='coerce').dropna()


    
    frame_intervals = np.diff(time)
    frame_rate = 1 / np.median(frame_intervals)


    minutes = (behavior_time.iloc[0, 0]) / 60
    auc_rate = auc / minutes


    #column labeling of the session values
    time.columns = ['time']
    signal.columns = ['df/f']
    event.columns = ['time']
    auc.columns = ['auc']
    duration.columns = ['duration']
    width.columns = ['width']
    amplitude.columns = ['amplitude']
    auc_rate.columns = ['auc_rate']

    signal_trace = pd.concat([time, signal], axis=1)
    
     #  time_values = time['time'].values
      #  frame_intervals = np.diff(time_values)
       # frame_rate = 1 / np.median(frame_intervals)
        #print("Detected frame rate:", frame_rate)
#
 #       target_rate = 60.23   # Hz (≈0.0166 s/sample)
  #      target_interval = 1 / target_rate
   #     new_time = np.arange(time_values[0], time_values[-1], target_interval)
#
 #       
  #     # Create interpolation function
  #      interp_func = interp1d(time_values, signal['df/f'].values,
   #                         kind='linear', fill_value='extrapolate')
#
        # Apply to new 60 Hz grid
 #       resampled_signal = interp_func(new_time)
#
        # Build resampled DataFrame
  #      signal_trace_resampled = pd.DataFrame({
   #         'time': new_time,
    #        'df/f': resampled_signal
     #   })
            
      #  signal_trace = signal_trace_resampled

       # print(signal_trace
        #    )



    # combining event related variables for better access
    events_related = pd.concat([event, auc, duration, width, amplitude, auc_rate], axis=1) 

    # from the behavior file we're only taking the rows that are related to the time at which entrance or exit occured
    df_en_a = behavior.iloc[:, [1]].rename(columns={behavior.columns[1]: 'timestamps'})
    df_en_b = behavior.iloc[:, [5]].rename(columns={behavior.columns[5]: 'timestamps'})
    df_ex_a = behavior.iloc[:, [2]].rename(columns={behavior.columns[2]: 'timestamps'})
    df_ex_b = behavior.iloc[:, [6]].rename(columns={behavior.columns[6]: 'timestamps'})

    df_a = pd.concat([df_en_a, df_ex_a], axis=1) # both entrance and exit of A
    df_b = pd.concat([df_en_b, df_ex_b], axis=1) # both entrance and exit of B

    # individual and grouped action dfs
    individual_dfs = [df_en_a, df_en_b, df_ex_a, df_ex_b]

    grouped_dfs = [df_a, df_b]

    all_interactions = pd.concat([
        df_en_a['timestamps'],
        df_en_b['timestamps'],

    ]).dropna().sort_values().reset_index(drop=True)

   #  plot_entire(signal_trace, all_interactions, session, save_file, group, condition)
    print("don't forget this^^")

    # the initial csv use seconds to compute total time taken so we're converting them to minutes

    
    
    # we're using a function that takes the averaged event values of the entirety of a session as well as getting the total events within the object interaction
    auc_means_a, auc_means_b, aucs, total_events_a, total_events_b, duration = session_event_related_means(grouped_dfs, "auc", events_related)
    duration_means_a, duration_means_b, durations, *_ = session_event_related_means(grouped_dfs, "duration", events_related) 
    width_means_a, width_means_b, widths, *_ = session_event_related_means(grouped_dfs, "width", events_related) 
    amplitude_means_a, amplitude_means_b, ampltitudes, *_ = session_event_related_means(grouped_dfs, "amplitude", events_related)

    print((auc_means_a))
    print(len(auc_means_a))
    print(len(durations))

    # events divided by total time
    event_rate_a = total_events_a / minutes
    event_rate_b = total_events_b / minutes

    print(f"--- Debug Info for {session['id']} ({condition}) ---")
    print(f"  Total Events (A): {total_events_a}")
    print(f"  Total Events (B): {total_events_b}")
    print(f"  Session Duration (minutes): {minutes:.2f}")
    print(f"  Calculated Event Rate (A): {event_rate_a:.2f} events/min")
    print(f"  Calculated Event Rate (B): {event_rate_b:.2f} events/min\n")

    
    location = mouse_speed(location)
    plt.close()
    # behavorial action
    # Original -10s to +10s window for signal traces
    beh_dfs = extract_action_window(individual_dfs, signal_trace, pre_time=10, post_time=10)

    # New window: -5s to 0s (pre-event)
    beh_dfs_pre_event = extract_action_window(individual_dfs, signal_trace, pre_time=5, post_time=0)
    print(f"beh_dfs_pre_event: {beh_dfs_pre_event}")
    # New window: 0s to +5s (post-event)
    beh_dfs_post_event = extract_action_window(individual_dfs, signal_trace, pre_time=0, post_time=5)
    print(f"beh_dfs_post_event: {beh_dfs_post_event}")
    
    locomotion = locomotion_epochs(signal_trace, location, pre_time=10,   post_time=10 )
    stationary = stationary_epochs(signal_trace, location, pre_time=10, post_time=10 )
    
    print(f"locomotion_epochs: {len(locomotion)}")
    # print(f"stationary_epochs: {len(stationary)}")

    # for i, e in enumerate(locomotion[:3]):
    #     print(f"Epoch {i} columns:", e.columns.tolist())


    # stationary_locomotion(locomotion, stationary, pre_time=10, post_time=10)




    print(beh_dfs)


    # REGULARLY THE EVENT ACTION WINDOW IS 7.5 TO 5 SECONDS
    #IN ORDER TO ACCESS THE INTERACTION TIME WE'RE TEMPORARILY USING 10 AND 10 SECONDS
    eve_dfs = event_action_window(individual_dfs, events_related, pre_time=10, post_time=10)


    # New windows for event-related data
    eve_dfs_pre_event = event_action_window(individual_dfs, events_related, pre_time=5, post_time=0)
    eve_dfs_post_event = event_action_window(individual_dfs, events_related, pre_time=0, post_time=5)

    non_interaction_epochs = extract_non_interaction_epochs(individual_dfs, signal_trace, epoch_duration=20, gap_after_exit=5)
    # Extract non-interaction epochs

    corner_epochs = corner_detection(individual_dfs, signal_trace, position_df=location, epoch_duration=20)


    
    print(f"here: {non_interaction_epochs}")
    print(f"session: {session}")
    print(f"Found {len(non_interaction_epochs)} non-interaction epochs for this session.")




    # including all the vlaues we've extracted into dictionary
    results = {
    "beh_dfs": beh_dfs,
    "beh_dfs_pre_event": beh_dfs_pre_event,
    "beh_dfs_post_event": beh_dfs_post_event,
    "eve_dfs": eve_dfs,
    "eve_dfs_pre_event": eve_dfs_pre_event,
    "eve_dfs_post_event": eve_dfs_post_event,
    "signal": signal,
    "event": event,
    "auc": auc,
    "signal_trace": signal_trace,
    "auc_means": (auc_means_a, auc_means_b, aucs),
    "total_events": (total_events_a, total_events_b),
    "event_rate": (event_rate_a, event_rate_b),
    "duration_means": (duration_means_a, duration_means_b, durations),
    "width_means": (width_means_a, width_means_b, widths),
    "amplitude_means": (amplitude_means_a, amplitude_means_b, ampltitudes),
    "location": location,
    "non_interaction_epochs": non_interaction_epochs,
    "individual_dfs": individual_dfs,
    "corner_epochs": corner_epochs,
    "locomotion_epochs": locomotion,
    "stationary_epochs": stationary,

    }
    return results


def plot_entire(signal_trace, all_interactions, session, save_file, group, condition):


    # Extract session ID safely
    session_id = session['id'] 

    # Interpolate y-values for interactions
    interaction_y_values = np.interp(all_interactions, signal_trace['time'], signal_trace['df/f'])

    # --- Plot 1: Detailed Two-Panel Figure ---
    fig1, ax1 = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    
    ax1[0].plot(signal_trace['time'], signal_trace['df/f'], label='Signal (df/f)')
    ax1[0].scatter(all_interactions, interaction_y_values, color='red', s=5, marker='x', label='Interactions', zorder=5)
    ax1[0].set_title(f'Signal Trace and Interaction Events for {session_id} {group} - {condition}')
    ax1[0].legend()

    ax1[1].stem(all_interactions, [1]*len(all_interactions), linefmt='r-', markerfmt='', basefmt=" ", label='Interactions') 
    ax1[1].set_xlabel('Time (s)')
    ax1[1].set_ylabel('Events')
    ax1[1].legend()

    plt.tight_layout()

    if False:
        fig1.savefig(
            f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/entire_recording/type1_{group}_{condition}_{session_id}.svg',
            format='svg', dpi=300
        )

    # --- Plot 2: Integrated, Cleaner Figure ---
    fig2, ax = plt.subplots(2, 1, figsize=(12, 5), sharex=True, gridspec_kw={'height_ratios': [2, 1]})
    fig2.subplots_adjust(hspace=0)

    ax[0].plot(signal_trace['time'], signal_trace['df/f'], label='Signal (df/f)')
    ax[0].scatter(all_interactions, interaction_y_values, color='red', s=8, marker='x', label='Interactions', zorder=5)
    ax[0].set_title(f"Signal Trace and Interaction for {session_id} {group} - {condition}")
    ax[0].legend()
    ax[0].spines[['top', 'right', 'bottom', 'left']].set_visible(False)
    ax[0].set_yticks([])

    ax[1].stem(all_interactions, [1]*len(all_interactions), linefmt='r-', markerfmt='', basefmt=" ", label='Interactions') 
    ax[1].set_xlabel('Time (s)')
    ax[1].spines[['top', 'right', 'left']].set_visible(False)
    ax[1].set_yticks([])

    plt.tight_layout()

    if False:
        fig2.savefig(
            f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/entire_recording/type2_{group}_{condition}_{session_id}.svg',
            format='svg', dpi=300
        )

    return fig1, fig2



def positional(location, signal_trace, session, group, condition, bins=100, sigma=2, xlim=None, ylim=None, margin_ratio=0.05):
    location['time_rounded'] = location['time'].round(1)
    signal_trace['time_rounded'] = signal_trace['time'].round(1)
    merged_df = pd.merge(location, signal_trace, on='time_rounded')

    # Remove top 1% df/f values
    # upper_cut = merged_df["df/f"].quantile(0.95)
    # merged_df.loc[merged_df["df/f"] > upper_cut, "df/f"] = upper_cut


    # --- Automatically determine x/y limits based on position data ---
    if xlim is None:
        x_min_data, x_max_data = merged_df['x'].min(), merged_df['x'].max()
        x_range = x_max_data - x_min_data
        x_min = x_min_data - x_range * margin_ratio
        x_max = x_max_data + x_range * margin_ratio
    else:
        x_min, x_max = xlim

    if ylim is None:
        y_min_data, y_max_data = merged_df['y'].min(), merged_df['y'].max()
        y_range = y_max_data - y_min_data
        y_min = y_min_data - y_range * margin_ratio
        y_max = y_max_data + y_range * margin_ratio
    else:
        y_min, y_max = ylim


    # --- Bin edges based on computed limits ---
    x_bins = np.linspace(x_min, x_max, bins)
    y_bins = np.linspace(y_min, y_max, bins)

    x_offset = 0#80
    y_offset = 0#130

    merged_df['x_bin'] = np.clip(np.digitize(merged_df['x'] - x_offset, bins=x_bins) - 1, 0, bins - 2)

    merged_df['y_bin'] = np.clip(np.digitize(merged_df['y'] - y_offset, bins=y_bins) - 1, 0, bins - 2)

    # --- Compute mean df/f per spatial bin ---
    heatmap = merged_df.groupby(['y_bin', 'x_bin'])['df/f'].mean().unstack()
    heatmap_filled = np.nan_to_num(heatmap, nan=0)
    heatmap_smooth = gaussian_filter(heatmap_filled, sigma=sigma)
    heat = heatmap_smooth
    heat_norm = (heat - 1.0474183599148584e-06) / (0.011608681079619683 - 1.0474183599148584e-06)
    cropped_heatmap = heat_norm[18:, :]




    # print(f"Heres the heatmap{heatmap_smooth}")


    fig, ax = plt.subplots(figsize=(8, 6))
    cmap = plt.cm.get_cmap('turbo')

    # --- Plot heatmap ---
    cax = ax.imshow(
        cropped_heatmap,
        origin='lower',
        cmap=cmap,
        extent=[x_min, x_max, y_min, y_max],
        alpha=0.9,
        aspect='equal',
        vmax=1.0,
        vmin=0


    )


    vmin, vmax = cax.get_clim()
    print(f"Colorbar limits: vmin={vmin}, vmax={vmax}")





    objectA_x = location['objectA_x'].mean(axis=0) 
    objectA_y = location['objectA_y'].mean(axis=0) 
    objectB_x = location['objectB_x'].mean(axis=0) 
    objectB_y = location['objectB_y'].mean(axis=0) 




    objects = pd.DataFrame({

        'objectA_x': [location['objectA_x'].mean(axis=0)],
        'objectA_y': [location['objectA_y'].mean(axis=0)],
        'objectB_x': [location['objectB_x'].mean(axis=0)],
        'objectB_y': [location['objectB_y'].mean(axis=0)],
        'x_min': [x_min],
        'x_max': [x_max],
        'y_min': [y_min],
        'y_max': [y_max]

    })


    objects.reset_index(drop=True)



    


    objectA = patches.Rectangle((objectA_x - 37.5, objectA_y - 37.5), 75, 75, linewidth=3, edgecolor='r', facecolor='none')
    objectB = patches.Rectangle((objectB_x - 37.5, objectB_y - 37.5), 75, 75, linewidth=3, edgecolor='b', facecolor='none')

    ax.add_patch(objectA)
    ax.add_patch(objectB)

    # --- Add colorbar and labels ---
    cbar = fig.colorbar(cax)
    cbar.set_label('Average df/f')

    ax.set_title(f"Positional df/f Heatmap for {group} {condition}")
    ax.set_xlabel("X-coordinate")
    ax.set_ylabel("Y-coordinate")
    ax.set_xlim(x_min - x_offset, x_max)
    ax.set_ylim(y_min, y_max)
    ax.legend()
    plt.close()
    #plt.tight_layout()


    if False:
        fig.savefig(
            f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOLfixed/heatmap_updated/requestedheatmap/map{session['id']}_{group}_{condition}_positional_heatmap.svg',
            format='svg', dpi=300

        )   

    return heatmap_smooth, objects
