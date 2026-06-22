from session_dict import session_dict
from preprocessing import get_zscore_traces, process, mouse_speed, combined_process
from non_interaction import extract_non_interaction_epochs, z_score_normalization
from dataloader import load_session_data, positional, plot_entire
from plotting import plot_dual_trace, plot_combines, plot_combined_auc, plot_events_per_second, plot_total_events, plot_auc_bar, plot_combined_traces, plot_combined_rate, plot_combined_events, plot_combined, histo, auc_rate_scatter, stationary_locomotion, save_traces_per_mouse, event_rate
from event_related import separate_traces_by_state, events_within_action_window
from plotting import get_random_non_interaction_trace, plot_trace_comparison, plot_interval_auc

import matplotlib.patches as patches
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



# Customize
action = input("Entrance or Exit?").strip().lower() == "entrance"
zscore = input("Z_score? Y or No").strip().lower() == "y"
save_file = input("Save? Y or No").strip().lower() == "y"
baseline_correction = True  # Whether to apply baseline correction


# how many total seconds from 10 seconds before interaction do we want
trunc_time = 20 



# initializing dictionary
from data_extractor import extract_all_data

extracted_data = extract_all_data(action=action, zscore=zscore, save_file=save_file, trunc_time=trunc_time)

all_traces = extracted_data['all_traces']
all_amplitudes = extracted_data['all_amplitudes']
all_durations = extracted_data['all_durations']
all_widths = extracted_data['all_widths']
all_aucs = extracted_data['all_aucs']
all_events = extracted_data['all_events']
all_rates = extracted_data['all_rates']
all_aucs_rate = extracted_data['all_aucs_rate']
all_aucs_pre_event = extracted_data['all_aucs_pre_event']
all_aucs_post_event = extracted_data['all_aucs_post_event']
all_aucrate_pre_event = extracted_data['all_aucrate_pre_event']
all_aucrate_post_event = extracted_data['all_aucrate_post_event']
all_width_pre_event = extracted_data['all_width_pre_event']
all_width_post_event = extracted_data['all_width_post_event']
all_amplitude_pre_event = extracted_data['all_amplitude_pre_event']
all_amplitude_post_event = extracted_data['all_amplitude_post_event']
all_duration_pre_event = extracted_data['all_duration_pre_event']
all_duration_post_event = extracted_data['all_duration_post_event']
all_mouse_ids = extracted_data['all_mouse_ids']
all_non_interaction_means = extracted_data['all_non_interaction_means']
time_axis = extracted_data['time_axis']

print("Data extraction complete.")
print("Note: Plotting functionality has been moved to notebooks/Barnes_Analysis_Pipeline.ipynb")
