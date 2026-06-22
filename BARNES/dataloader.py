import pandas as pd
from session_dict import barnes_session_dict
from event_related import events_within_action_window , event_action_window, compute_session_auc_means, extract_action_window, session_event_related_means
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

from scipy.ndimage import gaussian_filter


def load_session_data(session, save_file):
    

    # using similar directory to open file

    session['behavior_time'] = session['behavior'].replace("_events.csv", "_analyzed_extracted.csv")
    session['auc'] = session['signal'].replace("signal", "auc")
    session['duration'] = session['signal'].replace("signal", "duration")
    session['width'] = session['signal'].replace("signal", "width")
    session['ampltitude'] = session['signal'].replace("signal", "amplitude")
    session['position'] = session['behavior'].replace("_events.csv", "_analyzed.csv")

    time = pd.read_csv(session['time'])
    signal = pd.read_csv(session['signal'])
    event = pd.read_csv(session['event'])
    behavior = pd.read_csv(session['behavior'])
    behavior_time = pd.read_csv(session['behavior_time'])

    auc = pd.read_csv(session['auc'])
    duration = pd.read_csv(session['duration'])
    width = pd.read_csv(session['width'])
    amplitude = pd.read_csv(session['ampltitude'])
    position = pd.read_csv(session['position'])
    
    minutes = behavior_time.iloc[0, 0] / 60
    auc_rate = auc / minutes

    #column labeling of the session values

    # Dynamically generate column indices and names for all 20 holes
    # Base columns for time and mouse position
    column_indices = [1, 2, 3]  # time, x, y
    column_names = ['time', 'x', 'y']

    # Start index for the first hole's x-coordinate
    start_col_index = 8 
    for i in range(20):
        hole_x_index = start_col_index + (i * 3)
        hole_y_index = hole_x_index + 1
        column_indices.extend([hole_x_index, hole_y_index])
        column_names.extend([f'hole_{i+1}_x', f'hole_{i+1}_y'])

    location = position.iloc[2:, column_indices]
    location.columns = column_names
    

    time.columns = ['time']
    signal.columns = ['df/f']
    event.columns = ['time']
    auc.columns = ['auc']
    duration.columns = ['duration']
    width.columns = ['width']
    amplitude.columns = ['amplitude']
    auc_rate.columns = ['auc_rate']

    # Convert to numeric, coercing errors will turn non-numeric values into NaN
    location = location.apply(pd.to_numeric, errors='coerce').dropna()

    # For backward compatibility with positional function, let's alias the escape hole
    location['escape_x'] = location['hole_1_x']
    location['escape_y'] = location['hole_1_y']


    # combining time and signal for easier access
    signal_trace = pd.concat([time, signal], axis=1) 
    # combining events and auc for better access: event time and it's auc
    events_related = pd.concat([event, auc, duration, width, amplitude, auc_rate], axis=1) 

   
   
   # MAKE SURE TO REMOVE IF WANT TO USE POSITIONAL

    manual_map = {
    "escape": (738.4072875976562, 179.37542724609375),
    "holes": [
        (820.4266357421875, 280.7895812988281),
        (864.2387084960938, 400.3412170410156),
        (867.1669921875, 526.9323120117188),
        (828.9481811523438, 650.6558837890625),
        (755.9608154296875, 752.5498657226562),
        (654.2119750976562, 828.798828125),
        (532.2509765625, 866.0549926757812),
        (412.8546752929687, 868.3158569335938),
        (293.1972961425781, 826.1870727539062),
        (195.82485961914065, 755.0887451171875),
        (121.05014038085938, 660.7401123046875),
        (82.0280990600586, 541.8516845703125),
        (79.95576477050781, 422.2789611816406),
        (112.53396606445312, 304.1294250488281),
        (182.46307373046875, 203.8612060546875),
        (278.55865478515625, 126.29505157470705),
        (394.7107849121094, 85.7212905883789),
        (514.96435546875, 77.87523651123047),
        (635.4135131835938, 109.96292877197266)
    ]
    }
#    positional_with_manual_override(location, signal_trace, session, manual_map)
   
   
    #positional(location, signal_trace, session)

    df_a = behavior.loc[behavior['object'] == 'escape']
    df_b = behavior.loc[behavior['object'] != 'escape'] 

    # stripping only entrance, exits from the behavior file
    df_en_a = df_a.iloc[:, [2]].rename(columns={behavior.columns[2]: 'timestamps'}) #entrance
    df_ex_a = df_a.iloc[:, [3]].rename(columns={behavior.columns[3]: 'timestamps'}) # exit

    timestamps_a = df_en_a['timestamps'].tolist()


    df_en_b = df_b.iloc[:, [2]].rename(columns={behavior.columns[2]: 'timestamps'}) #entrance
    df_ex_b = df_b.iloc[:, [3]].rename(columns={behavior.columns[3]: 'timestamps'}) # exit




    df_a = pd.concat([df_en_a, df_ex_a], axis=1) # both entrance and exit
    df_b = pd.concat([df_en_b, df_ex_b], axis=1)


    # individual and grouped action dfs
    individual_dfs = [df_en_a, df_en_b, df_ex_a, df_ex_b]


    grouped_dfs = [df_a, df_b]


    # plot_entire(signal_trace, df_en_a['timestamps'].dropna(),df_en_b['timestamps'].dropna(), session, save_file)
    
    

    # we're using a function that takes the averaged event values of the entirety of a session as well as getting the total events within the object interaction
    auc_means_a, auc_means_b, aucs, total_events_a, total_events_b = session_event_related_means(grouped_dfs, "auc", events_related)
    duration_means_a, duration_means_b, durations, *_ = session_event_related_means(grouped_dfs, "duration", events_related) 
    width_means_a, width_means_b, widths, *_ = session_event_related_means(grouped_dfs, "width", events_related) 
    amplitude_means_a, amplitude_means_b, ampltitudes, *_ = session_event_related_means(grouped_dfs, "amplitude", events_related)
    auc_rate_means_a, auc_rate_means_b, auc_rates, *_ = session_event_related_means(grouped_dfs, "auc_rate", events_related)

    # events divided by total time
    event_rate_a = total_events_a / minutes
    event_rate_b = total_events_b / minutes


    # behavorial action
    beh_dfs = extract_action_window(individual_dfs, signal_trace)

    eve_dfs = event_action_window(individual_dfs, events_related, pre_time=0, post_time=10) # finds the event values between say time point A and B

    eve_dfs_pre_event = event_action_window(individual_dfs, events_related, pre_time=5, post_time=0)
    eve_dfs_post_event = event_action_window(individual_dfs, events_related, pre_time=0, post_time=5)

    # including all the vlaues we've extracted into dictionary
    results = {
    "beh_dfs": beh_dfs,
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
    "auc_rate_means": (auc_rate_means_a, auc_rate_means_b, auc_rates),
    "location": location
    }
    return results


def plot_entire(signal_trace, escape, nonescape, session, save_file ):


    # Extract session ID safely
    session_id = session['id'] 
    day = session['day']
    phase = session['phase']

    # Interpolate y-values for interactions
    interaction_y_values1 = np.interp(nonescape, signal_trace['time'], signal_trace['df/f'])
    interaction_y_values2 = np.interp(escape, signal_trace['time'], signal_trace['df/f'])


    # --- Plot 1: Detailed Two-Panel Figure ---
    fig, ax1 = plt.subplots(2, 1, figsize=(12, 6), sharex=True)
    
    ax1[0].plot(signal_trace['time'], signal_trace['df/f'], label='Signal (df/f)')
    #ax1[0].scatter(all_interactions, interaction_y_values, color='red', s=5, marker='x', label='Interactions', zorder=5)
    ax1[0].set_title(f'Signal Trace and Interaction Events for {session_id} {phase} - {day}')
    ax1[0].legend()

    if not escape.empty:
        ax1[1].stem(escape, [1]*len(escape), linefmt='r-', markerfmt='', basefmt=" ", label='Escape Interactions') 
    if not nonescape.empty:
        ax1[1].stem(nonescape, [1]*len(nonescape), linefmt='g-', markerfmt='', basefmt=" ", label='Non-Escape Interactions') 
    ax1[1].set_xlabel('Time (s)')
    ax1[1].set_ylabel('Events')
    ax1[1].legend()

    plt.tight_layout()


    if False:
        fig.savefig(
            f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/entire_recording/{phase}_{day}_{session_id}.svg',
            format='svg', dpi=300
        )



    return fig




def positional(location, signal_trace, session, bins=100, sigma=2):

    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    from scipy.ndimage import gaussian_filter
    import matplotlib.patches as patches

    # ------------------------------------------------------
    # 1. Merge time-aligned datasets
    # ------------------------------------------------------
    location["time_rounded"] = location["time"].round(1)
    signal_trace["time_rounded"] = signal_trace["time"].round(1)
    merged_df = pd.merge(location, signal_trace, on="time_rounded")

    # ------------------------------------------------------
    # 2. Define arena boundaries relative to the escape hole
    # -> New strategy: Center the maze at (0,0)
    # ------------------------------------------------------
    MAZE_RADIUS = 400

    # --- Extract initial hole coordinates (use first row to avoid drift) ---
    raw_hole_coords = np.array([
        [location[f'hole_{i}_x'].iloc[0], location[f'hole_{i}_y'].iloc[0]]
        for i in range(1, 21)
    ])

    # --- Circle-fitting using least-squares (Kåsa method) ---
    x = raw_hole_coords[:, 0]
    y = raw_hole_coords[:, 1]

    A = np.column_stack([x, y, np.ones_like(x)])
    b = -(x**2 + y**2)
    C, D, E = np.linalg.lstsq(A, b, rcond=None)[0]
    center_x_raw = -C / 2
    center_y_raw = -D / 2
    radius = np.sqrt((C**2 + D**2) / 4 - E)

    # --- Compute rotation offset so ideal circle aligns with actual escape hole ---
    escape_x_raw = location["escape_x"].iloc[0]
    escape_y_raw = location["escape_y"].iloc[0]

    real_escape_angle = np.arctan2(escape_y_raw - center_y_raw,
                                   escape_x_raw - center_x_raw)

    ideal_escape_index = 0  # hole_1_x corresponds to escape
    ideal_escape_angle = 2 * np.pi * ideal_escape_index / 20

    rotation_offset = real_escape_angle - ideal_escape_angle

    # --- Generate ideal evenly spaced hole positions with rotation applied ---
    ideal_holes_x = []
    ideal_holes_y = []
    for k in range(20):
        angle = 2 * np.pi * k / 20 + rotation_offset
        ideal_holes_x.append(center_x_raw + radius * np.cos(angle))
        ideal_holes_y.append(center_y_raw + radius * np.sin(angle))

    # These replace all raw hole positions
    hole_x_vals = ideal_holes_x
    hole_y_vals = ideal_holes_y


    # Shift all coordinates to be centered around (0,0)
    merged_df['x_shifted'] = merged_df['x'] - center_x_raw
    merged_df['y_shifted'] = merged_df['y'] - center_y_raw

    # Define new arena boundaries centered at (0,0)
    all_x = np.array(merged_df['x'].values.tolist() + hole_x_vals)
    all_y = np.array(merged_df['y'].values.tolist() + hole_y_vals)
    max_extent = max(
        np.max(np.abs(all_x - center_x_raw)),
        np.max(np.abs(all_y - center_y_raw))
    )
    ARENA_SIZE = max_extent + 50 # Add 50px padding
    x_min, x_max = -ARENA_SIZE, ARENA_SIZE
    y_min, y_max = -ARENA_SIZE, ARENA_SIZE
    escape_x_raw = location["escape_x"].iloc[0]
    escape_y_raw = location["escape_y"].iloc[0]

    # ------------------------------------------------------
    # 3. Define bin edges for the heatmap
    # ------------------------------------------------------

    
    # Define bin edges with bins+1 to cover full range
    x_edges = np.linspace(x_min, x_max, bins + 1)
    y_edges = np.linspace(y_min, y_max, bins + 1)

    # Digitize into bins safely
    merged_df['x_bin'] = np.digitize(merged_df['x_shifted'], x_edges) - 1
    merged_df['y_bin'] = np.digitize(merged_df['y_shifted'], y_edges) - 1

    # Clip bins to valid range
    merged_df['x_bin'] = merged_df['x_bin'].clip(0, bins - 1)
    merged_df['y_bin'] = merged_df['y_bin'].clip(0, bins - 1)

    # Compute bin centers for plotting alignment
    x_bin_centers = (x_edges[:-1] + x_edges[1:]) / 2
    y_bin_centers = (y_edges[:-1] + y_edges[1:]) / 2
    merged_df['x_plot'] = x_bin_centers[merged_df['x_bin'].values]
    merged_df['y_plot'] = y_bin_centers[merged_df['y_bin'].values]

    # ------------------------------------------------------
    # 5. Compute heatmap matrix
    # ------------------------------------------------------
    heatmap_matrix = np.full((bins, bins), np.nan)
    grouped = merged_df.groupby(['y_bin', 'x_bin'])['df/f'].mean()
    for (y_idx, x_idx), value in grouped.items():
        if 0 <= y_idx < bins and 0 <= x_idx < bins:
            heatmap_matrix[y_idx, x_idx] = value

    heatmap_matrix[np.isnan(heatmap_matrix)] = 0
    heat_smooth = gaussian_filter(heatmap_matrix, sigma=sigma)

    norm_min = np.min(heat_smooth[heat_smooth > 0]) if np.any(heat_smooth > 0) else 0
    norm_max = 0.014
    heat_norm = (heat_smooth - norm_min) / (norm_max - norm_min)
    heat_norm = np.clip(heat_norm, 0, 1)

    # ------------------------------------------------------
    # 6. Plotting
    # ------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    cmap = plt.get_cmap("turbo")

    extent = [x_min, x_max, y_min, y_max]

    # --- Draw heatmap ---
    cax = ax1.imshow(
        heat_norm,
        origin="lower",
        cmap=cmap,
        extent=extent,
        aspect="equal",
        vmin=0,
        vmax=1
    )

    # --- Draw zero-activity background on ax2 ---
    ax2.imshow(
        np.zeros_like(heat_norm),
        origin="lower",
        cmap=cmap,
        extent=extent,
        aspect="equal",
        vmin=0,
        vmax=1
    )

    # ------------------------------------------------------
    # Draw maze boundary circle
    # ------------------------------------------------------
    # maze_circle = patches.Circle(
    #     (0, 0),  # Centered at the new origin
    #     MAZE_RADIUS,
    #     linewidth=2,
    #     edgecolor='white',
    #     facecolor='none',
    #     linestyle='--',
    #     alpha=0.7,
    #     label='Maze Boundary'
    # )
    # ax.add_patch(maze_circle)

    # ------------------------------------------------------
    # 7. Scatter mouse path (unchanged)
    # ------------------------------------------------------
    ax2.scatter(
        merged_df["x_shifted"],
        merged_df["y_shifted"],
        marker="o",
        color="white",
        s=1.5,
        alpha=0.3,
        label="Mouse Path"
    )

    # ------------------------------------------------------
    # 8. Escape hole (raw coordinates)
    # ------------------------------------------------------
    escape_x_shifted = escape_x_raw - center_x_raw
    escape_y_shifted = escape_y_raw - center_y_raw

    for ax in [ax1, ax2]:
        ax.scatter(
            escape_x_shifted,
            escape_y_shifted,
            s=40,
            color="red",
            marker="x",
            label="Escape Hole"
        )

    # ------------------------------------------------------
    # 8b. Other holes (holes 2-20)
    # ------------------------------------------------------
    for i in range(2, 21):
        hole_x_ideal = ideal_holes_x[i-1]
        hole_y_ideal = ideal_holes_y[i-1]
        hole_x_shifted = hole_x_ideal - center_x_raw
        hole_y_shifted = hole_y_ideal - center_y_raw

        # Plot hole as white circle with interaction zone
        for ax in [ax1, ax2]:
            ax.scatter(
                hole_x_shifted,
                hole_y_shifted,
                s=30,
                facecolors='none',
                edgecolors='white',
                label='Hole' if i == 2 else None
            )
            zone_radius = 35
            ax.add_patch(patches.Circle(
                (hole_x_shifted, hole_y_shifted),
                radius=zone_radius,
                linewidth=1,
                edgecolor='white',
                facecolor='none',
                linestyle='--',
                alpha=0.7
            ))

    # ------------------------------------------------------
    # 9. Aesthetics
    # ------------------------------------------------------
    cbar = fig.colorbar(cax)
    cbar.set_label("Average df/f")

    ax1.set_title(f"Heatmap for Session {session['id']} Day {session['day']} {session['phase']}")
    ax1.set_xlabel("X Position")
    ax1.set_ylabel("Y Position")

    ax1.set_xlim(x_min, x_max)
    ax1.set_ylim(y_min, y_max)
    ax2.set_xlim(x_min, x_max)
    ax2.set_ylim(y_min, y_max)
    ax1.legend()
    ax2.legend()

    print(f"Heatmap for Session {session['id']} Day {session['day']} {session['phase']}")
    print(f"Here are the raw coordinates {escape_x_raw} {escape_y_raw}")
    print(f"its shifted by {center_x_raw} {center_y_raw}")
    print(f"Here is the escape coordinates {escape_x_shifted} {escape_y_shifted}")
    plt.tight_layout()



    if True:
        fig.savefig(
            f"/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/heatmap/revamped/map_{session['id']}_{session['day']}_{session['phase']}.svg",
            format='svg', dpi=300
        )



    return heat_smooth, {"escape_x": escape_x_shifted, "escape_y": escape_y_shifted}

def positional_with_manual_override(location, signal_trace, session, manual_map):
    # Create a copy to avoid modifying the original DataFrame passed into the function
    location_overridden = location.copy()

    # Overwrite the static hole coordinate columns with values from manual_map.
    # This ensures every row in these columns has the correct manual coordinate.
    location_overridden['escape_x'] = manual_map["escape"][0]
    location_overridden['escape_y'] = manual_map["escape"][1]

    # Assign hole_1 as escape, holes_2–20 as manual holes
    location_overridden['hole_1_x'] = manual_map["escape"][0]
    location_overridden['hole_1_y'] = manual_map["escape"][1]

    for idx, (hx, hy) in enumerate(manual_map["holes"], start=2):
        location_overridden[f'hole_{idx}_x'] = hx
        location_overridden[f'hole_{idx}_y'] = hy

    return positional(location_overridden, signal_trace, session)