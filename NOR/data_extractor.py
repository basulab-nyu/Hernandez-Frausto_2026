import pandas as pd
import numpy as np

from session_dict import session_dict
from preprocessing import get_zscore_traces, process, mouse_speed, combined_process
from non_interaction import extract_non_interaction_epochs, z_score_normalization
from dataloader import load_session_data, positional

def extract_all_data(action=True, zscore=True, save_file=False, trunc_time=20):
    # initializing dictionaries
    all_traces = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_amplitudes = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_durations = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_widths = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_aucs = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_events = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_rates = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_aucs_rate = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}

    all_aucs_pre_event = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_aucs_post_event = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_aucrate_pre_event = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_aucrate_post_event = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_width_pre_event = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_width_post_event = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_amplitude_pre_event = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_amplitude_post_event = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_duration_pre_event = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}
    all_duration_post_event = {'NOR': {'FAM': {}, 'NOV': {}}, 'NOL': {'FAM': {}, 'NOV': {}}}

    all_mouse_ids = {'NOR': [], 'NOL': []}
    all_non_interaction_means = {'NOR': {'FAM': [], 'NOV': []}, 'NOL': {'FAM': [], 'NOV': []}}

    time_axis = None

    for group in ['NOR', 'NOL']:
        if group == 'NOL':
            continue  # Replaces exit() to allow function to complete or return if needed
        mouse_ids_for_group = []
        for idx, condition in enumerate(['FAM', 'NOV']):

            all_events_to_save = []

            for key in ['A', 'B', 'All_a', 'All_b']:
                all_traces[group][condition].setdefault(key, [])
                all_amplitudes[group][condition].setdefault(key, [])
                all_durations[group][condition].setdefault(key, [])
                all_widths[group][condition].setdefault(key, [])
                all_aucs[group][condition].setdefault(key, [])
                all_events[group][condition].setdefault(key, [])
                all_rates[group][condition].setdefault(key, [])
                all_aucs_rate[group][condition].setdefault(key, [])
                all_aucs_pre_event[group][condition].setdefault(key, [])
                all_aucs_post_event[group][condition].setdefault(key, [])
                all_aucrate_pre_event[group][condition].setdefault(key, [])
                all_aucrate_post_event[group][condition].setdefault(key, [])
                all_width_pre_event[group][condition].setdefault(key, [])
                all_width_post_event[group][condition].setdefault(key, [])
                all_amplitude_pre_event[group][condition].setdefault(key, [])
                all_amplitude_post_event[group][condition].setdefault(key, [])
                all_duration_pre_event[group][condition].setdefault(key, [])
                all_duration_post_event[group][condition].setdefault(key, [])              
                all_rates[group][condition].setdefault('All_a', [])
                all_rates[group][condition].setdefault('All_b', [])

            for idx, session in enumerate(session_dict[group][condition]):
                if condition == 'FAM': 
                    mouse_ids_for_group.append(session['id'])

                data = load_session_data(session, save_file, group, condition)
                
                # We call positional but don't explicitly require plotting it 
                positional(data['location'], data['signal_trace'], session, group, condition)

                traces_a, traces_b = process(data["beh_dfs"], action, value="df/f") 
                auc_a, auc_b = process(data["eve_dfs"], action, value="auc")
                event_df = combined_process(data["eve_dfs"], action)

                if not event_df.empty:
                    event_df['mouse_id'] = session['id']
                    all_events_to_save.append(event_df)

                auc_a_pre, auc_b_pre = process(data["eve_dfs_pre_event"], action, value="auc")
                auc_a_post, auc_b_post = process(data["eve_dfs_post_event"], action, value="auc")
                aucrate_a_pre, aucrate_b_pre = process(data["eve_dfs_pre_event"], action, value="auc_rate")
                aucrate_a_post, aucrate_b_post = process(data["eve_dfs_post_event"], action, value="auc_rate")
                width_a_pre, width_b_pre = process(data["eve_dfs_pre_event"], action, value="width")
                width_a_post, width_b_post = process(data["eve_dfs_post_event"], action, value="width")
                amplitude_a_pre, amplitude_b_pre = process(data["eve_dfs_pre_event"], action, value="amplitude")
                amplitude_a_post, amplitude_b_post = process(data["eve_dfs_post_event"], action, value="amplitude")
                duration_a_pre, duration_b_pre = process(data["eve_dfs_pre_event"], action, value="duration")
                duration_a_post, duration_b_post = process(data["eve_dfs_post_event"], action, value="duration")

                auc_rate_a, auc_rate_b = process(data["eve_dfs"], action, value="auc_rate")

                if zscore:
                    traces_a, traces_b = get_zscore_traces(traces_a, traces_b, data["signal"])

                # Calculate traces and time_axis logic (previously inside plot_dual_trace)
                time_interval = 0.01660136795
                truncate = round(trunc_time / time_interval) 
                mean_A = traces_a.mean(axis=1)[:truncate] 
                mean_B = traces_b.mean(axis=1)[:truncate] 
                start_time = -10
                time_axis = np.arange(start_time, start_time + len(mean_A) * time_interval, time_interval)[:truncate]

                # Store trace values
                all_traces[group][condition]['A'].append(mean_A)
                all_traces[group][condition]['B'].append(mean_B)

                all_amplitudes[group][condition]['A'].append(data["amplitude_means"][0])
                all_amplitudes[group][condition]['B'].append(data["amplitude_means"][1])
                
                all_durations[group][condition]['A'].append(data["duration_means"][0])
                all_durations[group][condition]['B'].append(data["duration_means"][1])

                all_widths[group][condition]['A'].append(data["width_means"][0])
                all_widths[group][condition]['B'].append(data["width_means"][1])
                
                all_aucs[group][condition]['A'].append(data["auc_means"][0])
                all_aucs[group][condition]['B'].append(data["auc_means"][1])

                all_aucs[group][condition]['All_a'].append(auc_a.mean().values.flatten())
                all_aucs[group][condition]['All_b'].append(auc_b.mean().values.flatten())

                all_aucs_rate[group][condition]['All_a'].append(auc_rate_a.mean().values.flatten())
                all_aucs_rate[group][condition]['All_b'].append(auc_rate_b.mean().values.flatten())
                
                all_aucs_pre_event[group][condition]['All_a'].append(auc_a_pre.mean().values.flatten())
                all_aucs_pre_event[group][condition]['All_b'].append(auc_b_pre.mean().values.flatten())
                all_aucs_post_event[group][condition]['All_a'].append(auc_a_post.mean().values.flatten())
                all_aucs_post_event[group][condition]['All_b'].append(auc_b_post.mean().values.flatten())

                all_aucrate_pre_event[group][condition]['All_a'].append(aucrate_a_pre.mean().values.flatten())
                all_aucrate_pre_event[group][condition]['All_b'].append(aucrate_b_pre.mean().values.flatten())
                all_aucrate_post_event[group][condition]['All_a'].append(aucrate_a_post.mean().values.flatten())
                all_aucrate_post_event[group][condition]['All_b'].append(aucrate_b_post.mean().values.flatten())

                all_width_pre_event[group][condition]['All_a'].append(width_a_pre.mean().values.flatten())
                all_width_pre_event[group][condition]['All_b'].append(width_b_pre.mean().values.flatten())
                all_width_post_event[group][condition]['All_a'].append(width_a_post.mean().values.flatten())
                all_width_post_event[group][condition]['All_b'].append(width_b_post.mean().values.flatten())

                all_amplitude_pre_event[group][condition]['All_a'].append(amplitude_a_pre.mean().values.flatten())
                all_amplitude_pre_event[group][condition]['All_b'].append(amplitude_b_pre.mean().values.flatten())
                all_amplitude_post_event[group][condition]['All_a'].append(amplitude_a_post.mean().values.flatten())
                all_amplitude_post_event[group][condition]['All_b'].append(amplitude_b_post.mean().values.flatten())

                all_duration_pre_event[group][condition]['All_a'].append(duration_a_pre.mean().values.flatten())
                all_duration_pre_event[group][condition]['All_b'].append(duration_b_pre.mean().values.flatten())
                all_duration_post_event[group][condition]['All_a'].append(duration_a_post.mean().values.flatten())
                all_duration_post_event[group][condition]['All_b'].append(duration_b_post.mean().values.flatten())

                all_events[group][condition]['A'].append(data["total_events"][0])
                all_events[group][condition]['B'].append(data["total_events"][1])

                all_rates[group][condition]['A'].append(data["event_rate"][0])
                all_rates[group][condition]['B'].append(data["event_rate"][1])
                all_rates[group][condition]['All_a'].append([data["event_rate"][0]])
                all_rates[group][condition]['All_b'].append([data["event_rate"][1]])

        all_mouse_ids[group] = mouse_ids_for_group
        print(f"Mouse IDs for {group}: {all_mouse_ids[group]}")

    return {
        'all_traces': all_traces,
        'all_amplitudes': all_amplitudes,
        'all_durations': all_durations,
        'all_widths': all_widths,
        'all_aucs': all_aucs,
        'all_events': all_events,
        'all_rates': all_rates,
        'all_aucs_rate': all_aucs_rate,
        'all_aucs_pre_event': all_aucs_pre_event,
        'all_aucs_post_event': all_aucs_post_event,
        'all_aucrate_pre_event': all_aucrate_pre_event,
        'all_aucrate_post_event': all_aucrate_post_event,
        'all_width_pre_event': all_width_pre_event,
        'all_width_post_event': all_width_post_event,
        'all_amplitude_pre_event': all_amplitude_pre_event,
        'all_amplitude_post_event': all_amplitude_post_event,
        'all_duration_pre_event': all_duration_pre_event,
        'all_duration_post_event': all_duration_post_event,
        'all_mouse_ids': all_mouse_ids,
        'all_non_interaction_means': all_non_interaction_means,
        'time_axis': time_axis,
    }
