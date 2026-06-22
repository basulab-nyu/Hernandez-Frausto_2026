import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from scipy.stats import sem
import math
# not used


def event_rate(all_events, group, condition, action="", title="", save_path=None):
    """
    Plots a bar chart comparing the mean event rates (events per minute) for Object A vs Object B, 
    as well as the combined average of both objects.

    Parameters:
    - all_events: Dictionary containing the event rate data.
    - group: Experimental group name (e.g., 'NOR', 'NOL').
    - condition: Experimental condition (e.g., 'FAM', 'NOV').
    - action: Label indicating the action (used for saving).
    - title: Custom title for the plot.
    - save_path: Path/boolean to save the figure.
    """
    labels = ['Object A', 'Object B']
    combined = ["A + B"]

    # finding the mean of the events per minute for each mouse 
    mean_a = np.mean(all_events[group][condition]['A'])
    mean_b = np.mean(all_events[group][condition]['B'])
    mean_ab = np.mean([mean_a, mean_b])

    counts = [mean_a, mean_b]

    fig, ax = plt.subplots(figsize=(5,4))

    bars = ax.bar(labels, counts, color=['skyblue', 'salmon'])

    ax.set_ylabel('Event Rate')
    ax.set_title(f' Events per Minute{group} - {condition}')
    ax.bar_label(bars)
    plt.tight_layout()

    fig, ax = plt.subplots(figsize=(5, 4))

    bar = ax.bar(combined, [mean_ab], color=['gray'])
    ax.set_ylabel('Event Rate')
    ax.set_title(f' Events per Minute{group} - {condition}')
    ax.bar_label(bar)
    plt.tight_layout()


    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/images/events/rate{action}{group}{condition}.png')

def histo(all, group, condition, zscore, trunc_time, title="", save_path=None, action=""):
    """
    Plots a 4-panel histogram displaying the distribution of data points (e.g., AUCs) 
    for Object A and Object B across both FAM and NOV conditions.
    
    Parameters:
    - all: Dictionary containing the data values to distribute.
    - group: Experimental group name (e.g., 'NOR', 'NOL').
    - condition: Condition label (FAM vs NOV).
    - zscore: Boolean indicating if the data is z-scored.
    - trunc_time: Total seconds collected.
    - title: Title for the histogram plot.
    - save_path: If provided, saves the output.
    - action: Context of the action (e.g., 'entrance').
    """
    time_interval = 0.01660136795
    truncate = round(trunc_time / time_interval)
    # print(trace_a)
    # print(trace_a.shape)
    # print(trace_a.values.size)

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(ncols=4, figsize=(10, 4), sharex=True, sharey=True)
    ax1.hist(all[group]["FAM"]["All_a"], bins=25)
    ax1.set_xlabel("Object A")
    ax1.set_ylabel("Count")
    ax1.set_title("FAM")

    ax2.hist(all[group]["FAM"]["All_b"], bins=25)
    ax2.set_xlabel("Object B")
    ax2.set_title("FAM")

    ax3.hist(all[group]["NOV"]["All_a"], bins=25, alpha=0.7)
    ax3.set_xlabel("Object A")
    ax3.set_ylabel("Count")
    ax3.set_title("NOV")

    ax4.hist(all[group]["NOV"]["All_b"], bins=25, alpha=0.7)
    ax4.set_xlabel("Object B")
    ax4.set_title("NOV")

    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/histogram/{action}{group}.svg', format='svg')

def auc_rate_scatter(all, group, epoch, unit, save_path=None, action=""):
    """
    Creates a scatter plot comparing FAM vs NOV values (e.g., AUC/MIN) for each session.
    Includes both a per-session mean scatter plot and a plot with all individual values pooled.
    A reference line (y=x) is included to easily visualize shifts between conditions.
    
    Parameters:
    - all: Dictionary containing the data values.
    - group: Group name (e.g., 'NOR', 'NOL').
    - epoch: The interaction epoch period (e.g., "peri-event").
    - unit: The unit of the metric being measured (used for axis labels).
    - save_path: If provided, saves the output plot.
    - action: Interaction action context.
    """


    fam_a = all[group]["FAM"]['All_a']   # list of arrays, one per session

    fam_b = all[group]["FAM"]['All_b']   # list of arrays, one per session 

    nov_a = all[group]["NOV"]['All_a']
    nov_b = all[group]["NOV"]['All_b']
# Flatten across sessions (all values pooled)
    fam_all_a = np.concatenate(fam_a)

    fam_all_b = np.concatenate(fam_b)
    


    nov_all_a = np.concatenate(nov_a)
    nov_all_b = np.concatenate(nov_b)


    min_len_a = min(len(fam_all_a), len(nov_all_a))
    min_len_b = min(len(fam_all_b), len(nov_all_b))
# Mean per session
    fam_a_means = [np.nanmean(sess) for sess in fam_a]
    fam_b_means = [np.nanmean(sess) for sess in fam_b]
    nov_a_means = [np.nanmean(sess) for sess in nov_a]
    nov_b_means = [np.nanmean(sess) for sess in nov_b]


    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4), sharex=True, sharey=True)

    # Per-session mean scatter
    ax1.scatter(fam_a_means, nov_a_means, s=50, color='blue', edgecolor='k', alpha=0.7, label="Object A")
    ax1.scatter(fam_b_means, nov_b_means, s=50, color='orange', edgecolor='k', alpha=0.7, label="Object B")
    ax1.set_title(f"{group} Per-session means")

    # All-values scatter
    min_len_a = min(len(fam_all_a), len(nov_all_a))
    min_len_b = min(len(fam_all_b), len(nov_all_b))
    ax2.scatter(fam_all_a[:min_len_a], nov_all_a[:min_len_a], s=50, color='blue', edgecolor='k', alpha=0.7)
    ax2.scatter(fam_all_b[:min_len_b], nov_all_b[:min_len_b], s=50, color='orange', edgecolor='k', alpha=0.7)
    ax2.set_title("All values pooled")

    # Add reference line to both
    for ax in (ax1, ax2):
        ax.axline((0, 0), slope=1, color='red', linestyle='--')
        ax.legend()

    y1limits = ax1.get_ylim()
    x1limits = ax1.get_xlim()
    y2limits = ax2.get_ylim()
    x2limits = ax2.get_xlim()

    max_len = max(y1limits[1], x1limits[1], y2limits[1], x2limits[1])

    plt.xlim(0, max_len)
    plt.ylim(0, max_len)

    ax1.set_ylabel(f"{unit} - NOV")
    ax1.set_xlabel(f"{unit} - FAM")
    ax2.set_xlabel(f"{unit} - FAM")

    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/auc_rate/{action}scatter{group}.svg', format='svg')


    mice_id = ['200', '201', '202', '203', '204', '205' , '211', '212', '213', '214']
    print(fam_a_means)
    fam = np.mean(np.vstack([fam_a_means, fam_b_means]), axis=0)
    nov = np.mean(np.vstack([nov_a_means, nov_b_means]), axis=0)

    df = pd.DataFrame({
        unit: np.concatenate([fam, nov]),
        "Condition": ["FAM"] * len(fam) + ["NOV"] * len(nov),
        "Mouse": mice_id * 2
    })
    fig, ax = plt.subplots(figsize=(3, 4))

    sns.barplot(
        data=df, x="Condition", y=unit, ax=ax,
        capsize=0.3, edgecolor="black", lw=1.5,
        errwidth=1.5, palette="pastel", estimator=np.mean, errorbar="se"
    )

    # Use stripplot instead of swarmplot for cleaner jittered points
    strip = sns.stripplot(
        data=df, x="Condition", y=unit, ax=ax,
        color="black", size=5, jitter=True, alpha=0.7
    )


    # Add error bars with a different color (dark gray)
    for i, cond in enumerate(["FAM", "NOV"]):
        vals = df[df["Condition"] == cond][unit].values
        mean = np.nanmean(vals)
        err = np.nanstd(vals, ddof=1) / np.sqrt(np.sum(~np.isnan(vals)))
        ax.errorbar(
            i, mean, yerr=err, color="dimgray", capsize=6, fmt='none', zorder=10, lw=2
        )

    for i in range(len(mice_id)):
        mouse = mice_id[i]
        x = df[(df['Mouse'] == mouse) & (df['Condition'] == "FAM")][unit].values
        y = df[(df['Mouse'] == mouse) & (df['Condition'] == "NOV")][unit].values
        if len(x) > 0 and len(y) > 0:
            ax.plot(["FAM", "NOV"], [x, y], color="black", alpha=0.6, zorder=9)
    
#     sns.lineplot(data=df, x="Condition", y="AUC", hue="Mouse", marker='o', sort=False, legend=False, ax=ax, palette='rocket')

    for axis in ['bottom', 'left']:
        ax.spines[axis].set_linewidth(2.5)
        ax.spines[axis].set_color('0.2')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Improved axis labels and title
    ax.set_title(f"{group} {unit} Comparison", fontsize=16, color="0.2")
    ax.set_xlabel("Condition", fontsize=14, color="0.2")
    ax.set_ylabel(unit, fontsize=14, color="0.2")
    ax.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=15, fontsize=12, weight="bold", color="0.2")
    plt.yticks(fontsize=12, weight="bold", color="0.2")

    plt.ylim(top=4)
    ax.tick_params(width=2.5, color='0.2')
    
    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/auc_rate/{group}.svg', format='svg')

 


    # print(f"Current y-axis limits: {ylimits}")
    # plt.show()
    # exit()


    # fam_all = np.concatenate(all[group]["FAM"]['All'])
    # print(fam_all)
    # exit()
    # print(len(all[group]["FAM"]['All']))
    # print(len(all[group]["NOV"]['All']))
    # fam = all[group]["FAM"]['All']
    # print(fam)
    # nov = all[group]["NOV"]['All']
    # fig, ax = plt.subplots(figsize=(5, 4))

    # ax.axline((0, 0), slope=1, color='red', linestyle='--', )

    # min_len = min(len(fam), len(nov))
    # ax.scatter(fam[:min_len], nov[:min_len], s=50, color='blue', edgecolor='k', alpha=0.7)

    # ylimits = ax.get_ylim()
    # print(f"Current y-axis limits: {ylimits}")
    
    # plt.show()

    # exit()
    # if epoch == "interaction":

    #     fam_a = np.array(all[group]["FAM"]['A']).flatten()
    #     fam_b = np.array(all[group]["FAM"]['B']).flatten()
    #     nov_a = np.array(all[group]["NOV"]['A']).flatten()
    #     nov_b = np.array(all[group]["NOV"]['B']).flatten()

    #     fam = np.mean(np.vstack([fam_a, fam_b]), axis=0)
    #     nov = np.mean(np.vstack([nov_a, nov_b]), axis=0)

    # elif epoch == "peri-event":


    #     fam = all[group]["FAM"]['All']
    #     print(fam)
    #     nov = all[group]["NOV"]['All']


    # fig, ax = plt.subplots(figsize=(5, 4))

    # ax.axline((0, 0), slope=1, color='red', linestyle='--', )


    # print(f"fam: {fam}\n")
    # print(f"nov {nov}")
    # ax.scatter(fam, nov)

    # plt.xlim(right=4)
    # plt.ylim(top=4)



def plot_dual_trace(traces_a, traces_b, group, condition, zscore, trunc_time, title="", mouse="", save_path=None):
    """
    Plots the aligned calcium traces (z-score or df/f) over time for Object A and Object B.
    A vertical dashed line is drawn at 0 seconds to indicate the nose poke event.
    
    Returns:
    - mean_A: The averaged trace for Object A.
    - mean_B: The averaged trace for Object B.
    - time_axis: The generated time array for the x-axis.
    """
    # use the total seconds wanted and then find the total seconds
    time_interval=0.01660136795
    # finds the amount of values using the rate of collection
    truncate = round(trunc_time / time_interval) 

    mean_A = traces_a.mean(axis=1)[:truncate] 
    mean_B = traces_b.mean(axis=1)[:truncate] 
    # 10 seconds before interaction
    start_time = -10
    # we're converting the rate based iteration of the signals to now seconds
    time_axis = np.arange(start_time, start_time + len(mean_A) * time_interval, time_interval)[:truncate]

    df = pd.DataFrame({
        'time (s)': time_axis,
        'Object A': mean_A,
        'Object B': mean_B
    })

    y_value_name = 'zscore' if zscore else 'df/f'
    # Prepare DataFrame in long format for seaborn
    df_long = df.melt(id_vars='time (s)', value_vars=['Object A', 'Object B'], var_name='Object', value_name=y_value_name)

    

    plt.figure(figsize=(8,6), layout="constrained")
    sns.lineplot(data=df_long, x='time (s)', y=y_value_name, hue='Object', palette={'Object A': 'blue', 'Object B': 'red'}, linewidth=1.5)
    
    plt.axvline(0, color='k', linestyle='--')
    plt.ylim(-0.75,2)
    ax = plt.gca()

    # y=1.05 puts it just above the top edge
    plt.text(0, 1.01, 'nose poke', color='black', 
            ha='center', va='bottom', transform=ax.get_xaxis_transform())
    plt.title(f'{title} | Mouse: {mouse} | Group: {group} | Condition: {condition}', y=1.05)
    ax.spines[['top', 'right']].set_visible(False)

    if save_path:
        df_long.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/zscorewithnewmice/new{group}.csv', index=False)
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/zscorewithnewmice/{mouse}{group}{condition}.svg', format='svg')
 

    return mean_A, mean_B, time_axis

def plot_combined_traces(trace, group, time_axis, zscore, action, size="", save_path=None, singular=None):
    """
    Plot z-score or df/f of the trace when aligned at the entrance or exit based on time axis.

    Parameters:
    - trace: time and signal of all the total values
    - group: group name (e.g., 'NOR')
    - time_axis: time axis for the x-axis
    - zscore: boolean indicating whether to plot z-score or df/f
    - action: 'entrance' or 'exit' to indicate the type of action
    - size: size of the figure, default is empty string which uses default size
    - save_path: optional path to save figure
    """
    
    """
    Make the function versatile so that if we just want to have nov for example it is able to do that
    """

    if singular == True: # in the case that singular does get called 

        value = np.mean((np.array(trace[group]["NOV"]['A']) + np.array(trace[group]["NOV"]['B'])) / 2, axis=0)
        val_sem = sem((np.array(trace[group]["NOV"]['A']) + np.array(trace[group]["NOV"]['B'])) / 2, axis=0)

        if singular == "NOV":
            color_association = 'red'
        else:
            color_association = 'blue'

        df = pd.DataFrame({
            'time (s)': time_axis,
            'NOV': nov,
        })

        fig, ax = plt.subplots(figsize=size)

        df_long = df.melt(id_vars='time (s)', value_vars=[singular], var_name='Condition', value_name='df/f')

        ax.plot(time_axis, fam, label=singular, color='blue')
        ax.fill_between(time_axis, fam - fam_sem, fam + fam_sem, color='blue', alpha=0.2)



    else: 
        nov = np.mean((np.array(trace[group]["NOV"]['A']) + np.array(trace[group]["NOV"]['B'])) / 2, axis=0)
        fam = np.mean((np.array(trace[group]["FAM"]['A']) + np.array(trace[group]["FAM"]['B'])) / 2, axis=0)

        nov_sem = sem((np.array(trace[group]["NOV"]['A']) + np.array(trace[group]["NOV"]['B'])) / 2, axis=0)
        fam_sem = sem((np.array(trace[group]["FAM"]['A']) + np.array(trace[group]["FAM"]['B'])) / 2, axis=0)    
        
        value = np.concatenate([fam, nov])
        condition = (["FAM"] * len(fam) + ["NOV"] * len(nov))

        df = pd.DataFrame({
            'time (s)': time_axis,
            'NOV': nov,
            'FAM': fam
        })
        
        fig, ax = plt.subplots(figsize=size)
        
        df_long = df.melt(id_vars='time (s)', value_vars=['FAM', 'NOV'], var_name='Condition', value_name='df/f')
        
        if False:
            df_long.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOLfixed/zscorewithnewmice/new{group}.csv', index=False)
    

        ax.plot(time_axis, fam, label='FAM', color='blue')
        ax.fill_between(time_axis, fam - fam_sem, fam + fam_sem, color='blue', alpha=0.2)

        ax.plot(time_axis, nov, label='NOV', color='red')
        ax.fill_between(time_axis, nov - nov_sem, nov + nov_sem, color='red', alpha=0.2)

    ax.axvline(0, color='k', linestyle='--')
    ax.text(0, 1.01, 'nose poke', color='black', weight='bold', 
            ha='center', va='bottom', transform=ax.get_xaxis_transform())

    ax.spines[['top', 'right']].set_visible(False)
    plt.xticks(weight = 'bold')
    plt.yticks(weight = 'bold')
    
    ax.set_xlabel('Time (s)', weight='bold')
    if action:
        input = "Entrance"
    else:
        input = "Exit"

    if zscore:
        plt.ylim(-0.2, 1.2)
        ax.set_ylabel('z-score', weight = 'bold')
        plt.title(f'{input} Avg: zscore | Group: {group}',  y=1.05)
    else:

        plt.ylabel('df/f')
        plt.title(f'{input} Avg: df/f A & B | Group: {group}')
    plt.legend()
    plt.tight_layout()

    if save_path and zscore:
        
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOLfixed/zscorewithnewmice/new{action}{group}{size}.svg', format='svg')
 
def plot_interval_auc(trace, group, time_axis, zscore, action, interval=2.5, save_path=None):
    """
    Calculates and plots the AUC for every `interval` seconds for FAM and NOV conditions.
    """
    
    # Define bins
    t_min = time_axis[0]
    t_max = time_axis[-1]
    
    # Ensure we cover the whole range
    bins = np.arange(t_min, t_max + 0.001, interval)
    
    plot_data = []
    
    for condition in ['FAM', 'NOV']:
        # Get traces (list of arrays)
        if 'A' not in trace[group][condition] or 'B' not in trace[group][condition]:
             continue

        traces_a = np.array(trace[group][condition]['A'])
        traces_b = np.array(trace[group][condition]['B'])
        
        # Average A and B per mouse -> (n_mice, n_timepoints)
        if len(traces_a) == 0:
            continue
            
        avg_traces = (traces_a + traces_b) / 2
        
        # Iterate through bins
        for i in range(len(bins) - 1):
            b_start = bins[i]
            b_end = bins[i+1]
            
            # Mask for time points in this bin
            mask = (time_axis >= b_start) & (time_axis < b_end)
            
            if not np.any(mask):
                continue
                
            # Calculate AUC using trapezoidal rule
            # axis=1 integrates along time
            aucs = np.trapz(avg_traces[:, mask], x=time_axis[mask], axis=1)
            
            # Append to list
            for mouse_idx, val in enumerate(aucs):
                plot_data.append({
                    'Condition': condition,
                    'Time Bin': b_start + (interval / 2), # Use center for plotting x
                    'Bin Label': f"{b_start:.1f} to {b_end:.1f}",
                    'AUC': val,
                    'Mouse': mouse_idx
                })
                
    df = pd.DataFrame(plot_data)
    
    if df.empty:
        print("No data for interval AUC.")
        return

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    sns.lineplot(
        data=df, 
        x='Time Bin', 
        y='AUC', 
        hue='Condition', 
        palette={'FAM': 'blue', 'NOV': 'red'},
        marker='o',
        err_style='band',
        ax=ax
    )
    
    action_str = "Entrance" if action else "Exit"
    ax.set_title(f'{action_str} AUC per {interval}s Interval | {group}')
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('AUC')
    
    # Add vertical line at 0 if within range
    if t_min <= 0 <= t_max:
        ax.axvline(0, color='k', linestyle='--')
        ax.text(0, ax.get_ylim()[1], 'nose poke', color='black', weight='bold', ha='center', va='bottom')
        
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout()
    
    if save_path:
        # Construct path similar to others
        action_file = "entrance" if action else "exit"
        
        # Using the same directory as plot_combined_traces
        save_file = f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/zscorewithnewmice/interval_auc_{group}_{action_file}_{interval}s.svg'
        csv_file = f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/zscorewithnewmice/interval_auc_{group}_{action_file}_{interval}s.csv'
        
        plt.savefig(save_file, format='svg')
        df.to_csv(csv_file, index=False)

def save_traces_per_mouse(trace, group, time_axis, mouse_ids, zscore, action, save_path=None):
    """
    Saves the peri-event traces for each mouse to a single CSV file per group.

    """

    #we're checking to see if its a df/f / zscore trace or its event related trace
    is_timeseries = isinstance(trace[group]["FAM"]['A'][0], pd.Series)
    t_check = 0

    # --- Data Consistency Check ---
    if is_timeseries:
        fam_traces_a = trace[group]["FAM"]['A']
        fam_traces_b = trace[group]["FAM"]['B']
        nov_traces_a = trace[group]["NOV"]['A']
        nov_traces_b = trace[group]["NOV"]['B']


        fam_data = {'time_s': time_axis, 'condition': 'FAM'}
        nov_data = {'time_s': time_axis, 'condition': 'NOV'}

    else:
        fam_traces_a = trace[group]["FAM"]['All_a']
        fam_traces_b = trace[group]["FAM"]['All_b']
        nov_traces_a = trace[group]["NOV"]['All_a']
        nov_traces_b = trace[group]["NOV"]['All_b']

    num_mice = len(mouse_ids)
    if not (len(fam_traces_a) == num_mice and len(nov_traces_a) == num_mice):
        print(f"Warning: Mismatch in number of sessions for group {group}. Cannot reliably save per-mouse data.")
        return
 
    # --- Prepare Data for DataFrame ---
    # Initialize dictionaries to hold the data for FAM and NOV conditions

 
    if is_timeseries:
    # --- Continuous (aligned) case ---
        for i, mouse_id in enumerate(mouse_ids):
            fam_trace = (fam_traces_a[i] + fam_traces_b[i]) / 2
            nov_trace = (nov_traces_a[i] + nov_traces_b[i]) / 2

            fam_data[mouse_id] = fam_trace
            nov_data[mouse_id] = nov_trace

        df_fam = pd.DataFrame(fam_data)
        df_nov = pd.DataFrame(nov_data)

    else:
        # --- Event-based (unaligned) case ---
        fam_dfs = []
        nov_dfs = []

        for i, mouse_id in enumerate(mouse_ids):
            fam_trace = (fam_traces_a[i] + fam_traces_b[i]) / 2
            nov_trace = (nov_traces_a[i] + nov_traces_b[i]) / 2

            # Ensure we have pandas Series with indices as times
            if not isinstance(fam_trace, pd.Series):
                fam_trace = pd.Series(fam_trace)
            if not isinstance(nov_trace, pd.Series):
                nov_trace = pd.Series(nov_trace)

            fam_df = pd.DataFrame({'time_s': fam_trace.index, mouse_id: fam_trace.values})
            nov_df = pd.DataFrame({'time_s': nov_trace.index, mouse_id: nov_trace.values})

            fam_dfs.append(fam_df)
            nov_dfs.append(nov_df)

        # Merge all mice by 'time_s' (outer join to preserve all timestamps)
        df_fam = fam_dfs[0]
        for df in fam_dfs[1:]:
            df_fam = pd.merge(df_fam, df, on='time_s', how='outer')
        df_fam['condition'] = 'FAM'

        df_nov = nov_dfs[0]
        for df in nov_dfs[1:]:
            df_nov = pd.merge(df_nov, df, on='time_s', how='outer')
        df_nov['condition'] = 'NOV'

    # --- Combine both conditions ---
    final_df = pd.concat([df_fam, df_nov], ignore_index=True)

    print(final_df.head())

    # --- Save ---
    action_str = "entrance" if action else "exit"
    if save_path:
        output_path = f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOLfixed/zscorewithnewmice/{group}_{action_str}_of_mouse.csv'
        final_df.to_csv(output_path, index=False)
    
def plot_auc_bar(all_aucs, group, condition, action="", title="", ylabel="AUC", save_path=None):

    
    """
    Plot bar graph of AUC means with SEM error bars for Object A, B, and A+B combined.
    Parameters:
    - all_aucs: dict structured like all_aucs[group][condition]['A' or 'B']
    - group: group name (e.g., 'NOR')
    - condition: condition name (e.g., 'FAM')
    - title: plot title
    - ylabel: y-axis label
    - save_path: optional path to save figure
    """
    # Get AUCs for A and B
    # Get AUCs for A and B
    

    aucs_a = np.array(all_aucs[group][condition]['A']).flatten()
    aucs_b = np.array(all_aucs[group][condition]['B']).flatten()

    # Ensure equal length or pad with NaNs
    min_len = min(len(aucs_a), len(aucs_b))
    aucs_a = aucs_a[:min_len]
    aucs_b = aucs_b[:min_len]

    # Compute A+B per session (mean of each pair)
    aucs_ab = (aucs_a + aucs_b) / 2
    # Stack for easier mean/SEM calculation
    auc_data = np.array([aucs_a, aucs_b, aucs_ab])
    labels = ["Object A", "Object B", "A + B"]


    means = np.nanmean(auc_data, axis=1)

    sems = np.nanstd(auc_data, axis=1, ddof=1) / np.sqrt(np.sum(~np.isnan(auc_data), axis=1))

    fig, ax = plt.subplots(figsize=(5, 4))

    ax.bar(labels, means, yerr=sems, capsize=5, color=["skyblue", "salmon", "gray"])
    ax.set_ylabel(ylabel)
    ax.set_title(title if title else f"{group} - {condition} AUC")
    ax.spines[['top', 'right']].set_visible(False)
    plt.tight_layout() 
    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/images/events/aucs{action}{group}{condition}.png')

def plot_total_events(all_events, group="", condition="", action="", title="", save_path=None):
    """
    Plots a simple bar chart comparing the total number of events for Object A, Object B, 
    and the combined sum (A+B) during a specific condition.
    """
    labels = ['Object A', 'Object B', 'Both']
    
    totala = np.mean(all_events[group][condition]['A'])
    totalb = np.mean(all_events[group][condition]['B'])
    total = totala + totalb
    counts = [
        totala, totalb, total
    ]


    fig, ax = plt.subplots(figsize=(5, 4))
    bars = ax.bar(labels, counts, color=['skyblue', 'salmon'])

    ax.set_ylabel('Total Number of Events')
    ax.set_title(title)
    ax.bar_label(bars)
    plt.tight_layout()


    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/events/total_events{action}{group}{condition}.png')

def plot_events_per_second(all_rates, group="", condition="", action="",title="", save_path=None):
    """
    Plots a bar chart showing the mean events per minute for Object A, Object B, 
    and the combined average of both objects.
    """
    labels = ['Object A', 'Object B', "A + B"]
    mean_a = np.mean(all_rates[group][condition]['A'])
    mean_b = np.mean(all_rates[group][condition]['B'])
    mean_ab = np.mean([mean_a, mean_b])

    counts = [mean_a, mean_b, mean_ab]

    fig, ax = plt.subplots(figsize=(5,4))

    bars = ax.bar(labels, counts, color=['skyblue', 'salmon'])

    ax.set_ylabel('Event Rate')
    ax.set_title(f' Events per Minute{group} - {condition}')
    ax.bar_label(bars)
    plt.tight_layout()

    # fig, axs = plt.subplots(3, figsize=(5, 4))
    # axs[0].bar(labels[0], counts[0], color=['skyblue', 'salmon'])
    # axs[1].bar(labels[1], counts[1], color=['skyblue', 'salmon'])
    # axs[2].bar(labels[2], counts[2], color=['skyblue', 'salmon'])

    # for ax in axs.flat:

    #     ax.set_ylabel('Events Per Minute')
    #     ax.set_title(title)

    # plt.tight_layout()


    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/images/events/rate{action}{group}{condition}.png')

#not using these ^^


def plot_combined_auc(all_aucs, group, condition, title="", save_path=None):
    """
    Plots a comprehensive bar chart with an overlaid swarmplot representing AUC data.
    The data points correspond to specific mice, and lines connect the paired FAM and NOV 
    measurements for the same mouse, allowing clear visualization of individual changes.
    """
    combined = True
    fam_a = np.array(all_aucs[group]["FAM"]['A']).flatten()
    fam_b = np.array(all_aucs[group]["FAM"]['B']).flatten()
    nov_a = np.array(all_aucs[group]["NOV"]['A']).flatten()
    nov_b = np.array(all_aucs[group]["NOV"]['B']).flatten()

    print(f"nov_b: {nov_b}")
    if combined:
        # want to find out where each of the mices values are so we can compare the different familiarity and novelty
        mice_id = ['200', '201', '202', '203', '204', '205']

        fam = np.mean(np.vstack([fam_a, fam_b]), axis=0)
        nov = np.mean(np.vstack([nov_a, nov_b]), axis=0)

        df = pd.DataFrame({
            "AUC": np.concatenate([fam, nov]),
            "Condition": ["FAM"] * len(fam) + ["NOV"] * len(nov),
            "Mouse": mice_id * 2
        })
        fig, ax = plt.subplots(figsize=(3, 4))

        sns.barplot(data=df, x="Condition", y="AUC", ax=ax, capsize = 0.5, edgecolor = '0.2', lw= 2.5, errwidth = 2.5, palette = [ 'crimson', 'mistyrose' ], estimator=np.mean, errorbar='se')

        # Draw swarmplot
        swarm = sns.swarmplot(data=df, x="Condition", y="AUC", s=8, ax=ax, palette=["lightcoral", "lightpink"])
    

        # Add outlines to each point
        for coll in swarm.collections:
            coll.set_edgecolor('0.2')
            coll.set_linewidth(1.0)

        for i in range(len(mice_id)):  
            mouse = mice_id[i]

            x = df[(df['Mouse'] == mouse) & (df['Condition'] == "FAM")]['AUC'].values
            y = df[(df['Mouse'] == mouse) & (df['Condition'] == "NOV")]['AUC'].values
            
            if len(x) > 0 and len(y) > 0:
                ax.plot(["FAM", "NOV"], [x, y], color="black", alpha=0.6)

                # we're plotting a line between FAM and NOV of the same mouse ^
        
   #     sns.lineplot(data=df, x="Condition", y="AUC", hue="Mouse", marker='o', sort=False, legend=False, ax=ax, palette='rocket')

        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(size = 14, ha = 'center', weight = 'bold', color = '0.2')
        plt.ylim(top=4)
        plt.yticks(size = 14, weight = 'bold', color = '0.2')

        ax.tick_params(width = 2.5, color = '0.2')

        plt.ylabel('AUC', size = 14, weight = 'bold', color = '0.2')   
        
    else:
        aucs = np.concatenate([fam_a, fam_b, nov_a, nov_b])
        condition = (["FAM"] * len(fam_a) + ["FAM"] * len(fam_b) +
                    ["NOV"] * len(nov_a) + ["NOV"] * len(nov_b))
        obj = (["A"] * len(fam_a) + ["B"] * len(fam_b) +
            ["A"] * len(nov_a) + ["B"] * len(nov_b))

        df = pd.DataFrame({
            "AUC": aucs,
            "Condition": condition,
            "Object": obj
        })
        plt.figure(figsize=(5, 4))

        ax = sns.barplot(data=df, x="Condition", y="AUC", capsize = 0.5, edgecolor = '0.2', lw= 2.5, errwidth = 2.5, palette = [ 'crimson', 'mistyrose' ], errcolor = '0.2', hue = "Object", dodge = True)

        kwargs = {'edgecolor': '0.2', 'linewidth': 2.5, 'fc': 'none'}

        ax = sns.swarmplot(data = df, x = "Condition", y = "AUC", s = 8, **kwargs, color = '0.2', dodge = True)



        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(size = 14, ha = 'center', weight = 'bold', color = '0.2')
        plt.yticks(size = 14, weight = 'bold', color = '0.2')

        ax.tick_params(width = 2.5, color = '0.2')

        plt.ylabel('AUC', size = 14, weight = 'bold', color = '0.2')
    plt.xlabel('')
    if title:
        ax.set_title(title, fontsize=14, weight='bold', color='0.2')
    plt.tight_layout()
    if save_path:
        df.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/AUC/{group}.csv', index=True)
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/AUC/{group}{combined}.svg', format='svg')

def plot_combined_rate(all_rates, group, condition, action="", title="", save_path=None):


    combined = True
    fam_a = np.array(all_rates[group]["FAM"]['A']).flatten()
    fam_b = np.array(all_rates[group]["FAM"]['B']).flatten()
    nov_a = np.array(all_rates[group]["NOV"]['A']).flatten()
    nov_b = np.array(all_rates[group]["NOV"]['B']).flatten()

    print(f"nov_b: {nov_b}")


    if combined:
        mice_id = ['200', '201', '202', '203', '204', '205']

        # Compute average per mouse between A and B
        fam = np.mean(np.vstack([fam_a, fam_b]), axis=0)
        nov = np.mean(np.vstack([nov_a, nov_b]), axis=0)

        df = pd.DataFrame({
            "Rate": np.concatenate([fam, nov]),
            "Condition": ["FAM"] * len(fam) + ["NOV"] * len(nov),
            "Mouse": mice_id * 2
        })


        fig, ax = plt.subplots(figsize=(3, 4))

        sns.barplot(data=df, x="Condition", y="Rate", ax=ax,
                    capsize=0.5, edgecolor='0.2', lw=2.5,
                    errwidth=2.5, palette=['crimson', 'mistyrose'], estimator=np.mean, errorbar='se')

        swarm = sns.stripplot(data=df, x="Condition", y="Rate", s=8,
                              ax=ax, palette=['lightcoral', 'lightpink'])
        
        for coll in swarm.collections:
            coll.set_edgecolor('0.2')
            coll.set_linewidth(1.0)


        for i in range(len(mice_id)):
            mouse = mice_id[i]
            x = df[(df['Mouse'] == mouse) & (df['Condition'] == "FAM")]['Rate'].values
            y = df[(df['Mouse'] == mouse) & (df['Condition'] == "NOV")]['Rate'].values
            
            if len(x) > 0 and len(y) > 0:
                ax.plot(["FAM", "NOV"], [x, y], color="black", alpha=0.6)
        
   #     sns.lineplot(data=df, x="Condition", y="Rate", hue="Mouse", marker='o', sort=False, legend=False, ax=ax, palette='rocket') 


        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(size=14, ha='center', weight='bold', color='0.2')
        plt.ylim(top=3.5)
        plt.yticks(size=14, weight='bold', color='0.2')
        
        ax.tick_params(width=2.5, color='0.2')

        plt.ylabel('Events per Minute', size=14, weight='bold', color='0.2')

        plt.xlabel('')


    else:
        rate = np.concatenate([fam_a, fam_b, nov_a, nov_b])
        condition = (["FAM"] * len(fam_a) + ["FAM"] * len(fam_b) +
                    ["NOV"] * len(nov_a) + ["NOV"] * len(nov_b))
        obj = (["A"] * len(fam_a) + ["B"] * len(fam_b) +
            ["A"] * len(nov_a) + ["B"] * len(nov_b))

        df = pd.DataFrame({
            "Rate": rate,
            "Condition": condition,
            "Object": obj
        })
        plt.figure(figsize=(5, 4))

        ax = sns.barplot(data=df, x="Condition", y="Rate", capsize = 0.5, edgecolor = '0.2', lw= 2.5, errwidth = 2.5, palette = [ 'crimson', 'mistyrose' ], errcolor = '0.2', hue = "Object", dodge = True)

        kwargs = {'edgecolor': '0.2', 'linewidth': 2.5, 'fc': 'none'}

        ax = sns.swarmplot(data = df, x = "Condition", y = "Rate", s = 8, **kwargs, color = '0.2', dodge = True)



        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(size = 14, ha = 'center', weight = 'bold', color = '0.2')
        plt.yticks(size = 14, weight = 'bold', color = '0.2')

        ax.tick_params(width = 2.5, color = '0.2')

        plt.ylabel('Events per Minute', size = 14, weight = 'bold', color = '0.2')

    plt.tight_layout()
    if title:
        ax.set_title(title, fontsize=14, weight='bold', color='0.2')
    plt.xlabel('')
    plt.tight_layout()
    if save_path:
        df.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/rate/{group}.csv', index=True)
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/rate/mice{group}{combined}.svg', format='svg')

def plot_combined_events(all_events, group, condition, title="", save_path=None):
    
    combined = True
    fam_a = np.array(all_events[group]["FAM"]['A']).flatten()
    fam_b = np.array(all_events[group]["FAM"]['B']).flatten()
    nov_a = np.array(all_events[group]["NOV"]['A']).flatten()
    nov_b = np.array(all_events[group]["NOV"]['B']).flatten()

    print(f"nov_b: {nov_b}")
    if combined:

        mice_id = ['200', '201', '202', '203', '204', '205']

        fam = np.mean(np.vstack([fam_a, fam_b]), axis=0)
        nov = np.mean(np.vstack([nov_a, nov_b]), axis=0)

        df = pd.DataFrame({
            "Events": np.concatenate([fam, nov]),
            "Condition": ["FAM"] * len(fam) + ["NOV"] * len(nov),
            "Mouse": mice_id * 2
        })

        fig, ax = plt.subplots(figsize=(3, 4))

        sns.barplot(data=df, x="Condition", y="Events", ax=ax,
                    capsize=0.5, edgecolor='0.2', lw=2.5,
                    errwidth=2.5, palette=['crimson', 'mistyrose'], estimator=np.mean, errorbar='se')

        swarm = sns.swarmplot(data=df, x="Condition", y="Events", s=8,
                              ax=ax, palette=['lightcoral', 'lightpink'])
        for coll in swarm.collections:
            coll.set_edgecolor('0.2')
            coll.set_linewidth(1.0)

        for i in range(len(mice_id)):
            mouse = mice_id[i]
            x = df[(df['Mouse'] == mouse) & (df['Condition'] == "FAM")]['Events'].values
            y = df[(df['Mouse'] == mouse) & (df['Condition'] == "NOV")]['Events'].values
            
            if len(x) > 0 and len(y) > 0:
                ax.plot(["FAM", "NOV"], [x, y], color="black", alpha=0.6)
        
   #     sns.lineplot(data=df, x="Condition", y="Events", hue="Mouse", marker='o', sort=False, legend=False, ax=ax, palette='rocket')

        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(size=14, ha='center', weight='bold', color='0.2')
        plt.ylim(top=45)
        plt.yticks(size=14, weight='bold', color='0.2')
        plt.ylabel("Events", size=14, weight='bold', color='0.2')
        
        ax.tick_params(width=2.5, color='0.2')

    else:
        events = np.concatenate([fam_a, fam_b, nov_a, nov_b])
        condition = (["FAM"] * len(fam_a) + ["FAM"] * len(fam_b) +
                    ["NOV"] * len(nov_a) + ["NOV"] * len(nov_b))
        obj = (["A"] * len(fam_a) + ["B"] * len(fam_b) +
            ["A"] * len(nov_a) + ["B"] * len(nov_b))

        df = pd.DataFrame({
            "Events": events,
            "Condition": condition,
            "Object": obj
        })
        plt.figure(figsize=(5, 4))

        ax = sns.barplot(data=df, x="Condition", y="Events", capsize = 0.5, edgecolor = '0.2', lw= 2.5, errwidth = 2.5, palette = [ 'crimson', 'mistyrose' ], errcolor = '0.2', hue = "Object", dodge = True)

        kwargs = {'edgecolor': '0.2', 'linewidth': 2.5, 'fc': 'none'}

        ax = sns.swarmplot(data = df, x = "Condition", y = "Events", s = 8, **kwargs, color = '0.2', dodge = True)



        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(size = 14, ha = 'center', weight = 'bold', color = '0.2')
        plt.yticks(size = 14, weight = 'bold', color = '0.2')

        ax.tick_params(width = 2.5, color = '0.2')

        plt.ylabel('Events', size = 14, weight = 'bold', color = '0.2')
    if title:
            ax.set_title(title, fontsize=14, weight='bold', color='0.2')
    plt.xlabel('')
    plt.tight_layout()
    if save_path:
        df.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/events/{group}.csv', index=True)
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/events/{group}{combined}.svg', format='svg')

def plot_combined(all, event_type, max_value, group, condition, action="", title="", save_path=None):

    combined = True
    fam_a = np.array(all[group]["FAM"]['A']).flatten()
    fam_b = np.array(all[group]["FAM"]['B']).flatten()
    nov_a = np.array(all[group]["NOV"]['A']).flatten()
    nov_b = np.array(all[group]["NOV"]['B']).flatten()

    print(f"nov_b: {nov_b}")
    if combined:

        mice_id = ['200', '201', '202', '203', '204', '205']

        fam = np.mean(np.vstack([fam_a, fam_b]), axis=0)
        nov = np.mean(np.vstack([nov_a, nov_b]), axis=0)

        df = pd.DataFrame({
            event_type: np.concatenate([fam, nov]),
            "Condition": ["FAM"] * len(fam) + ["NOV"] * len(nov),
            "Mouse": mice_id * 2
        })
        fig, ax = plt.subplots(figsize=(3, 4))

        sns.barplot(data=df, x="Condition", y=event_type, ax=ax, capsize = 0.5, edgecolor = '0.2', lw= 2.5, errwidth = 2.5, palette = [ 'crimson', 'mistyrose' ], estimator=np.mean, errorbar='se')

        # Draw swarmplot
        swarm = sns.swarmplot(data=df, x="Condition", y=event_type, s=8, ax=ax, palette=["lightcoral", "lightpink"])
    

        # Add outlines to each point
        for coll in swarm.collections:
            coll.set_edgecolor('0.2')
            coll.set_linewidth(1.0)

        for i in range(len(mice_id)):
            mouse = mice_id[i]
            x = df[(df['Mouse'] == mouse) & (df['Condition'] == "FAM")][event_type].values
            y = df[(df['Mouse'] == mouse) & (df['Condition'] == "NOV")][event_type].values
            
            if len(x) > 0 and len(y) > 0:
                ax.plot(["FAM", "NOV"], [x, y], color="black", alpha=0.6)
        
   #     sns.lineplot(data=df, x="Condition", y="AUC", hue="Mouse", marker='o', sort=False, legend=False, ax=ax, palette='rocket')

        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(size = 14, ha = 'center', weight = 'bold', color = '0.2')
        plt.ylim(top=max_value)
        plt.yticks(size = 14, weight = 'bold', color = '0.2')

        ax.tick_params(width = 2.5, color = '0.2')

        plt.ylabel(event_type, size = 14, weight = 'bold', color = '0.2')   
        
    else:
        aucs = np.concatenate([fam_a, fam_b, nov_a, nov_b])
        condition = (["FAM"] * len(fam_a) + ["FAM"] * len(fam_b) +
                    ["NOV"] * len(nov_a) + ["NOV"] * len(nov_b))
        obj = (["A"] * len(fam_a) + ["B"] * len(fam_b) +
            ["A"] * len(nov_a) + ["B"] * len(nov_b))

        df = pd.DataFrame({
            "AUC": aucs,
            "Condition": condition,
            "Object": obj
        })
        plt.figure(figsize=(5, 4))

        ax = sns.barplot(data=df, x="Condition", y=event_type, capsize = 0.5, edgecolor = '0.2', lw= 2.5, errwidth = 2.5, palette = [ 'crimson', 'mistyrose' ], errcolor = '0.2', hue = "Object", dodge = True)

        kwargs = {'edgecolor': '0.2', 'linewidth': 2.5, 'fc': 'none'}

        ax = sns.swarmplot(data = df, x = "Condition", y = event_type, s = 8, **kwargs, color = '0.2', dodge = True)



        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(size = 14, ha = 'center', weight = 'bold', color = '0.2')
        plt.yticks(size = 14, weight = 'bold', color = '0.2')

        ax.tick_params(width = 2.5, color = '0.2')

        plt.ylabel(event_type, size = 14, weight = 'bold', color = '0.2')
    plt.xlabel('')
    if title:
        ax.set_title(title, fontsize=14, weight='bold', color='0.2')
    plt.tight_layout()
    if save_path:
        df.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/{event_type}/{group}.csv', index=True)
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/{event_type}/{group}{combined}.svg', format='svg')

def plot_combines(all, event_type, max_value, group, condition, mouse_ids, action="", title="", save_path=None, normalize=False, combined=True):
    """
    Plots a summary metric (e.g., AUC, amplitude, duration) comparing Familiar (FAM) 
    and Novel (NOV) conditions. Can plot both objects combined or separated.
    
    Parameters:
    - all: Nested dictionary containing the data extracted from sessions.
    - event_type: String label for the metric (e.g., "AUC", "amplitude") for the y-axis.
    - max_value: Optional maximum y-axis limit.
    - group: Group name (e.g., 'NOR', 'NOL').
    - condition: Specific condition label (not used for subsetting data in this function, but passed).
    - mouse_ids: List of unique mouse identifiers for pairing lines across conditions.
    - action: Label indicating action context (e.g., 'entrance', 'exit').
    - title: Custom title for the plot.
    - save_path: If True, saves the plot to the disk.
    - normalize: If True, normalizes the data to relative proportions.
    - combined: If True, averages data for Object A and Object B together. If False, plots them separately.
    """

    # Extract all session data arrays for FAM and NOV, Object A and Object B
    fam_per_session_a = all[group]["FAM"]['All_a']
    fam_per_session_b = all[group]["FAM"]['All_b']
    nov_per_session_a = all[group]["NOV"]['All_a']
    nov_per_session_b = all[group]["NOV"]['All_b']

    if combined:
        # Combined plot: For each mouse, calculate the overall mean of Object A and Object B interactions
        fam = [np.nanmean([np.nanmean(fam_per_session_a[i]), np.nanmean(fam_per_session_b[i])]) for i in range(len(fam_per_session_a))]
        nov = [np.nanmean([np.nanmean(nov_per_session_a[i]), np.nanmean(nov_per_session_b[i])]) for i in range(len(nov_per_session_a))]

        # Normalize values as a fraction of the total (FAM + NOV) if requested
        if normalize:
            fam_norm = []
            nov_norm = []
            for i in range(len(fam)):
                total = fam[i] + nov[i]
                fam_norm.append(fam[i] / total if total > 0 else 0)
                nov_norm.append(nov[i] / total if total > 0 else 0)
            
            fam = fam_norm
            nov = nov_norm

        print(mouse_ids)

        # Validate that the amount of data points matches the number of unique mice
        assert len(fam) == len(mouse_ids), f"Mismatch between FAM data points ({len(fam)}) and mouse IDs ({len(mouse_ids)})"
        assert len(nov) == len(mouse_ids), f"Mismatch between NOV data points ({len(nov)}) and mouse IDs ({len(mouse_ids)})"

        # Construct DataFrame for seaborn plotting
        df = pd.DataFrame({
            event_type: np.concatenate([fam, nov]),
            "Condition": ["FAM"] * len(fam) + ["NOV"] * len(nov),
            "Mouse": mouse_ids * 2
        })
        
        # Initialize a small bar plot
        fig, ax = plt.subplots(figsize=(3, 4))

        # 1. Plot average bars with standard error (SE) lines
        sns.barplot(data=df, x="Condition", y=event_type, ax=ax, capsize = 0.5, edgecolor = '0.2', lw= 2.5, errwidth = 2.5, palette = [ 'crimson', 'mistyrose' ], estimator=np.mean, errorbar='se')

        # 2. Overlay individual data points for each mouse
        swarm = sns.swarmplot(data=df, x="Condition", y=event_type, s=8, ax=ax, palette=["lightcoral", "lightpink"])
    

        # Add outlines to each point
        for coll in swarm.collections:
            coll.set_edgecolor('0.2')
            coll.set_linewidth(1.0)

        for i in range(len(mouse_ids)):
            mouse = mouse_ids[i]
            x = df[(df['Mouse'] == mouse) & (df['Condition'] == "FAM")][event_type].values
            y = df[(df['Mouse'] == mouse) & (df['Condition'] == "NOV")][event_type].values
            
            if len(x) > 0 and len(y) > 0:
                ax.plot(["FAM", "NOV"], [x, y], color="black", alpha=0.6)
        
   #     sns.lineplot(data=df, x="Condition", y="AUC", hue="Mouse", marker='o', sort=False, legend=False, ax=ax, palette='rocket')

        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(size=14, ha='center', weight='bold', color='0.2')
        if max_value is not None:
            ax.set_ylim(bottom=0, top=max_value)

        if normalize:
            plt.ylim(0, 1)
        plt.yticks(size = 14, weight = 'bold', color = '0.2')

        ax.tick_params(width = 2.5, color = '0.2')

        plt.ylabel(event_type, size = 14, weight = 'bold', color = '0.2')

    else:
        # Separate logic
        fam_a = [np.nanmean(sess) for sess in fam_per_session_a]
        fam_b = [np.nanmean(sess) for sess in fam_per_session_b]
        nov_a = [np.nanmean(sess) for sess in nov_per_session_a]
        nov_b = [np.nanmean(sess) for sess in nov_per_session_b]

        vals = np.concatenate([fam_a, fam_b, nov_a, nov_b])
        conds = ["FAM"] * (2 * len(mouse_ids)) + ["NOV"] * (2 * len(mouse_ids))
        objs = ["A"] * len(mouse_ids) + ["B"] * len(mouse_ids) + ["A"] * len(mouse_ids) + ["B"] * len(mouse_ids)
        mice = mouse_ids * 4

        df = pd.DataFrame({
            event_type: vals,
            "Condition": conds,
            "Object": objs,
            "Mouse": mice
        })

        fig, ax = plt.subplots(figsize=(5, 4))

        sns.barplot(data=df, x="Condition", y=event_type, hue="Object",
                    palette=['skyblue', 'salmon'], capsize=0.1, errwidth=1.5,
                    edgecolor='0.2', ax=ax, errorbar='se')

        sns.swarmplot(data=df, x="Condition", y=event_type, hue="Object",
                      dodge=True, color='0.2', size=5, ax=ax)

        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        plt.xticks(size=14, ha='center', weight='bold', color='0.2')
        if max_value is not None:
            ax.set_ylim(bottom=0, top=max_value)

        plt.yticks(size = 14, weight = 'bold', color = '0.2')
        ax.tick_params(width = 2.5, color = '0.2')
        plt.ylabel(event_type, size = 14, weight = 'bold', color = '0.2')
        plt.legend(title='Object', loc='upper right')

    if title:
        ax.set_title(title, fontsize=14, weight='bold', color='0.2')
    plt.xlabel('')
    plt.tight_layout()
    if save_path:
        norm_suffix = "_normalized" if normalize else ""
        action_suffix = "entrance" if action else "exit"
        combined_suffix = "_" if combined else "_separate"
        df.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/{event_type}/{group}{norm_suffix}{action_suffix}{combined_suffix}.csv', index=True)
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/{event_type}/{group}{norm_suffix}{action_suffix}{combined_suffix}.svg', format='svg')

  
        
def stationary_locomotion(locomotion_epochs, stationary_epochs, pre_time=10.0, post_time=10.0, time_interval=0.0166):
    """
    Plot mean dF/F traces for locomotion and stationary epochs aligned to transition time.

    Args:
        locomotion_epochs (list of pd.DataFrame): Epochs around locomotion onsets (output from locomotion_epochs()).
        stationary_epochs (list of pd.DataFrame): Epochs during stationary periods (or locomotion offsets).
        pre_time (float): Seconds before transition.
        post_time (float): Seconds after transition.
        time_interval (float): Sampling interval (s/frame).
    """

    # --- Check for valid data ---
    if len(locomotion_epochs) == 0 or len(stationary_epochs) == 0:
        print("⚠️ One or both epoch lists are empty.")
        return

    # --- Extract and align signals ---
    def extract_traces(epochs, key="df/f"):
        """
        Extracts fluorescence traces (or any numerical signal) from epoch DataFrames.

        Args:
            epochs (list of pd.DataFrame): List of epoch DataFrames.
            key (str): Column name containing the signal values (e.g., 'df/f').

        Returns:
            np.ndarray: 2D array (n_epochs × n_samples) of truncated traces.
        """
        traces = []
        for e in epochs:
            if key in e.columns:
                values = e[key].dropna().values
                if len(values) > 0:
                    traces.append(values)
        if len(traces) == 0:
            print(f"⚠️ No valid '{key}' traces found. Columns were {epochs[0].columns.tolist()}")
            return np.array([])
        min_len = min(len(t) for t in traces)
        traces = np.array([t[:min_len] for t in traces])
        return traces

    traces_loco = extract_traces(locomotion_epochs)
    traces_stat = extract_traces(stationary_epochs)

    # --- Compute mean and SEM ---
    mean_loco = np.nanmean(traces_loco, axis=0)
    sem_loco = np.nanstd(traces_loco, axis=0) / np.sqrt(len(traces_loco))

    mean_stat = np.nanmean(traces_stat, axis=0)
    sem_stat = np.nanstd(traces_stat, axis=0) / np.sqrt(len(traces_stat))

    min_len = min(len(mean_stat), len(mean_loco))
    mean_stat = mean_stat[:min_len]
    mean_loco = mean_loco[:min_len]

    # --- Build time axis ---
    n_points = len(mean_loco)
    time_axis = np.linspace(-pre_time, post_time, n_points)

    # --- Create DataFrame for seaborn ---
    df_plot = pd.DataFrame({
        "time (s)": np.tile(time_axis, 2),
        "df/f": np.concatenate([mean_stat, mean_loco]),
        "State": ["Stationary"] * n_points + ["Locomotion"] * n_points
    })

    # --- Plot ---
    plt.figure(figsize=(8,6), layout="constrained")
    sns.lineplot(data=df_plot, x="time (s)", y="df/f", hue="State",
                 palette={"Stationary": "blue", "Locomotion": "red"}, linewidth=1.8)

    # Add shaded SEM region
    ax = plt.gca()

    # Mark transition time
    plt.axvline(0, color="k", linestyle="--")
    plt.text(0, 1.01, "Transition", ha="center", va="bottom", color="black", transform=ax.get_xaxis_transform())

    ax.spines[["top", "right"]].set_visible(False)
    plt.title("Mean dF/F around Locomotion vs Stationary Periods")
    plt.xlabel("Time (s)")
    plt.ylabel("ΔF/F")


def extract_traces(epochs, key="df/f"):
    """
    Extracts fluorescence traces (or any numerical signal) from epoch DataFrames.

    Args:
        epochs (list of pd.DataFrame): List of epoch DataFrames.
        key (str): Column name containing the signal values (e.g., 'df/f').

    Returns:
        np.ndarray: 2D array (n_epochs × n_samples) of truncated traces.
    """
    traces = []
    for e in epochs:
        if key in e.columns:
            values = e[key].dropna().values
            if len(values) > 0:
                traces.append(values)
    if len(traces) == 0:
        print(f"⚠️ No valid '{key}' traces found. Columns were {epochs[0].columns.tolist()}")
        return np.array([])
    min_len = min(len(t) for t in traces)
    traces = np.array([t[:min_len] for t in traces])
    return traces


def plot_non_interaction_trace(epochs, epoch_duration=20, title=""):
    """
    Plots the average trace of non-interaction epochs.

    Args:
        epochs (list of pd.DataFrame): A list of non-interaction epoch DataFrames.
        epoch_duration (int): The duration of the epochs in seconds.
        title (str): The title for the plot.
    """
    if not epochs:
        print("No non-interaction epochs to plot.")
        return

    # Extract df/f traces and align them by truncating to the minimum length
    traces = []
    for epoch in epochs:
        traces.append(epoch['df/f'].values)
    
    if not traces:
        print("Epochs list is not empty, but no valid df/f traces were found.")
        return

    min_len = min(len(t) for t in traces)
    aligned_traces = np.array([t[:min_len] for t in traces])

    # Calculate mean and Standard Error of the Mean (SEM)
    mean_trace = np.mean(aligned_traces, axis=0)
    sem_trace = sem(aligned_traces, axis=0)

    # Create the time axis for the plot
    time_axis = np.linspace(0, epoch_duration, len(mean_trace), endpoint=False)

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(time_axis, mean_trace, label='Avg. Non-Interaction', color='green')
    ax.fill_between(time_axis, mean_trace - sem_trace, mean_trace + sem_trace, color='green', alpha=0.2)
    
    ax.set_xlabel('Time in Epoch (s)')
    ax.set_ylabel('df/f')
    ax.set_title(title)
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend()
    plt.tight_layout()


import random

def get_random_non_interaction_trace(epochs):
    """
    Randomly selects a single trace from a list of non-interaction epochs.

    Args:
        epochs (list of pd.DataFrame): A list of non-interaction epoch DataFrames.

    Returns:
        pd.DataFrame or None: A single randomly selected epoch DataFrame, or None if the list is empty.
    """
    if not epochs:
        return None
    return random.choice(epochs)

def plot_trace_comparison(interaction_trace, non_interaction_trace, time_axis, title=""):
    """
    Draws a graph comparing a brain signal during an object interaction
    with a random signal from a time of no interaction.

    This helps to see if the signal during the interaction is different
    from the baseline "quiet" signal.

    Args:
        interaction_trace (np.ndarray): The average signal trace from around a nose poke event.
        non_interaction_trace (pd.DataFrame): A single, randomly chosen signal trace from a period
                                            when the mouse was not near any objects.
        time_axis (np.ndarray): The time scale for the x-axis of the plot (e.g., from -10s to +10s).
        title (str): The text to show at the top of the graph.
    """
    if non_interaction_trace is None or interaction_trace is None:
        print("One or both traces are missing, cannot plot comparison.")
        return

    fig, ax = plt.subplots(figsize=(10, 6))

    # 1. Plot the interaction trace
    ax.plot(time_axis, interaction_trace, label='Avg. Interaction Trace', color='red', linewidth=2)
    ax.axvline(0, color='k', linestyle='--', label='Nose Poke Event')
    ax.text(0, 1.01, 'nose poke', color='black', weight='bold',
            ha='center', va='bottom', transform=ax.get_xaxis_transform())

    # 2. Plot the non-interaction trace
    # Create a new time axis for the non-interaction trace to overlay it
    non_interaction_dff = non_interaction_trace['df/f'].values
    # We align the start of the non-interaction trace with the start of the interaction trace's time axis
    min_len = min(len(time_axis), len(non_interaction_dff))
    ax.plot(time_axis[:min_len], non_interaction_dff[:min_len], label='Random Non-Interaction Trace', color='blue', linewidth=2)

    # --- Formatting ---
    ax.set_xlabel('Time (s)', weight='bold')
    ax.set_ylabel('df/f', weight='bold')
    ax.set_title(title, fontsize=14, weight='bold')
    ax.spines[['top', 'right']].set_visible(False)
    ax.legend()
    plt.tight_layout()
