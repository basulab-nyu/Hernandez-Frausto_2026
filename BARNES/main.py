from plotting import (
    plot_combines, plot_daily_traces_separated, all_csv, all_csv_ab,
    day_combined_scatter, day_comp_scatter, plot_daily_summary_bar,
    plot_mouse_daily_traces, plot_daily_traces
)
from utils import calculate_mean_trace
import matplotlib.pyplot as plt 
import pandas as pd
import numpy as np

# Import our new extractor
from data_extractor import extract_data

print("hello")
# Customize
action = input("Entrance or Exit?").strip().lower() == "entrance"

zscore = True

print("testing")
looptype = False 
trunc_time = 20
Days = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]
Phases = ["PH1", "PH2", "PH3", "PH4", "TD"]

# --- DATA EXTRACTION ---
# The heavy lifting loop has been moved to data_extractor.py 
# to allow easy importing from Jupyter notebooks.
results = extract_data(action=action, zscore=zscore, trunc_time=trunc_time, 
                       looptype=looptype, Days=Days, Phases=Phases)

# Unpack the dictionaries for the plotting functions
all_traces = results["all_traces"]
all_amplitudes = results["all_amplitudes"]
all_durations = results["all_durations"]
all_widths = results["all_widths"]
all_aucs = results["all_aucs"]
all_events = results["all_events"]
all_rates = results["all_rates"]
all_latency = results["all_latency"]
all_aucs_rate = results["all_aucs_rate"]
all_aucs_pre_event = results["all_aucs_pre_event"]
all_aucs_post_event = results["all_aucs_post_event"]
all_aucrate_pre_event = results["all_aucrate_pre_event"]
all_aucrate_post_event = results["all_aucrate_post_event"]
all_width_pre_event = results["all_width_pre_event"]
all_width_post_event = results["all_width_post_event"]
all_amplitude_pre_event = results["all_amplitude_pre_event"]
all_amplitude_post_event = results["all_amplitude_post_event"]
all_duration_pre_event = results["all_duration_pre_event"]
all_duration_post_event = results["all_duration_post_event"]
mouse_description = results["mouse_description"]
time_axis = results["time_axis"]


# --- VERIFICATION ---
day_to_check = "D1"
if day_to_check in all_traces and False:
    print("\n--- Verification of all_traces['D1'] counts ---")
    total_traces = 0
    for phase in sorted(all_traces[day_to_check].keys()):
        num_traces = len(all_traces[day_to_check][phase]['A'])
        total_traces += num_traces
        print(f"Phase {phase}: Found {num_traces} traces.")
    print(f"Total traces collected for {day_to_check}: {total_traces}")
    print(f"Total labels collected in mouse_description['{day_to_check}']: {len(mouse_description.get(day_to_check, []))}")
    print("------------------------------------------------\n")


# --- PLOTTING ---
mice_ids = ['200', '201', '202', '203', '204', '205']

plt.close('all')

# Output iteration (Assuming 'i' was previously used in a loop, plotting functions will handle the iteration typically)
for i in Days:
    print(f"Generating outputs for {i}:")
    
    # CSV generation
    all_csv(all_aucs_rate, i, Phases, 1, unit="auc_rate", save_path=True, action=action, mouse_log=mouse_description)
    all_csv(all_rates, i, Phases, 1, unit="rate", save_path=False, action=action, mouse_log=mouse_description)
    all_csv_ab(all_aucs_rate, i, Phases, 1, unit="auc_rate", save_path=True, action=action, mouse_log=mouse_description)
    all_csv_ab(all_rates, i, Phases, 1, unit="rate", save_path=True, action=action, mouse_log=mouse_description)

    # Scatters
    save = True
    save1 = True
    day_combined_scatter(all_aucs_rate, i, Phases, 1, unit="auc_rate", save_path=save, action=action, mouse_log=mouse_description, ax1lim=(15,15), ax2lim=(20,20))
    day_combined_scatter(all_rates, i, Phases, 1, unit="rate", save_path=False, action=action)

    day_comp_scatter(all_aucs_rate, i, Phases, 1, unit="auc_rate", save_path=save1, action=action, mouse_log=mouse_description, ax1lim=(20,20), ax2lim=(20,50))
    day_comp_scatter(all_rates, i, Phases, 1, unit="rate", save_path=False, action=action, mouse_log=mouse_description)

plt.show()

exit()

# Additional plotting options (Unreachable code due to exit() above, left for user to toggle)
days_to_plot = Days

plot_daily_summary_bar(all_amplitudes, days_to_plot, unit="amplitude", action=action, save_path=False)
plot_daily_summary_bar(all_durations, days_to_plot, unit="duration", action=action, save_path=False)
plot_daily_summary_bar(all_widths, days_to_plot, unit="width", action=action, save_path=False)

# plot_daily_traces_separated(all_traces, mouse_description, days_to_plot, time_axis, zscore, action, save_path=True, phases=Phases)
# plot_daily_traces(all_traces, mouse_description, days_to_plot, time_axis, zscore, action, save_path=False)
# plot_mouse_daily_traces(all_traces, days_to_plot, time_axis, zscore, action, save_path=False)