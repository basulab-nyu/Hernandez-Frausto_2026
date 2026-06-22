import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import sem
import seaborn as sns





def day_combined_scatter(all_data, i, iterable, epoch, unit, save_path=None, action="", mouse_log=None, ax1lim=None, ax2lim=None):
    # Define groups of days to compare
    group1 = ["D1", "D2", "D3", "D4", "D5", "D6"]
    group2 = ["D7", "D8"]

    mice_id = ['200', '201', '202', '203', '204', '205']
    num_mice = len(mice_id)


    # Initialize storage per mouse
    g1_a_data = [[] for _ in range(num_mice)]
    g1_b_data = [[] for _ in range(num_mice)]
    g2_a_data = [[] for _ in range(num_mice)]
    g2_b_data = [[] for _ in range(num_mice)]

    for j in iterable:
        # Collect Group 1
        for day in group1:
            if day in all_data and j in all_data[day]:
                if "All_a" in all_data[day][j] and "All_b" in all_data[day][j]:
                    a_list = all_data[day][j]["All_a"]
                    b_list = all_data[day][j]["All_b"]

                    current_ids = []
                    if mouse_log and day in mouse_log:
                        current_ids = [mid for mid, mphase in mouse_log[day] if mphase == j]

                    if current_ids:
                        for k, mid in enumerate(current_ids):
                            if k < len(a_list):
                                clean_id = mid.replace("MHF", "")
                                if clean_id in mice_id:
                                    idx = mice_id.index(clean_id)
                                    g1_a_data[idx].append(a_list[k])
                                    g1_b_data[idx].append(b_list[k])
                    else:
                        count = min(len(a_list), len(b_list), num_mice)
                        for k in range(count):
                            g1_a_data[k].append(a_list[k])
                            g1_b_data[k].append(b_list[k])
        # Collect Group 2
        for day in group2:
            if day in all_data and j in all_data[day]:
                if "All_a" in all_data[day][j] and "All_b" in all_data[day][j]:
                    a_list = all_data[day][j]["All_a"]
                    b_list = all_data[day][j]["All_b"]

                    # Debug check for Group 2
                    print(f"DEBUG: Group 2 {day} {j} - Found {len(a_list)} entries.")
                    
                    current_ids = []
                    if mouse_log and day in mouse_log:
                        current_ids = [mid for mid, mphase in mouse_log[day] if mphase == j]
                        print(f"       Mice found: {current_ids}")

                    if current_ids:
                        for k, mid in enumerate(current_ids):
                            if k < len(a_list):
                                clean_id = mid.replace("MHF", "")
                                if clean_id in mice_id:
                                    idx = mice_id.index(clean_id)
                                    g2_a_data[idx].append(a_list[k])
                                    g2_b_data[idx].append(b_list[k])
                    else:
                        count = min(len(a_list), len(b_list), num_mice)
                        for k in range(count):
                            g2_a_data[k].append(a_list[k])
                            g2_b_data[k].append(b_list[k])

    if not any(g1_a_data) or not any(g2_a_data):
        print(f"Skipping due to empty data.")
        return

    # Calculate means per mouse and pool all values
    g1_a_means, g1_b_means = [], []
    g2_a_means, g2_b_means = [], []
    
    g1_all_a_pooled, g1_all_b_pooled = [], []
    g2_all_a_pooled, g2_all_b_pooled = [], []


    
    for k in range(num_mice):
        # G1
        if g1_a_data[k]:
            ma = np.concatenate(g1_a_data[k])
            mb = np.concatenate(g1_b_data[k])
            g1_a_means.append(np.nanmean(ma))
            g1_b_means.append(np.nanmean(mb))
            g1_all_a_pooled.append(ma)
            g1_all_b_pooled.append(mb)
        else:
            g1_a_means.append(np.nan)
            g1_b_means.append(np.nan)
        
        # G2
        if g2_a_data[k]:
            ma = np.concatenate(g2_a_data[k])
            mb = np.concatenate(g2_b_data[k])
            g2_a_means.append(np.nanmean(ma))
            g2_b_means.append(np.nanmean(mb))
            g2_all_a_pooled.append(ma)
            g2_all_b_pooled.append(mb)
        else:
            g2_a_means.append(np.nan)
            g2_b_means.append(np.nan)

    g1_a_means = np.array(g1_a_means)
    g1_b_means = np.array(g1_b_means)
    g2_a_means = np.array(g2_a_means)
    g2_b_means = np.array(g2_b_means)
    
    g1_combined = np.nanmean(np.vstack([g1_a_means, g1_b_means]), axis=0)
    g2_combined = np.nanmean(np.vstack([g2_a_means, g2_b_means]), axis=0)

    def flatten(lst):
        valid = [x for x in lst if len(x) > 0]
        return np.concatenate(valid) if valid else np.array([])

    g1_all_a_flat = flatten(g1_all_a_pooled)
    g1_all_b_flat = flatten(g1_all_b_pooled)
    g2_all_a_flat = flatten(g2_all_a_pooled)
    g2_all_b_flat = flatten(g2_all_b_pooled)

    gconcat_g1_means = np.concatenate([g1_a_means, g1_b_means])
    gconcat_g2_means = np.concatenate([g2_a_means, g2_b_means])

    # --- Scatter Plot ---
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4))

    ax1.scatter(g1_combined, g2_combined, s=50, color='blue', edgecolor='k', alpha=0.7, label="Combined Holes")
    ax1.set_title(f"All Phases Per-mouse means for {unit}")

    min_len_a = min(len(g1_all_a_flat), len(g2_all_a_flat))
    min_len_b = min(len(g1_all_b_flat), len(g2_all_b_flat))

    ax2.scatter(gconcat_g1_means, gconcat_g2_means, s=50, color='blue', edgecolor='k', alpha=0.7)
    ax2.set_title("All values pooled")

    

 #   lim = np.nanmax(np.concatenate([g1_all_a_flat, g2_all_a_flat, g1_all_b_flat, g2_all_b_flat])) * 1.1
    ax1.axline((0, 0), slope=1, color='red', linestyle='--')
    ax2.axline((0, 0), slope=1, color='red', linestyle='--')
    if ax1lim is not None and ax2lim is not None:
    
        ax1.set_xlim(0, ax1lim[0])
        ax1.set_ylim(0, ax1lim[1])
        ax1.legend()


        ax2.set_xlim(0, ax2lim[0])
        ax2.set_ylim(0, ax2lim[1])
        ax2.legend()

    for ax in (ax1, ax2):
        ax.set_ylabel(f"Days 7-8")
        ax.set_xlabel(f"Days 1-6")
    vals = np.concatenate([
        g1_a_means, g1_b_means, g2_a_means, g2_b_means,
        g1_all_a_flat[:min_len_a], g2_all_a_flat[:min_len_a],
        g1_all_b_flat[:min_len_b], g2_all_b_flat[:min_len_b]
    ])
    vals = vals[~np.isnan(vals)]

    data_dict = {
        "g1_a_means": g1_a_means,
        "g1_b_means": g1_b_means,   
        "g2_a_means": g2_a_means,
        "g2_b_means": g2_b_means,
        "g1_all_a_flat": g1_all_a_flat,
        "g1_all_b_flat": g1_all_b_flat,
        "g2_all_a_flat": g2_all_a_flat,
        "g2_all_b_flat": g2_all_b_flat
    }

    data_dict['Mouse_ID'] = np.array(mice_id)
    max_len = max(len(v) for v in data_dict.values())
    for k, v in data_dict.items():
        if len(v) < max_len:
            if np.issubdtype(v.dtype, np.number):
                padded = np.full(max_len, np.nan)
            else:
                padded = np.full(max_len, np.nan, dtype=object)
            padded[:len(v)] = v
            data_dict[k] = padded

    df = pd.DataFrame(data_dict)
    df.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{unit}combined_AllPhases.csv', index=False)
    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{unit}{action}scatter_AllPhases.svg', format='svg')

    # --- Bar Plot ---
    g1_comb = np.nanmean(np.vstack([g1_a_means, g1_b_means]), axis=0)
    g2_comb = np.nanmean(np.vstack([g2_a_means, g2_b_means]), axis=0)

    df = pd.DataFrame({
        unit: np.concatenate([g1_comb, g2_comb]),
        "Condition": ["Days 1-6"] * num_mice + ["Days 7-8"] * num_mice,
        "Mouse": mice_id * 2
    })

    fig_bar, ax_bar = plt.subplots(figsize=(3, 4))
    sns.barplot(data=df, x="Condition", y=unit, ax=ax_bar, capsize=0.3, edgecolor="black", lw=1.5, errwidth=1.5, palette="pastel", estimator=np.mean, errorbar="se")
    sns.stripplot(data=df, x="Condition", y=unit, ax=ax_bar, color="black", size=5, jitter=True, alpha=0.7)

    for idx, cond in enumerate(["Days 1-6", "Days 7-8"]):
        v = df[df["Condition"] == cond][unit].values
        m = np.nanmean(v)
        e = np.nanstd(v, ddof=1) / np.sqrt(np.sum(~np.isnan(v)))
        ax_bar.errorbar(idx, m, yerr=e, color="dimgray", capsize=6, fmt='none', zorder=10, lw=2)

    for m in mice_id:
        x = df[(df['Mouse'] == m) & (df['Condition'] == "Days 1-6")][unit].values
        y = df[(df['Mouse'] == m) & (df['Condition'] == "Days 7-8")][unit].values
        if len(x) > 0 and len(y) > 0 and not np.isnan(x[0]) and not np.isnan(y[0]):
            ax_bar.plot(["Days 1-6", "Days 7-8"], [x, y], color="black", alpha=0.6, zorder=9)

    for axis in ['bottom', 'left']:
        ax_bar.spines[axis].set_linewidth(2.5)
        ax_bar.spines[axis].set_color('0.2')
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)

    ax_bar.set_title(f"All Phases {unit} Comparison", fontsize=16, color="0.2")
    ax_bar.set_xlabel("Condition", fontsize=14, color="0.2")
    ax_bar.set_ylabel(unit, fontsize=14, color="0.2")
    ax_bar.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=15, fontsize=12, weight="bold", color="0.2")
    plt.yticks(fontsize=12, weight="bold", color="0.2")
    ax_bar.tick_params(width=2.5, color='0.2')
    
    if not df[unit].isnull().all():
            plt.ylim(top=df[unit].max() * 1.2)
    

    plt.xlim()
    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{action}barplot_AllPhases.svg', format='svg')
    

def all_csv(all_data, i, iterable, epoch, unit, save_path=None, action="", mouse_log=None):
    avg_data = []
    pooled_data = []

    # Iterate over all days in the dataset
    for day in all_data:
        # Iterate over all phases for the day
        for phase in all_data[day]:

            if "All_a" not in all_data[day][phase] or "All_b" not in all_data[day][phase]:
                continue

            a_list = all_data[day][phase]["All_a"]
            b_list = all_data[day][phase]["All_b"]
            # Retrieve mouse IDs for this day and phase
            current_ids = []
            if mouse_log and day in mouse_log:
                current_ids = [mid for mid, mphase in mouse_log[day] if mphase == phase]

            # Iterate through sessions (mice)
            for idx in range(len(a_list)):
                mouse_id = current_ids[idx] if idx < len(current_ids) else "Unknown"
                
                # Escape Hole (A)
                vals_a = a_list[idx]
                if len(vals_a) > 0:
                    mean_a = np.nanmean(vals_a)
                    avg_data.append({
                        "Mouse_ID": mouse_id,
                        "Day": day,
                        "Phase": phase,
                        "Hole": "Escape Hole",
                        "Value": mean_a
                    })
                    for v in vals_a:
                        pooled_data.append({
                            "Mouse_ID": mouse_id,
                            "Day": day,
                            "Phase": phase,
                            "Hole": "Escape Hole",
                            "Value": v
                        })

                # Non-Escape Hole (B)
                vals_b = b_list[idx]
                if len(vals_b) > 0:
                    mean_b = np.nanmean(vals_b)
                    avg_data.append({
                        "Mouse_ID": mouse_id,
                        "Day": day,
                        "Phase": phase,
                        "Hole": "Non-Escape Hole",
                        "Value": mean_b
                    })
                    for v in vals_b:
                        pooled_data.append({
                            "Mouse_ID": mouse_id,
                            "Day": day,
                            "Phase": phase,
                            "Hole": "Non-Escape Hole",
                            "Value": v
                        })

    # Create DataFrames
    df_avg = pd.DataFrame(avg_data)
    df_pooled = pd.DataFrame(pooled_data)

    # Define output paths
    base_path = f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}'
    avg_path = f'{base_path}/{unit}_{action}_average_all_trials.csv'
    pooled_path = f'{base_path}/{unit}_{action}_pooled_all_trials.csv'

    # Save to CSV
    try:
        df_avg.to_csv(avg_path, index=False)
        print(f"Saved average CSV to: {avg_path}")
    except Exception as e:
        print(f"Failed to save average CSV: {e}")

    try:
        df_pooled.to_csv(pooled_path, index=False)
        print(f"Saved pooled CSV to: {pooled_path}")
    except Exception as e:
        print(f"Failed to save pooled CSV: {e}")

def all_csv_ab(all_data, i, iterable, epoch, unit, save_path=None, action="", mouse_log=None):
    import os
    data_rows = []

    # Iterate over all days in the dataset
    for day in all_data:
        # Iterate over all phases for the day
        for phase in all_data[day]:

            if "A" not in all_data[day][phase] or "B" not in all_data[day][phase]:
                continue

            a_list = all_data[day][phase]["A"]
            b_list = all_data[day][phase]["B"]
            
            # Retrieve mouse IDs for this day and phase
            current_ids = []
            if mouse_log and day in mouse_log:
                current_ids = [mid for mid, mphase in mouse_log[day] if mphase == phase]

            # Iterate through sessions (mice)
            for idx in range(len(a_list)):
                mouse_id = current_ids[idx] if idx < len(current_ids) else "Unknown"
                
                # Escape Hole (A)
                val_a = a_list[idx]
                if isinstance(val_a, (list, np.ndarray)):
                    if len(val_a) == 1:
                        val_a = val_a[0]
                    elif len(val_a) > 1:
                        val_a = np.nanmean(val_a)
                    else:
                        val_a = np.nan
                
                data_rows.append({
                    "Mouse_ID": mouse_id,
                    "Day": day,
                    "Phase": phase,
                    "Hole": "Escape Hole",
                    "Value": val_a
                })

                # Non-Escape Hole (B)
                val_b = b_list[idx]
                if isinstance(val_b, (list, np.ndarray)):
                    if len(val_b) == 1:
                        val_b = val_b[0]
                    elif len(val_b) > 1:
                        val_b = np.nanmean(val_b)
                    else:
                        val_b = np.nan

                data_rows.append({
                    "Mouse_ID": mouse_id,
                    "Day": day,
                    "Phase": phase,
                    "Hole": "Non-Escape Hole",
                    "Value": val_b
                })

    # Create DataFrame
    df = pd.DataFrame(data_rows)

    # Define output path
    base_path = f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}'
    output_path = f'{base_path}/{unit}_{action}_summary_AB.csv'

    # Save to CSV
    if save_path:
        os.makedirs(base_path, exist_ok=True)
        try:
            df.to_csv(output_path, index=False)
            print(f"Saved summary AB CSV to: {output_path}")
        except Exception as e:
            print(f"Failed to save summary AB CSV: {e}")

def alt_day_comp_scatter(all_data, i, iterable, epoch, unit, save_path=None, action="", mouse_log=None):
    # Define groups of days to compare
    group1 = ["D1", "D2", "D3", "D4", "D5", "D6"]
    group2 = ["D7", "D8"]

    mice_id = ['200', '201', '202', '203', '204', '205']
    num_mice = len(mice_id)


    # Initialize storage per mouse
    g1_a_data = [[] for _ in range(num_mice)]
    g1_b_data = [[] for _ in range(num_mice)]
    g2_a_data = [[] for _ in range(num_mice)]
    g2_b_data = [[] for _ in range(num_mice)]

    for j in iterable:
        # Collect Group 1
        for day in group1:
            if day in all_data and j in all_data[day]:
                if "A" in all_data[day][j] and "B" in all_data[day][j]:
                    a_list = all_data[day][j]["A"]
                    b_list = all_data[day][j]["B"]

                    current_ids = []
                    if mouse_log and day in mouse_log:
                        current_ids = [mid for mid, mphase in mouse_log[day] if mphase == j]

                    if current_ids:
                        for k, mid in enumerate(current_ids):
                            if k < len(a_list):
                                clean_id = mid.replace("MHF", "")
                                if clean_id in mice_id:
                                    idx = mice_id.index(clean_id)
                                    g1_a_data[idx].append(a_list[k])
                                    g1_b_data[idx].append(b_list[k])
                    else:
                        count = min(len(a_list), len(b_list), num_mice)
                        for k in range(count):
                            g1_a_data[k].append(a_list[k])
                            g1_b_data[k].append(b_list[k])
        # Collect Group 2
        for day in group2:
            if day in all_data and j in all_data[day]:
                if "A" in all_data[day][j] and "B" in all_data[day][j]:
                    a_list = all_data[day][j]["A"]
                    b_list = all_data[day][j]["B"]

                    # Debug check for Group 2
                    print(f"DEBUG: Group 2 {day} {j} - Found {len(a_list)} entries.")
                    
                    current_ids = []
                    if mouse_log and day in mouse_log:
                        current_ids = [mid for mid, mphase in mouse_log[day] if mphase == j]
                        print(f"       Mice found: {current_ids}")

                    if current_ids:
                        for k, mid in enumerate(current_ids):
                            if k < len(a_list):
                                clean_id = mid.replace("MHF", "")
                                if clean_id in mice_id:
                                    idx = mice_id.index(clean_id)
                                    g2_a_data[idx].append(a_list[k])
                                    g2_b_data[idx].append(b_list[k])
                    else:
                        count = min(len(a_list), len(b_list), num_mice)
                        for k in range(count):
                            g2_a_data[k].append(a_list[k])
                            g2_b_data[k].append(b_list[k])

    if not any(g1_a_data) or not any(g2_a_data):
        print(f"Skipping due to empty data.")
        return

    # Calculate means per mouse and pool all values
    g1_a_means, g1_b_means = [], []
    g2_a_means, g2_b_means = [], []
    
    g1_all_a_pooled, g1_all_b_pooled = [], []
    g2_all_a_pooled, g2_all_b_pooled = [], []


    
    for k in range(num_mice):
        # G1
        if g1_a_data[k]:
            ma = np.concatenate(g1_a_data[k])
            mb = np.concatenate(g1_b_data[k])
            g1_a_means.append(np.nanmean(ma))
            g1_b_means.append(np.nanmean(mb))
            g1_all_a_pooled.append(ma)
            g1_all_b_pooled.append(mb)
        else:
            g1_a_means.append(np.nan)
            g1_b_means.append(np.nan)
        
        # G2
        if g2_a_data[k]:
            ma = np.concatenate(g2_a_data[k])
            mb = np.concatenate(g2_b_data[k])
            g2_a_means.append(np.nanmean(ma))
            g2_b_means.append(np.nanmean(mb))
            g2_all_a_pooled.append(ma)
            g2_all_b_pooled.append(mb)
        else:
            g2_a_means.append(np.nan)
            g2_b_means.append(np.nan)

    g1_a_means = np.array(g1_a_means)
    g1_b_means = np.array(g1_b_means)
    g2_a_means = np.array(g2_a_means)
    g2_b_means = np.array(g2_b_means)

    def flatten(lst):
        valid = [x for x in lst if len(x) > 0]
        return np.concatenate(valid) if valid else np.array([])

    g1_all_a_flat = flatten(g1_all_a_pooled)
    g1_all_b_flat = flatten(g1_all_b_pooled)
    g2_all_a_flat = flatten(g2_all_a_pooled)
    g2_all_b_flat = flatten(g2_all_b_pooled)

    concat_g1_means = np.concatenate([g1_a_means, g1_b_means])
    concat_g2_means = np.concatenate([g2_a_means, g2_b_means])


    # --- Scatter Plot ---
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4), sharex=True, sharey=True)


    ax1.scatter(g1_b_means, g2_b_means, s=50, color='orange', edgecolor='k', alpha=0.7, label="Non-Escape Hole")
    ax1.set_title(f"All Phases Per-mouse means")

    min_len = min(len(concat_g1_means), len(concat_g2_means))

    
    ax2.scatter(concat_g1_means[:min_len], concat_g2_means[min_len], s=50, color='blue', edgecolor='k', alpha=0.7)
    
    ax2.set_title("All values pooled")

    for ax in (ax1, ax2):
        ax.axline((0, 0), slope=1, color='red', linestyle='--')
        ax.legend()

    vals = np.concatenate([
        g1_a_means, g1_b_means, g2_a_means, g2_b_means,
        g1_all_a_flat[:min_len_a], g2_all_a_flat[:min_len_a],
        g1_all_b_flat[:min_len_b], g2_all_b_flat[:min_len_b]
    ])
    vals = vals[~np.isnan(vals)]

    data_dict = {
        "g1_a_means": g1_a_means,
        "g1_b_means": g1_b_means,   
        "g2_a_means": g2_a_means,
        "g2_b_means": g2_b_means,
        "g1_all_a_flat": g1_all_a_flat,
        "g1_all_b_flat": g1_all_b_flat,
        "g2_all_a_flat": g2_all_a_flat,
        "g2_all_b_flat": g2_all_b_flat
    }

    data_dict['Mouse_ID'] = np.array(mice_id)
    max_len = max(len(v) for v in data_dict.values())
    for k, v in data_dict.items():
        if len(v) < max_len:
            if np.issubdtype(v.dtype, np.number):
                padded = np.full(max_len, np.nan)
            else:
                padded = np.full(max_len, np.nan, dtype=object)
            padded[:len(v)] = v
            data_dict[k] = padded

    df = pd.DataFrame(data_dict)
    df.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{action}scatter_AllPhases.csv', index=False)
    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{action}scatter_AllPhases.svg', format='svg')

    # --- Bar Plot ---
    g1_comb = np.nanmean(np.vstack([g1_a_means, g1_b_means]), axis=0)
    g2_comb = np.nanmean(np.vstack([g2_a_means, g2_b_means]), axis=0)

    df = pd.DataFrame({
        unit: np.concatenate([g1_comb, g2_comb]),
        "Condition": ["Days 1-6"] * num_mice + ["Days 7-8"] * num_mice,
        "Mouse": mice_id * 2
    })

    fig_bar, ax_bar = plt.subplots(figsize=(3, 4))
    sns.barplot(data=df, x="Condition", y=unit, ax=ax_bar, capsize=0.3, edgecolor="black", lw=1.5, errwidth=1.5, palette="pastel", estimator=np.mean, errorbar="se")
    sns.stripplot(data=df, x="Condition", y=unit, ax=ax_bar, color="black", size=5, jitter=True, alpha=0.7)

    for idx, cond in enumerate(["Days 1-6", "Days 7-8"]):
        v = df[df["Condition"] == cond][unit].values
        m = np.nanmean(v)
        e = np.nanstd(v, ddof=1) / np.sqrt(np.sum(~np.isnan(v)))
        ax_bar.errorbar(idx, m, yerr=e, color="dimgray", capsize=6, fmt='none', zorder=10, lw=2)

    for m in mice_id:
        x = df[(df['Mouse'] == m) & (df['Condition'] == "Days 1-6")][unit].values
        y = df[(df['Mouse'] == m) & (df['Condition'] == "Days 7-8")][unit].values
        if len(x) > 0 and len(y) > 0 and not np.isnan(x[0]) and not np.isnan(y[0]):
            ax_bar.plot(["Days 1-6", "Days 7-8"], [x, y], color="black", alpha=0.6, zorder=9)

    for axis in ['bottom', 'left']:
        ax_bar.spines[axis].set_linewidth(2.5)
        ax_bar.spines[axis].set_color('0.2')
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)

    ax_bar.set_title(f"All Phases {unit} Comparison", fontsize=16, color="0.2")
    ax_bar.set_xlabel("Condition", fontsize=14, color="0.2")
    ax_bar.set_ylabel(unit, fontsize=14, color="0.2")
    ax_bar.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=15, fontsize=12, weight="bold", color="0.2")
    plt.yticks(fontsize=12, weight="bold", color="0.2")
    ax_bar.tick_params(width=2.5, color='0.2')
    
    if not df[unit].isnull().all():
            plt.ylim(top=df[unit].max() * 1.2)

    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{action}barplot_AllPhases.svg', format='svg')
    
    plt.show()


def day_comp_scatter(all_data, i, iterable, epoch, unit, save_path=None, action="", mouse_log=None, ax1lim=None, ax2lim=None):
    # Define groups of days to compare
    group1 = ["D1", "D2", "D3", "D4", "D5", "D6"]
    group2 = ["D7", "D8"]

    mice_id = ['200', '201', '202', '203', '204', '205']
    num_mice = len(mice_id)

    combined_g1_a = []
    combined_g1_b = []
    combined_g2_a = []
    combined_g2_b = []

    # Initialize storage per mouse
    g1_a_data = [[] for _ in range(num_mice)]
    g1_b_data = [[] for _ in range(num_mice)]
    g2_a_data = [[] for _ in range(num_mice)]
    g2_b_data = [[] for _ in range(num_mice)]

    for j in iterable:
        # Collect Group 1
        for day in group1:
            if day in all_data and j in all_data[day]:
                if "All_a" in all_data[day][j] and "All_b" in all_data[day][j]:
                    a_list = all_data[day][j]["All_a"]
                    b_list = all_data[day][j]["All_b"]

                    current_ids = []
                    if mouse_log and day in mouse_log:
                        current_ids = [mid for mid, mphase in mouse_log[day] if mphase == j]

                    if current_ids:
                        for k, mid in enumerate(current_ids):
                            if k < len(a_list):
                                clean_id = mid.replace("MHF", "")
                                if clean_id in mice_id:
                                    idx = mice_id.index(clean_id)
                                    g1_a_data[idx].append(a_list[k])
                                    g1_b_data[idx].append(b_list[k])
                    else:
                        count = min(len(a_list), len(b_list), num_mice)
                        for k in range(count):
                            g1_a_data[k].append(a_list[k])
                            g1_b_data[k].append(b_list[k])
        # Collect Group 2
        for day in group2:
            if day in all_data and j in all_data[day]:
                if "All_a" in all_data[day][j] and "All_b" in all_data[day][j]:
                    a_list = all_data[day][j]["All_a"]
                    b_list = all_data[day][j]["All_b"]

                    # Debug check for Group 2
                    print(f"DEBUG: Group 2 {day} {j} - Found {len(a_list)} entries.")
                    
                    current_ids = []
                    if mouse_log and day in mouse_log:
                        current_ids = [mid for mid, mphase in mouse_log[day] if mphase == j]
                        print(f"       Mice found: {current_ids}")

                    if current_ids:
                        for k, mid in enumerate(current_ids):
                            if k < len(a_list):
                                clean_id = mid.replace("MHF", "")
                                if clean_id in mice_id:
                                    idx = mice_id.index(clean_id)
                                    g2_a_data[idx].append(a_list[k])
                                    g2_b_data[idx].append(b_list[k])
                    else:
                        count = min(len(a_list), len(b_list), num_mice)
                        for k in range(count):
                            g2_a_data[k].append(a_list[k])
                            g2_b_data[k].append(b_list[k])

    if not any(g1_a_data) or not any(g2_a_data):
        print(f"Skipping due to empty data.")
        return

    # Calculate means per mouse and pool all values
    g1_a_means, g1_b_means = [], []
    g2_a_means, g2_b_means = [], []
    
    g1_all_a_pooled, g1_all_b_pooled = [], []
    g2_all_a_pooled, g2_all_b_pooled = [], []


    
    for k in range(num_mice):
        # G1
        if g1_a_data[k]:
            ma = np.concatenate(g1_a_data[k])
            mb = np.concatenate(g1_b_data[k])
            g1_a_means.append(np.nanmean(ma))
            g1_b_means.append(np.nanmean(mb))
            g1_all_a_pooled.append(ma)
            g1_all_b_pooled.append(mb)
        else:
            g1_a_means.append(np.nan)
            g1_b_means.append(np.nan)
        
        # G2
        if g2_a_data[k]:
            ma = np.concatenate(g2_a_data[k])
            mb = np.concatenate(g2_b_data[k])
            g2_a_means.append(np.nanmean(ma))
            g2_b_means.append(np.nanmean(mb))
            g2_all_a_pooled.append(ma)
            g2_all_b_pooled.append(mb)
        else:
            g2_a_means.append(np.nan)
            g2_b_means.append(np.nan)

    g1_a_means = np.array(g1_a_means)
    g1_b_means = np.array(g1_b_means)
    g2_a_means = np.array(g2_a_means)
    g2_b_means = np.array(g2_b_means)

    def flatten(lst):
        valid = [x for x in lst if len(x) > 0]
        return np.concatenate(valid) if valid else np.array([])

    g1_all_a_flat = flatten(g1_all_a_pooled)
    g1_all_b_flat = flatten(g1_all_b_pooled)
    g2_all_a_flat = flatten(g2_all_a_pooled)
    g2_all_b_flat = flatten(g2_all_b_pooled)

    # --- Scatter Plot ---
    fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(10, 4))

    ax1.scatter(g1_a_means, g2_a_means, s=50, color='blue', edgecolor='k', alpha=0.7, label="Escape Hole")
    ax1.scatter(g1_b_means, g2_b_means, s=50, color='orange', edgecolor='k', alpha=0.7, label="Non-Escape Hole")
    ax1.set_title(f"All Phases Per-mouse means for {unit}")

    min_len_a = min(len(g1_all_a_flat), len(g2_all_a_flat))
    min_len_b = min(len(g1_all_b_flat), len(g2_all_b_flat))
    
    ax2.scatter(g1_all_a_flat[:min_len_a], g2_all_a_flat[:min_len_a], s=50, color='blue', edgecolor='k', alpha=0.7)
    ax2.scatter(g1_all_b_flat[:min_len_b], g2_all_b_flat[:min_len_b], s=50, color='orange', edgecolor='k', alpha=0.7)
    ax2.set_title("All values pooled")

    for ax in (ax1, ax2):
        ax.set_ylabel(f"Days 7-8")
        ax.set_xlabel(f"Days 1-6")

   # lim = np.nanmax(np.concatenate([g1_all_a_flat, g2_all_a_flat, g1_all_b_flat, g2_all_b_flat])) * 1.1

    ax1.axline((0, 0), slope=1, color='red', linestyle='--')
    ax2.axline((0, 0), slope=1, color='red', linestyle='--')
    if ax1lim is not None and ax2lim is not None:
    
        ax1.set_xlim(0, ax1lim[0])
        ax1.set_ylim(0, ax1lim[1])
        ax1.legend()


        ax2.set_xlim(0, ax2lim[0])
        ax2.set_ylim(0, ax2lim[1])
        ax2.legend()

    vals = np.concatenate([
        g1_a_means, g1_b_means, g2_a_means, g2_b_means,
        g1_all_a_flat[:min_len_a], g2_all_a_flat[:min_len_a],
        g1_all_b_flat[:min_len_b], g2_all_b_flat[:min_len_b]
    ])
    vals = vals[~np.isnan(vals)]


    means_data = []
    for idx, mouse in enumerate(mice_id):
        # D1-6 data
        means_data.append({
            'Mouse_ID': mouse,
            'Period': 'D1-6',
            'Escape_Hole_Mean': g1_a_means[idx],
            'Non_Escape_Hole_Mean': g1_b_means[idx]
        })
        # D7-8 data
        means_data.append({
            'Mouse_ID': mouse,
            'Period': 'D7-8',
            'Escape_Hole_Mean': g2_a_means[idx],
            'Non_Escape_Hole_Mean': g2_b_means[idx]
        })

    df_means = pd.DataFrame(means_data)
    df_means.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{unit}{action}means_AllPhases.csv', index=False)

    pooled_data = []
    for idx, mouse in enumerate(mice_id):
        # explanation: if the number of mice is greater than the length of pooled list create a row to use the data
        # D1-6 Escape Hole
        if idx < len(g1_all_a_pooled) and len(g1_all_a_pooled[idx]) > 0:
            for val in g1_all_a_pooled[idx]:
                pooled_data.append({
                    'Mouse_ID': mouse,
                    'Period': 'D1-6',
                    'Hole_Type': 'Escape_Hole',
                    'Value': val
                })
        
        # D1-6 Non-Escape Hole same thing but with object B / non-escape hole
        if idx < len(g1_all_b_pooled) and len(g1_all_b_pooled[idx]) > 0:
            for val in g1_all_b_pooled[idx]:
                pooled_data.append({
                    'Mouse_ID': mouse,
                    'Period': 'D1-6',
                    'Hole_Type': 'Non_Escape_Hole',
                    'Value': val
                })
        
        # D7-8 Escape Hole
        if idx < len(g2_all_a_pooled) and len(g2_all_a_pooled[idx]) > 0:
            for val in g2_all_a_pooled[idx]:
                pooled_data.append({
                    'Mouse_ID': mouse,
                    'Period': 'D7-8',
                    'Hole_Type': 'Escape_Hole',
                    'Value': val
                })
        
        # D7-8 Non-Escape Hole
        if idx < len(g2_all_b_pooled) and len(g2_all_b_pooled[idx]) > 0:
            for val in g2_all_b_pooled[idx]:
                pooled_data.append({
                    'Mouse_ID': mouse,
                    'Period': 'D7-8',
                    'Hole_Type': 'Non_Escape_Hole',
                    'Value': val
                })

    df_pooled = pd.DataFrame(pooled_data)
    df_pooled.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{unit}{action}pooled_AllPhases.csv', index=False)
    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{action}scatter_AllPhases.svg', format='svg')

    # --- Bar Plot ---
    g1_comb = np.nanmean(np.vstack([g1_a_means, g1_b_means]), axis=0)
    g2_comb = np.nanmean(np.vstack([g2_a_means, g2_b_means]), axis=0)

    df = pd.DataFrame({
        unit: np.concatenate([g1_comb, g2_comb]),
        "Condition": ["Days 1-6"] * num_mice + ["Days 7-8"] * num_mice,
        "Mouse": mice_id * 2
    })

    fig_bar, ax_bar = plt.subplots(figsize=(3, 4))
    sns.barplot(data=df, x="Condition", y=unit, ax=ax_bar, capsize=0.3, edgecolor="black", lw=1.5, errwidth=1.5, palette="pastel", estimator=np.mean, errorbar="se")
    sns.stripplot(data=df, x="Condition", y=unit, ax=ax_bar, color="black", size=5, jitter=True, alpha=0.7)

    for idx, cond in enumerate(["Days 1-6", "Days 7-8"]):
        v = df[df["Condition"] == cond][unit].values
        m = np.nanmean(v)
        e = np.nanstd(v, ddof=1) / np.sqrt(np.sum(~np.isnan(v)))
        ax_bar.errorbar(idx, m, yerr=e, color="dimgray", capsize=6, fmt='none', zorder=10, lw=2)

    for m in mice_id:
        x = df[(df['Mouse'] == m) & (df['Condition'] == "Days 1-6")][unit].values
        y = df[(df['Mouse'] == m) & (df['Condition'] == "Days 7-8")][unit].values
        if len(x) > 0 and len(y) > 0 and not np.isnan(x[0]) and not np.isnan(y[0]):
            ax_bar.plot(["Days 1-6", "Days 7-8"], [x, y], color="black", alpha=0.6, zorder=9)

    for axis in ['bottom', 'left']:
        ax_bar.spines[axis].set_linewidth(2.5)
        ax_bar.spines[axis].set_color('0.2')
    ax_bar.spines['top'].set_visible(False)
    ax_bar.spines['right'].set_visible(False)

    ax_bar.set_title(f"All Phases {unit} Comparison", fontsize=16, color="0.2")
    ax_bar.set_xlabel("Condition", fontsize=14, color="0.2")
    ax_bar.set_ylabel(unit, fontsize=14, color="0.2")
    ax_bar.grid(axis="y", linestyle="--", alpha=0.7)
    plt.xticks(rotation=15, fontsize=12, weight="bold", color="0.2")
    plt.yticks(fontsize=12, weight="bold", color="0.2")
    ax_bar.tick_params(width=2.5, color='0.2')
    
    if not df[unit].isnull().all():
            plt.ylim(top=df[unit].max() * 1.2)

    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{action}barplot_AllPhases.svg', format='svg')
    


def histo(all, i, cond, trunc_time, save_path=None):
   
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(all, bins=25, alpha=0.7)

    # time_interval = 0.01660136795
    # truncate = round(trunc_time / time_interval)

    # ncols = 2  # we only want All_a and All_b
    # fig, axes = plt.subplots(ncols=ncols, figsize=(4 * ncols, 4), sharex=True, sharey=True)

    # if ncols == 1:
    #     axes = [axes]

    # ax_a = axes[0]
    # ax_b = axes[1]

    # print(all[i][cond]["All_a"])
    # ax_a.hist(all[i][cond]["All_a"], bins=25, alpha=0.7)
    # ax_a.set_xlabel("Object A")
    # ax_a.set_ylabel("Count")
    # ax_a.set_title(cond)

    # ax_b.hist(all[i][cond]["All_b"], bins=25, alpha=0.7)
    # ax_b.set_xlabel("Object B")
    # ax_b.set_title(cond)

    # plt.tight_layout()
    # if save_path:
    #     plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/NORNOL/histogram/{i}_{cond}.svg', format="svg")

def hole_scatter(all, i, iterable, epoch, unit, save_path=None, action=""):
    global_limit = 0

    # First pass: find the global limit based on all pooled values
    for j in iterable:
        a_list = all[i][j]["All_a"]
        b_list = all[i][j]["All_b"]
        print(f" a_list be like: {a_list}")

        if not a_list or not b_list:
            print(f"Skipping {i} {j} due to empty data.")
            continue
        cat_a = np.concatenate(a_list)
        cat_b = np.concatenate(b_list)
        if len(cat_a) > 0 and len(cat_b) > 0:
            min_len = min(len(cat_a), len(cat_b))
            global_limit = max(global_limit, np.max(cat_a[:min_len]), np.max(cat_b[:min_len]))

    # Second pass: plot each condition in its own figure
    for j in iterable:
        a_list = all[i][j]["All_a"]
        b_list = all[i][j]["All_b"]
        if not a_list or not b_list:
            print(f"Skipping {i} {j} due to empty data.")
            continue
        cat_a = np.concatenate(a_list)
        cat_b = np.concatenate(b_list)
        min_len = min(len(cat_a), len(cat_b))

        fig, ax = plt.subplots(figsize=(5, 4))
        ax.scatter(cat_a[:min_len], cat_b[:min_len], alpha=0.5, label="All values")

        # Per-session means
        a_means = [np.nanmean(sess) for sess in a_list]
        b_means = [np.nanmean(sess) for sess in b_list]
        ax.scatter(a_means, b_means, color="black", marker="x", s=60, label="Per-session mean")

        ax.set_title(j, weight='bold')
        ax.set_xlabel('Escape Hole', weight='bold')
        ax.set_ylabel('Non-Escape Hole', weight='bold')
        ax.spines[['top', 'right']].set_visible(False)
        ax.axline((0, 0), slope=1, color='red', linestyle='--')
        # ax.set_xlim(0, global_limit)
        # ax.set_ylim(0, global_limit)
        ax.set_aspect('equal', 'box')
        ax.legend()
        plt.xlim(0, max(ax.get_xlim()[1], ax.get_ylim()[1]) * 1.5)
        plt.ylim(0, max(ax.get_xlim()[1], ax.get_ylim()[1]) * 1.5)

        if save_path:
            plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/{unit}/{action}scatter{i}{j}.svg', format='svg')

    plt.tight_layout()
    plt.show()


        # the difference found between holes and their prospective unit of measurement
    
    
    # for j in iterable:
    #     # Make sure this condition exists
    #     if j not in all[i]:
    #         continue  
        
    #     a_list = all[i][j]["All_a"]
    #     b_list = all[i][j]["All_b"]

    #     # Ensure both lists have the same length
    #     min_len = min(len(a_list[0]), len(b_list[0]))

        

    #     ax1.scatter((a_list[0])[:min_len], (b_list[0])[:min_len], alpha=0.7)
    #     ax2.scatter((a_list[1])[:min_len], (b_list[1])[:min_len], alpha=0.7)

    #     # Make axes square and equal
    #     ylimits = ax1.get_ylim()
    #     xlimits = ax1.get_xlim()
    #     max_len = max(ylimits[1], xlimits[1])

    #     plt.xlim(0, max_len)
    #     plt.ylim(0, max_len)

    #     ax1.axline((0, 0), slope=1, color='red', linestyle='--')

    #     plt.suptitle(f"{i} - {j} | {unit} ({epoch})")

    #     if save_path:
    #         plt.savefig(f"{save_path}/{i}_{j}_{unit}_{epoch}.png")


def rate_scatter(all, i, iterable, epoch, unit, save_path=None):
    for j in iterable:
        if "All_a" not in all[i][j] or "All_b" not in all[i][j]:
            print(f"Skipping {i} {j}: Missing All_a or All_b.")
            continue
        a_list = [a for a in all[i][j]["All_a"]]
        b_list = [b for b in all[i][j]["All_b"]]
        if not a_list or not b_list:
            print(f"Skipping {i} {j} due to empty All_a or All_b.")
            continue
        min_len_a = min(len(a_list[0]), len(b_list[0]))
        fig, (ax1, ax2) = plt.subplots(ncols=2, figsize=(6, 6), sharex=True, sharey=True)
        ax1.scatter((a_list[0])[:min_len_a], (b_list[0])[:min_len_a], alpha=0.7)
        ax2.scatter((a_list[1])[:min_len_a], (b_list[1])[:min_len_a], alpha=0.7)

        ylimits = ax1.get_ylim()
        xlimits = ax1.get_xlim()
        max_len = max(ylimits[1], xlimits[1])
        plt.xlim(0, max_len)
        plt.ylim(0, max_len)
        ax1.axline((0, 0), slope=1, color='red', linestyle='--')
        plt.tight_layout()
        plt.show()

def plot_dual_trace(traces_a, traces_b, i, j, zscore, trunc_time, title=""):
    
    # use the total seconds wanted and then find the total seconds
    time_interval=0.01660136795
    # finds the amount of values using the rate of collection
    truncate = round(trunc_time / time_interval) 
    
    # Truncate both traces to the same minimum length
    min_len = min(traces_a.shape[0], traces_b.shape[0], round(trunc_time / time_interval))
    traces_a = traces_a[:min_len]
    traces_b = traces_b[:min_len]

    mean_A = traces_a.mean(axis=1)[:truncate] 
    mean_B = traces_b.mean(axis=1)[:truncate] 

    combined = (mean_A + mean_B) / 2


    
    start_time = -10
    time_axis = np.arange(start_time, start_time + min_len * time_interval, time_interval)[:truncate]
    

    # Plot
    plt.figure(figsize=(10, 6),layout="constrained")
    plt.plot(time_axis, mean_A, label='Object A', color='blue')
    plt.plot(time_axis, mean_B, label="Object B", color="red")
    
    plt.axvline(0, color='k', linestyle='--')
    plt.xlabel('Time (s)')
    plt.ylabel('Z-score' if zscore else 'df/f')
    plt.title(title if title else f"Calcium Trace {i} {j}")
    plt.legend()
    plt.tight_layout()


    return mean_A, mean_B, time_axis

def plot_combined_traces(trace, i, looptype, time_axis, zscore, action, save_path=None):
    action_str = "Entrance" if action == "entrance" else "Exit"

    fig, ax = plt.subplots(figsize=(6, 4))
    for cond in looptype[1]:
        # Filter valid A traces
        a_list = [a for a in trace[i][cond]['A'] if len(a) == len(time_axis)]
        b_list = [b for b in trace[i][cond]['B'] if len(b) == len(time_axis)]

        if not a_list or not b_list:
            print(f"Skipping {i} {cond} due to empty or mismatched traces.")
            continue

        # Convert to arrays, guard against empty arrays
        if len(a_list) == 0 or len(b_list) == 0:
            print(f"Skipping {i} {cond} due to empty trace arrays.")
            continue
        a_traces = np.stack(a_list)
        b_traces = np.stack(b_list)
        combined = (a_traces + b_traces) / 2

        mean = np.mean(combined, axis=0)
        error = sem(combined, axis=0)

        ax.plot(time_axis, mean, label=f'{action_str} {i} {cond}')
        ax.fill_between(time_axis, mean - error, mean + error, alpha=0.2)

    ax.axvline(0, color='k', linestyle='--')
    ax.text(0, 1.01, 'nose poke', color='black', weight='bold', ha='center', va='bottom', transform=ax.get_xaxis_transform())
    
    ax.spines[['top', 'right']].set_visible(False)
    plt.xticks(weight='bold')
    plt.yticks(weight='bold')
    
    plt.xlabel('Time (s)', weight='bold')
    plt.ylabel('z-score' if zscore else 'df/f', weight='bold')
    plt.title(f'{action_str} Avg: {"z-score" if zscore else "df/f"} A & B | Group: {i}', y=1.05)
    plt.legend()
    plt.tight_layout()
    
    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/svg/Barnes/figurefor{action_str}{i}.png')

def plot_mouse_daily_traces(all_traces, days, time_axis, zscore, action, save_path=None):
    import os
    from scipy.stats import sem
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt

    action_str = "Entrance" if action == "entrance" else "Exit"

    # Loop through each mouse
    for mouse_id, mouse_data in all_traces.items():
        fig, ax = plt.subplots(figsize=(10, 6))
        plt.title(f"Daily Average Traces for Mouse: {mouse_id}", weight='bold')

        for day in days:
            if day not in mouse_data:
                continue

            day_data = mouse_data[day]
            combined_traces = []

            # --- Average across all phases (e.g., FAM/NOV) ---
            for phase_name, phase_data in day_data.items():
                traces_a = phase_data.get('All_a', [])
                traces_b = phase_data.get('All_b', [])
                for a, b in zip(traces_a, traces_b):
                    if len(a) == len(time_axis) and len(b) == len(time_axis):
                        combined_traces.append((a + b) / 2)

            if not combined_traces:
                continue

            combined_traces = np.stack(combined_traces)
            daily_mean_trace = np.mean(combined_traces, axis=0)
            daily_sem_trace = sem(combined_traces, axis=0)

            # Plot on same figure for this mouse
            ax.plot(time_axis, daily_mean_trace, label=f'{day}')
            ax.fill_between(time_axis, daily_mean_trace - daily_sem_trace, daily_mean_trace + daily_sem_trace, alpha=0.2)

            # --- Save CSV for this mouse–day ---
            if False:
                os.makedirs(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/zscore/', exist_ok=True)
                df = pd.DataFrame({
                    'Time (s)': time_axis,
                    'Mean Trace': daily_mean_trace,
                    'SEM': daily_sem_trace
                })
                df.to_csv(
                    f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/zscore/{action_str}_Daily_{mouse_id}_{day}.csv',
                    index=False
                )

        # --- Format figure ---
        ax.axvline(0, color='k', linestyle='--')
        ax.text(0, 1.01, 'Nose Poke', color='black', weight='bold', ha='center', va='bottom', transform=ax.get_xaxis_transform())
        ax.spines[['top', 'right']].set_visible(False)
        plt.xticks(weight='bold')
        plt.yticks(weight='bold')
        plt.xlabel('Time (s)', weight='bold')
        plt.ylabel('Z-score' if zscore else 'dF/F', weight='bold')
        plt.legend(title="Day")
        plt.tight_layout()

        if False:
            plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/zscore/{action_str}_AllDays_{mouse_id}.svg', format='svg')
        plt.show()
def plot_daily_traces(all_traces, mouse_description, days, time_axis, zscore, action, save_path=None, phases=None):
    """
    Plots the daily average of Z-score traces.
    Each day's trace is an average of all phases for that day.
    """
    action_str = "Entrance" if action == "entrance" else "Exit"

    fig, ax = plt.subplots(figsize=(10, 6))

    for day in days:
        if day not in all_traces:
            continue

        # --- Data and Label Collection (Paired) ---
        # We will build the final list of traces and labels together to prevent mismatches.
        combined_traces = []
        trace_labels = []

        if phases:
            sorted_phases = [p for p in phases if p in all_traces[day]]
        else:
            sorted_phases = sorted(all_traces[day].keys())
        session_counter = 0

        for phase in sorted_phases:
            traces_a = all_traces[day][phase].get('All_a', [])
            traces_b = all_traces[day][phase].get('All_b', [])

            # Process session by session to keep data and labels in sync
            for i in range(len(traces_a)):
                a, b = traces_a[i], traces_b[i]

                # Only include this session if both traces are valid
                if len(a) == len(time_axis) and len(b) == len(time_axis):
                    combined_traces.append((a + b) / 2)
                    
                    # Get the corresponding label for this specific session
                    mouse_id, session_phase = mouse_description[day][session_counter]
                    trace_labels.append(f"{mouse_id}_{session_phase}")
                else:
                    print(f"Skipping plot for {day} (Session {session_counter}): Data length {len(a)} does not match time axis {len(time_axis)}")
                
                session_counter += 1

        # --- CSV and Plotting ---
        if not combined_traces:
            continue

        individual_traces_df = pd.DataFrame(combined_traces).T
        individual_traces_df.columns = trace_labels

        individual_traces_df.insert(0, 'Time (s)', time_axis)
        
        # Save the individual traces to CSV
        individual_traces_df.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/zscore/{action_str}_Mice_Traces_{day}.csv', index=False)
        
        # --- Plotting Logic ---
        if combined_traces:
            combined_traces_arr = np.stack(combined_traces)
            mean_trace = np.mean(combined_traces_arr, axis=0)
            sem_trace = sem(combined_traces_arr, axis=0)
            ax.plot(time_axis, mean_trace, label=f'{day}')
            ax.fill_between(time_axis, mean_trace - sem_trace, mean_trace + sem_trace, alpha=0.2)


    ax.axvline(0, color='k', linestyle='--')
    ax.text(0, 1.01, 'Nose Poke', color='black', weight='bold', ha='center', va='bottom', transform=ax.get_xaxis_transform())
    ax.spines[['top', 'right']].set_visible(False)
    plt.xticks(weight='bold')
    plt.yticks(weight='bold')
    plt.xlabel('Time (s)', weight='bold')
    plt.ylabel('Z-score' if zscore else 'dF/F', weight='bold')
    plt.legend(title="Day")
    plt.tight_layout()

    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/exit{action_str}.svg', format='svg')

def plot_daily_traces_separated(all_traces, mouse_description, days, time_axis, zscore, action, save_path=None, phases=None):
    """
    Plots the daily average of Z-score traces for escape and non-escape holes separately.
    """
    action_str = "Entrance" if action == "entrance" else "Exit"

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), sharey=True)

    for day in days:
        if day not in all_traces:
            continue

        traces_a_list = []
        traces_b_list = []
        labels_list = []
        
        if phases:
            sorted_phases = [p for p in phases if p in all_traces[day]]
        else:
            sorted_phases = sorted(all_traces[day].keys())
        session_counter = 0

        for phase in sorted_phases:
            phase_traces_a = all_traces[day][phase].get('A', [])
            phase_traces_b = all_traces[day][phase].get('B', [])

            # Assuming A and B lists are aligned by session (mouse)
            for i in range(len(phase_traces_a)):
                if i < len(phase_traces_b):
                    a = phase_traces_a[i]
                    b = phase_traces_b[i]
                    
                    # Check validity
                    valid_a = (len(a) == len(time_axis))
                    valid_b = (len(b) == len(time_axis))
                    
                    if valid_a and valid_b:
                        traces_a_list.append(a)
                        traces_b_list.append(b)
                        
                        # Get label
                        if day in mouse_description and session_counter < len(mouse_description[day]):
                            mouse_id, session_phase = mouse_description[day][session_counter]
                            labels_list.append(f"{mouse_id}_{session_phase}")
                        else:
                            labels_list.append(f"Unknown_{session_counter}")
                
                session_counter += 1

        # --- Save CSVs ---
        if traces_a_list:
            df_a = pd.DataFrame(traces_a_list).T
            df_a.columns = labels_list
            df_a.insert(0, 'Time (s)', time_axis)
            df_a.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/z_score_sep/{action_str}_A_Traces_{day}.csv', index=False)
            
            # Plot A
            arr_a = np.stack(traces_a_list)
            mean_a = np.mean(arr_a, axis=0)
            sem_a = sem(arr_a, axis=0)
            ax1.plot(time_axis, mean_a, label=f'{day}')
            ax1.fill_between(time_axis, mean_a - sem_a, mean_a + sem_a, alpha=0.2)

        if traces_b_list:
            df_b = pd.DataFrame(traces_b_list).T
            df_b.columns = labels_list
            df_b.insert(0, 'Time (s)', time_axis)
            df_b.to_csv(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/z_score_sep/{action_str}_B_Traces_{day}.csv', index=False)

            # Plot B
            arr_b = np.stack(traces_b_list)
            mean_b = np.mean(arr_b, axis=0)
            sem_b = sem(arr_b, axis=0)
            ax2.plot(time_axis, mean_b, label=f'{day}')
            ax2.fill_between(time_axis, mean_b - sem_b, mean_b + sem_b, alpha=0.2)

    # Formatting
    ax1.set_ylabel('Z-score' if zscore else 'dF/F', weight='bold')
    
    for ax, title in zip([ax1, ax2], ["Escape Hole (A)", "Non-Escape Hole (B)"]):
        ax.axvline(0, color='k', linestyle='--')
        ax.text(0, 1.01, 'Nose Poke', color='black', weight='bold', ha='center', va='bottom', transform=ax.get_xaxis_transform())
        ax.spines[['top', 'right']].set_visible(False)
        plt.setp(ax.get_xticklabels(), weight='bold')
        plt.setp(ax.get_yticklabels(), weight='bold')
        ax.set_xlabel('Time (s)', weight='bold')
        ax.set_title(title, weight='bold')
        ax.legend(title="Day")

    plt.tight_layout()

    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/z_score_sep/separated_{action_str}.svg', format='svg')

def plot_auc_bar(all_aucs, i, looptype, action="", title="", ylabel="AUC", save_path=None):

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


    plt.figure(figsize=(5, 4))
    df_all = []  # Initialize a list to collect DataFrames for each condition
    for cond in all_aucs[i]:
        if all_aucs[i][cond]['A'] and all_aucs[i][cond]['B']:
            a_list = [a for a in all_aucs[i][cond]['A']]
            b_list = [b for b in all_aucs[i][cond]['B']]
        else:
            print(f"Skipping {i}-{cond}: Missing data")
            continue
        # Get AUCs for A and B
        if len(a_list) == 0 or len(b_list) == 0:
            print(f"Skipping {i}-{cond}: Empty A or B list after filtering")
            continue
        a_aucs = np.stack(a_list)
        b_aucs = np.stack(b_list)
        combined = (a_aucs + b_aucs) / 2
        mean = np.mean(combined, axis=0)
        error = sem(combined, axis=0)

        df = pd.DataFrame({
            'AUC': mean,
            'Condition': [cond]
        })
        df_all.append(df)
    if not df_all:
        print("No data to plot for AUC bar.")
        return
    df_combined = pd.concat(df_all, ignore_index=True)

    ax = sns.barplot(x='Condition', y='AUC', data=df_combined, capsize=0.1, palette='Set2', estimator=np.mean, errorbar='se', edgecolor='0.2')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.xlabel(f"{i}", weight='bold')
    plt.ylabel("AUC", weight='bold')
    plt.title("AUC ", weight='bold')
    plt.xticks(weight='bold')
    plt.yticks(weight='bold')
    # Remove redundant legend call (no labeled items)
    plt.tight_layout()

    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/svg/Barnes/auc/{action}{i}.png')


def plot_latency(all_latency, i, j, looptype, action="", title="", save_path=None):
    # swarmplot of the total amount of time the mice experiment lasts 

    fig, ax = plt.subplots(figsize=(5, 4))  # set figure size
    df_all = []  # Initialize a list to collect DataFrames for each condition
    for cond in looptype[1]: 
        if all_latency[i][cond]:
            list_vals = [a for a in all_latency[i][cond]]
        else:
            print(f"Skipping {i}-{cond}: Missing data")
            continue
        latency = np.stack(list_vals)
        mean = np.mean(latency, axis=0)
        error = sem(latency, axis=0)
        df = pd.DataFrame({
            'Latency': mean,
            'Condition': [cond]
        })
        df_all.append(df)

    df_combined = pd.concat(df_all, ignore_index=True)

    sns.swarmplot(x='Condition', y='Latency', data=df_combined, ax=ax, color='skyblue', alpha=0.7)
    sns.barplot(x='Condition', y='Latency', data=df_combined, ax=ax, capsize=0.1, palette='Set2', estimator=np.mean, errorbar='se', edgecolor='0.2')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.xticks(weight='bold')
    plt.yticks(weight='bold')
    plt.xlabel(f"{i}", weight='bold')
    plt.ylabel("Latency (s)", weight='bold')
    plt.title(title if title else f"Latency {i} - {j}", weight='bold')
    # Remove redundant legend call (no labeled items)
    plt.tight_layout()

    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/svg/Barnes/latency/{action}{i}{j}.png')

    # Add text annotation for latency
   

    # Add a horizontal line at y=0
    ax.axhline(0, color='black', linestyle='--')

def plot_daily_summary_bar(all_data, days, unit, action="", save_path=None):
    """
    Plots a bar graph summarizing data over days, averaging over phases.
    Each day will be a group on the x-axis, with bars for 'Escape Hole' and 'Non-Escape Hole'.
    """
    df_all = []
    for day in days:
        if day not in all_data:
            continue

        # Collect all session means for a given day across all phases
        day_aucs_a = []
        day_aucs_b = []
        for phase in all_data[day]:
            day_aucs_a.extend(all_data[day][phase]['A'])
            day_aucs_b.extend(all_data[day][phase]['B'])

        # Create a DataFrame for each value, not the mean
        if day_aucs_a:
            temp_df_a = pd.DataFrame({
                'Value': day_aucs_a,
                'Day': day,
                'Object': 'Escape Hole'
            })
            df_all.append(temp_df_a)
        if day_aucs_b:
            temp_df_b = pd.DataFrame({
                'Value': day_aucs_b,
                'Day': day,
                'Object': 'Non-Escape Hole'
            })
            df_all.append(temp_df_b)

    if not df_all:
        print("No data to plot for daily summary.")
        return

    df_combined = pd.concat(df_all, ignore_index=True)

    # Print the full DataFrame with all values
    print(f"--- Data for {unit} (All Values) ---")
    print(df_combined.to_string())

    # Print the averaged data
    print(f"\n--- Data for {unit} (Averaged) ---")
    averaged = df_combined.groupby(['Day', 'Object']).agg(mean=('Value', 'mean')).reset_index()
    print(averaged)
    if False:
        averaged.to_csv(f"/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/csv/{unit}_averaged.csv", index=False)
        df_combined.to_csv(f"/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/csv/{unit}.csv", index=False)

    plt.figure(figsize=(10, 6))
    # Plot the bar plot for the mean and error
    ax = sns.barplot(x='Day', y='Value', hue='Object', data=df_combined, palette='Set2', capsize=0.1, errorbar='se')

    ax.spines[['top', 'right']].set_visible(False)
    plt.xlabel("Day", weight='bold')
    plt.ylabel(unit, weight='bold')
    plt.title(f"{unit}", weight='bold')
    plt.xticks(rotation=45, ha='right', weight='bold')
    plt.tight_layout()


def plot_total_events(all_events, i, j, action="", title="", save_path=None):

    labels = ['Object A', 'Object B', 'Both']
    
    totala = np.mean(all_events[i][j]['A'])
    totalb = np.mean(all_events[i][j]['B'])
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
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/images/events/total_events{action}{i}{j}.png')


def plot_events_per_second(all_rates, i, j, action="",title="", save_path=None):

    plt.figure(figsize=(5, 4))
    df_all = []  # Initialize a list to collect DataFrames for each condition
    for cond in all_rates[i]:
        if all_rates[i][cond]['A'] or all_rates[i][cond]['B']:
            a_list = [a for a in all_rates[i][cond]['A']]
            b_list = [b for b in all_rates[i][cond]['B']]
        else:
            print(f"Skipping {i}-{cond}: Missing data")
            continue
        # Get event rates for A and B
        if len(a_list) == 0 or len(b_list) == 0:
            print(f"Skipping {i}-{cond}: Empty A or B list after filtering")
            continue
        a_rates = np.stack(a_list)
        b_rates = np.stack(b_list)
        combined = (a_rates + b_rates) / 2
        mean = np.mean(combined, axis=0)
        error = sem(combined, axis=0)
        df = pd.DataFrame({
            'Event Rate': mean,
            'Condition': [cond]
        })
        df_all.append(df)
    if not df_all:
        print("No data to plot for events per second.")
        return
    df_combined = pd.concat(df_all, ignore_index=True)

    ax = sns.barplot(x='Condition', y='Event Rate', data=df_combined, capsize=0.5, palette='Set2', estimator=np.mean, errorbar='se', edgecolor='0.2')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(weight='bold')
    plt.yticks(weight='bold')
    plt.xlabel(f"{i}")
    plt.ylabel("Events Per Minute", weight='bold')
    plt.title(f"Events per Minute {i}", weight='bold')
    # Remove redundant legend call (no labeled items)
    plt.tight_layout()

    if save_path:
        plt.savefig(f'/Volumes/basulab/basulabspace/TS/svg/Barnes/events/rate{action}{i}.png')

# Helper function for saving figures
def save_figure(fig, save_path):
    if save_path:
        fig.savefig(save_path)


def plot_combines(all_data, event_type, max_value, mouse_ids, phases, mouse_log=None, action="", title="", save_path=None, normalize=False, combined=None):

    # Define groups of days to compare
    group1 = ["D1", "D2", "D3", "D4", "D5", "D6"]
    group2 = ["D7", "D8"]

    num_mice = len(mouse_ids)



    def collect_group_data(days, storage):
        for day in days:
            if day not in all_data:
                continue
            for phase in phases:
                if phase not in all_data[day]:
                    continue
                
                if "All_a" in all_data[day][phase] and "All_b" in all_data[day][phase]:
                    a_list = all_data[day][phase]["All_a"]
                    b_list = all_data[day][phase]["All_b"]

                    current_ids = []
                    if mouse_log and day in mouse_log:
                        current_ids = [mid for mid, mphase in mouse_log[day] if mphase == phase]

                    if current_ids:
                        for k, mid in enumerate(current_ids):
                            if k < len(a_list):
                                clean_id = mid.replace("MHF", "")
                                if clean_id in mouse_ids:
                                    idx = mouse_ids.index(clean_id)
                                    # Collect both A and B values
                                    if len(a_list[k]) > 0:
                                        storage[idx].extend(a_list[k])
                                    if len(b_list[k]) > 0:
                                        storage[idx].extend(b_list[k])
                    else:
                        # Fallback logic if no mouse_log provided
                        count = min(len(a_list), len(b_list), num_mice)
                        for k in range(count):
                            if len(a_list[k]) > 0:
                                storage[k].extend(a_list[k])
                            if len(b_list[k]) > 0:
                                storage[k].extend(b_list[k])

    def collect_separate_data(days, storage_escape, storage_non_escape):
        for day in days:
            if day not in all_data:
                continue
            for phase in phases:
                if phase not in all_data[day]:
                    continue
                
                if "All_a" in all_data[day][phase] and "All_b" in all_data[day][phase]:
                    a_list = all_data[day][phase]["All_a"]
                    b_list = all_data[day][phase]["All_b"]

                    current_ids = []
                    if mouse_log and day in mouse_log:
                        current_ids = [mid for mid, mphase in mouse_log[day] if mphase == phase]

                    if current_ids:
                        for k, mid in enumerate(current_ids):
                            if k < len(a_list):
                                clean_id = mid.replace("MHF", "")
                                if clean_id in mouse_ids:
                                    idx = mouse_ids.index(clean_id)
                                    # Collect A values for escape hole and B values for non-escape hole
                                    if len(a_list[k]) > 0:
                                        storage_escape[idx].extend(a_list[k])
                                    if len(b_list[k]) > 0:
                                        storage_non_escape[idx].extend(b_list[k])
                    else:
                        # Fallback logic if no mouse_log provided
                        count = min(len(a_list), len(b_list), num_mice)
                        for k in range(count):
                            if len(a_list[k]) > 0:
                                storage_escape[k].extend(a_list[k])
                            if len(b_list[k]) > 0:
                                storage_non_escape[k].extend(b_list[k])

    if combined:

                # Initialize storage per mouse
        g1_data = [[] for _ in range(num_mice)]
        g2_data = [[] for _ in range(num_mice)]

        # Collect data for each group
        collect_group_data(group1, g1_data)     # D1-D6
        collect_group_data(group2, g2_data)     # D7-D8

        # Calculate means
        g1_means = []
        g2_means = []

        for i in range(num_mice):       
            val1 = np.nanmean(g1_data[i]) if g1_data[i] else np.nan
            val2 = np.nanmean(g2_data[i]) if g2_data[i] else np.nan
            g1_means.append(val1)
            g2_means.append(val2)

        if normalize:
            g1_norm = []
            g2_norm = []
            for i in range(num_mice):
                total = g1_means[i] + g2_means[i]
                if total > 0 and not np.isnan(total):
                    g1_norm.append(g1_means[i] / total)
                    g2_norm.append(g2_means[i] / total)
                else:
                    g1_norm.append(np.nan)
                    g2_norm.append(np.nan)
            g1_means = g1_norm
            g2_means = g2_norm

        # Plotting
        df = pd.DataFrame({
            event_type: np.concatenate([g1_means, g2_means]),
            "Condition": ["Days 1-6"] * num_mice + ["Days 7-8"] * num_mice,
            "Mouse": mouse_ids * 2
        })

        fig, ax = plt.subplots(figsize=(3, 4))

        sns.barplot(data=df, x="Condition", y=event_type, ax=ax, capsize=0.5, edgecolor='0.2', lw=2.5, errwidth=2.5, palette=['crimson', 'mistyrose'], estimator=np.mean, errorbar='se')

        # Draw swarmplot
        swarm = sns.swarmplot(data=df, x="Condition", y=event_type, s=8, ax=ax, palette=["lightcoral", "lightpink"])

        # Add outlines to each point
        for coll in swarm.collections:
            coll.set_edgecolor('0.2')
            coll.set_linewidth(1.0)

        for i in range(len(mouse_ids)):
            mouse = mouse_ids[i]
            x = df[(df['Mouse'] == mouse) & (df['Condition'] == "Days 1-6")][event_type].values
            y = df[(df['Mouse'] == mouse) & (df['Condition'] == "Days 7-8")][event_type].values
            
            if len(x) > 0 and len(y) > 0 and not np.isnan(x[0]) and not np.isnan(y[0]):
                ax.plot(["Days 1-6", "Days 7-8"], [x, y], color="black", alpha=0.6)

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

        if title:
            ax.set_title(title, fontsize=14, weight='bold', color='0.2')
        plt.xlabel('')
        plt.tight_layout()
        if save_path:
            import os
            norm_suffix = "_normalized" if normalize else ""
            action_suffix = "entrance" if action else "exit"
            out_dir = f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/event_bar/{event_type}'
            os.makedirs(out_dir, exist_ok=True)
            
            df.to_csv(f'{out_dir}/combined_days_{norm_suffix}{action_suffix}.csv', index=True)
            plt.savefig(f'{out_dir}/combined_days_{norm_suffix}{action_suffix}.svg', format='svg')

    else:

            # Initialize storage per mouse
        g1_data_escape = [[] for _ in range(num_mice)]
        g1_data_non_escape = [[] for _ in range(num_mice)]
        g2_data_escape = [[] for _ in range(num_mice)]
        g2_data_non_escape = [[] for _ in range(num_mice)]

        collect_separate_data(group1, g1_data_escape, g1_data_non_escape)     # D1-D6
        collect_separate_data(group2, g2_data_escape, g2_data_non_escape)     # D7-D8

        # Calculate means
        g1_means_escape = []
        g1_means_non_escape = []
        g2_means_escape = []
        g2_means_non_escape = []

        for i in range(num_mice):
            val1 = np.nanmean(g1_data_escape[i]) if g1_data_escape[i] else np.nan
            val2 = np.nanmean(g1_data_non_escape[i]) if g1_data_non_escape[i] else np.nan
            val3 = np.nanmean(g2_data_escape[i]) if g2_data_escape[i] else np.nan
            val4 = np.nanmean(g2_data_non_escape[i]) if g2_data_non_escape[i] else np.nan
            g1_means_escape.append(val1)
            g1_means_non_escape.append(val2)
            g2_means_escape.append(val3)
            g2_means_non_escape.append(val4)
        
        if normalize:
            g1_escape_norm = []
            g1_non_escape_norm = []
            g2_escape_norm = []
            g2_non_escape_norm = []

            for i in range(num_mice):
                total_escape = g1_means_escape[i] + g2_means_escape[i]
                total_non_escape = g1_means_non_escape[i] + g2_means_non_escape[i]
                if total_escape > 0 and total_non_escape > 0 and not np.isnan(total_escape) and not np.isnan(total_non_escape):
                    g1_escape_norm.append(g1_means_escape[i] / total_escape)
                    g2_escape_norm.append(g2_means_escape[i] / total_escape)
                    g1_non_escape_norm.append(g1_means_non_escape[i] / total_non_escape)
                    g2_non_escape_norm.append(g2_means_non_escape[i] / total_non_escape)
                else:
                    g1_escape_norm.append(np.nan)
                    g2_escape_norm.append(np.nan)
                    g1_non_escape_norm.append(np.nan)
                    g2_non_escape_norm.append(np.nan)
            g1_means_escape = g1_escape_norm
            g1_means_non_escape = g1_non_escape_norm
            g2_means_escape = g2_escape_norm
            g2_means_non_escape = g2_non_escape_norm

        # Plotting
        df = pd.DataFrame({
            event_type: np.concatenate([g1_means_escape, g1_means_non_escape, g2_means_escape, g2_means_non_escape]),
            "Condition": (["Days 1-6 Escape Hole"] * num_mice) + (["Days 1-6 Non-Escape Hole"] * num_mice) + (["Days 7-8 Escape Hole"] * num_mice) + (["Days 7-8 Non-Escape Hole"] * num_mice),
            "Mouse": mouse_ids * 4
        })

        fig, ax = plt.subplots(figsize=(3, 4))

        sns.barplot(data=df, x="Condition", y=event_type, ax=ax, capsize=0.5, edgecolor='0.2', lw=2.5, errwidth=2.5, palette=['crimson', 'lightcoral', 'mistyrose', 'lightpink'], estimator=np.mean, errorbar='se')
        # Draw swarmplot
        swarm = sns.swarmplot(data=df, x="Condition", y=event_type, s=8, ax=ax, palette=["lightcoral", "salmon", "lightpink", "mistyrose"])
        # Add outlines to each point
        for coll in swarm.collections:
            coll.set_edgecolor('0.2')
            coll.set_linewidth(1.0)
        for i in range(len(mouse_ids)):
            mouse = mouse_ids[i]
            x = df[(df['Mouse'] == mouse) & (df['Condition'] == "Days 1-6 Escape Hole")][event_type].values
            y = df[(df['Mouse'] == mouse) & (df['Condition'] == "Days 7-8 Escape Hole")][event_type].values
            
            if len(x) > 0 and len(y) > 0 and not np.isnan(x[0]) and not np.isnan(y[0]):
                ax.plot(["Days 1-6 Escape Hole", "Days 7-8 Escape Hole"], [x, y], color="black", alpha=0.6)

            x_non_escape = df[(df['Mouse'] == mouse) & (df['Condition'] == "Days 1-6 Non-Escape Hole")][event_type].values
            y_non_escape = df[(df['Mouse'] == mouse) & (df['Condition'] == "Days 7-8 Non-Escape Hole")][event_type].values
            
            if len(x_non_escape) > 0 and len(y_non_escape) > 0 and not np.isnan(x_non_escape[0]) and not np.isnan(y_non_escape[0]):
                ax.plot(["Days 1-6 Non-Escape Hole", "Days 7-8 Non-Escape Hole"], [x_non_escape, y_non_escape], color="black", alpha=0.6)
        for axis in ['bottom', 'left']:
            ax.spines[axis].set_linewidth(2.5)
            ax.spines[axis].set_color('0.2')
        ax.tick_params(axis='x', labelrotation=45)

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
        if title:
            ax.set_title(title, fontsize=14, weight='bold', color='0.2')
        plt.xlabel('')
        plt.tight_layout()
        if save_path:
            import os
            norm_suffix = "_normalized" if normalize else ""
            action_suffix = "entrance" if action else "exit"
            out_dir = f'/Volumes/basulab/basulabspace/TS/Figures/svg/Barnes/event_bar/{event_type}'
            os.makedirs(out_dir, exist_ok=True)
            
            df.to_csv(f'{out_dir}/separate_days_{norm_suffix}{action_suffix}.csv', index=True)
            plt.savefig(f'{out_dir}/separate_days_{norm_suffix}{action_suffix}.svg', format='svg')