import pandas as pd
import numpy as np

from session_dict import barnes_session_dict
from preprocessing import get_zscore_traces, process, combined_process
from dataloader import load_session_data
from utils import calculate_mean_trace

def extract_data(action, zscore=True, trunc_time=20, looptype=False, Days=None, Phases=None):
    if Days is None:
        Days = ["D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8"]
    if Phases is None:
        Phases = ["PH1", "PH2", "PH3", "PH4", "TD"]

    days_in_phase = [Phases, Days]
    phases_in_day = [Days, Phases]

    active_loop = days_in_phase if looptype else phases_in_day

    all_traces = {}
    all_amplitudes = {}
    all_durations = {}
    all_widths = {}
    all_aucs = {}
    all_events = {}
    all_rates = {}
    all_latency = {}
    all_aucs_rate = {}
    all_aucs_pre_event = {}
    all_aucs_post_event = {}
    all_aucrate_pre_event = {}
    all_aucrate_post_event = {}
    all_width_pre_event = {}
    all_width_post_event = {}
    all_amplitude_pre_event = {}
    all_amplitude_post_event = {}
    all_duration_pre_event = {}
    all_duration_post_event = {}
    all_mouse_ids = {d: [] for d in Days}
    mouse_description = {}

    for i in active_loop[0]:
        all_traces.setdefault(i, {})
        all_amplitudes.setdefault(i, {})
        all_durations.setdefault(i, {})
        all_widths.setdefault(i, {})
        all_aucs.setdefault(i, {})
        all_events.setdefault(i, {})
        all_rates.setdefault(i, {})
        all_latency.setdefault(i, {})
        all_aucs_rate.setdefault(i, {})
        mouse_description.setdefault(i, [])
        all_aucs_pre_event.setdefault(i, {})
        all_aucs_post_event.setdefault(i, {})
        all_aucrate_pre_event.setdefault(i, {})
        all_aucrate_post_event.setdefault(i, {})
        all_width_pre_event.setdefault(i, {})
        all_width_post_event.setdefault(i, {})
        all_amplitude_pre_event.setdefault(i, {})
        all_amplitude_post_event.setdefault(i, {})
        all_duration_pre_event.setdefault(i, {})
        all_duration_post_event.setdefault(i, {})  

        mouse_ids_for_group = []

        for j in active_loop[1]:

            all_traces[i].setdefault(j, {})
            all_amplitudes[i].setdefault(j, {})
            all_durations[i].setdefault(j, {})
            all_widths[i].setdefault(j, {})
            all_aucs[i].setdefault(j, {})
            all_events[i].setdefault(j, {})
            all_rates[i].setdefault(j, {})
            all_latency[i].setdefault(j, [])
            all_aucs_rate[i].setdefault(j, {})
            all_aucs_pre_event[i].setdefault(j, {})
            all_aucs_post_event[i].setdefault(j, {})
            all_aucrate_pre_event[i].setdefault(j, {})
            all_aucrate_post_event[i].setdefault(j, {})
            all_width_pre_event[i].setdefault(j, {})
            all_width_post_event[i].setdefault(j, {})
            all_amplitude_pre_event[i].setdefault(j, {})
            all_amplitude_post_event[i].setdefault(j, {})
            all_duration_pre_event[i].setdefault(j, {})
            all_duration_post_event[i].setdefault(j, {})   
            
            all_events_to_save = []

            for key in ['A', 'B', "All_a", "All_b"]:
                all_traces[i][j].setdefault(key, [])
                all_amplitudes[i][j].setdefault(key, [])
                all_durations[i][j].setdefault(key, [])
                all_widths[i][j].setdefault(key, [])
                all_aucs[i][j].setdefault(key, [])
                all_events[i][j].setdefault(key, [])
                all_rates[i][j].setdefault(key, [])
                all_aucs_rate[i][j].setdefault(key, [])
                all_aucs_pre_event[i][j].setdefault(key, [])
                all_aucs_post_event[i][j].setdefault(key, [])
                all_aucrate_pre_event[i][j].setdefault(key, [])
                all_aucrate_post_event[i][j].setdefault(key, [])
                all_width_pre_event[i][j].setdefault(key, [])
                all_width_post_event[i][j].setdefault(key, [])
                all_amplitude_pre_event[i][j].setdefault(key, [])
                all_amplitude_post_event[i][j].setdefault(key, [])
                all_duration_pre_event[i][j].setdefault(key, [])
                all_duration_post_event[i][j].setdefault(key, [])      

            combined = pd.DataFrame()
            combined_esc = pd.DataFrame()

            for session in barnes_session_dict:
                if ((i == session['day'] and j == session['phase'])):
                    mouse_ids_for_group.append(session['id'])
                    # --- Verification Step ---
                    # print(f"{session['id']}, Session Day: {session['day']}, Session Phase: {session['phase']}")
                    
                    data = load_session_data(session, save_file=False)
                    mouse_description[i].append((session['id'], session['phase']))

                    traces_a, traces_b = process(data["beh_dfs"], action, value="df/f")
                    auc_a, auc_b = process(data["eve_dfs"], action, value="auc")
                    auc_rate_a, auc_rate_b = process(data["eve_dfs"], action, value="auc_rate")
                    amp_a, amp_b = process(data["eve_dfs"], action, value="amplitude")

                    #combined dataframes with all different events
                    event_df = combined_process(data["eve_dfs"], action)

                    if not event_df.empty:
                        event_df['mouse_id'] = session['id']
                        all_events_to_save.append(event_df)

                    # Process the new pre- and post-event AUC data
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

                    if zscore:
                        traces_a, traces_b = get_zscore_traces(traces_a, traces_b, data["signal"])
                    
                    mean_a, mean_b, time_axis = calculate_mean_trace(traces_a, traces_b, trunc_time)
                    
                    # add the values to the dictionaries we've created
                    all_traces[i][j]['A'].append(mean_a)
                    all_traces[i][j]['B'].append(mean_b)

                    all_amplitudes[i][j]['A'].extend(data["amplitude_means"][0])
                    all_amplitudes[i][j]['B'].extend(data["amplitude_means"][1])
                    
                    all_durations[i][j]['A'].extend(data["duration_means"][0])
                    all_durations[i][j]['B'].extend(data["duration_means"][1])

                    all_widths[i][j]['A'].extend(data["width_means"][0])
                    all_widths[i][j]['B'].extend(data["width_means"][1])
                    
                    all_aucs[i][j]['A'].extend(data["auc_means"][0])
                    all_aucs[i][j]['B'].extend(data["auc_means"][1])

                    all_aucs_rate[i][j]['A'].extend(data["auc_rate_means"][0])
                    all_aucs_rate[i][j]['B'].extend(data["auc_rate_means"][1])

                    all_aucs[i][j]['All_a'].append(auc_a.mean().values.flatten())
                    all_aucs[i][j]['All_b'].append(auc_b.mean().values.flatten())

                    all_aucs_rate[i][j]['All_a'].append(auc_rate_a.mean().values.flatten())
                    all_aucs_rate[i][j]['All_b'].append(auc_rate_b.mean().values.flatten())

                    all_amplitudes[i][j]['All_a'].append(amp_a.mean().values.flatten())
                    all_amplitudes[i][j]['All_b'].append(amp_b.mean().values.flatten())

                    all_events[i][j]['All_a'].append(np.array([data["total_events"][0]]))
                    all_events[i][j]['All_b'].append(np.array([data["total_events"][1]]))

                    all_rates[i][j]['All_a'].append(np.array([data["event_rate"][0]]))
                    all_rates[i][j]['All_b'].append(np.array([data["event_rate"][1]]))
                    
                    # Store the new pre- and post-event AUC values
                    all_aucs_pre_event[i][j]['All_a'].append(auc_a_pre.mean().values.flatten())
                    all_aucs_pre_event[i][j]['All_b'].append(auc_b_pre.mean().values.flatten())
                    all_aucs_post_event[i][j]['All_a'].append(auc_a_post.mean().values.flatten())
                    all_aucs_post_event[i][j]['All_b'].append(auc_b_post.mean().values.flatten())

                    all_aucrate_pre_event[i][j]['All_a'].append(aucrate_a_pre.mean().values.flatten())
                    all_aucrate_pre_event[i][j]['All_b'].append(aucrate_b_pre.mean().values.flatten())
                    all_aucrate_post_event[i][j]['All_a'].append(aucrate_a_post.mean().values.flatten())
                    all_aucrate_post_event[i][j]['All_b'].append(aucrate_b_post.mean().values.flatten())

                    all_width_pre_event[i][j]['All_a'].append(width_a_pre.mean().values.flatten())
                    all_width_pre_event[i][j]['All_b'].append(width_b_pre.mean().values.flatten())
                    all_width_post_event[i][j]['All_a'].append(width_a_post.mean().values.flatten())
                    all_width_post_event[i][j]['All_b'].append(width_b_post.mean().values.flatten())

                    all_amplitude_pre_event[i][j]['All_a'].append(amplitude_a_pre.mean().values.flatten())
                    all_amplitude_pre_event[i][j]['All_b'].append(amplitude_b_pre.mean().values.flatten())
                    all_amplitude_post_event[i][j]['All_a'].append(amplitude_a_post.mean().values.flatten())
                    all_amplitude_post_event[i][j]['All_b'].append(amplitude_b_post.mean().values.flatten())

                    all_duration_pre_event[i][j]['All_a'].append(duration_a_pre.mean().values.flatten())
                    all_duration_pre_event[i][j]['All_b'].append(duration_b_pre.mean().values.flatten())
                    all_duration_post_event[i][j]['All_a'].append(duration_a_post.mean().values.flatten())
                    all_duration_post_event[i][j]['All_b'].append(duration_b_post.mean().values.flatten())

                    all_events[i][j]['A'].append(data["total_events"][0])
                    all_events[i][j]['B'].append(data["total_events"][1])

                    all_rates[i][j]['A'].append(data["event_rate"][0])
                    all_rates[i][j]['B'].append(data["event_rate"][1])

            all_mouse_ids[i] = mouse_ids_for_group

    time_axis = calculate_mean_trace(pd.DataFrame(), pd.DataFrame(), trunc_time)[2]

    return {
        "all_traces": all_traces,
        "all_amplitudes": all_amplitudes,
        "all_durations": all_durations,
        "all_widths": all_widths,
        "all_aucs": all_aucs,
        "all_events": all_events,
        "all_rates": all_rates,
        "all_latency": all_latency,
        "all_aucs_rate": all_aucs_rate,
        "all_aucs_pre_event": all_aucs_pre_event,
        "all_aucs_post_event": all_aucs_post_event,
        "all_aucrate_pre_event": all_aucrate_pre_event,
        "all_aucrate_post_event": all_aucrate_post_event,
        "all_width_pre_event": all_width_pre_event,
        "all_width_post_event": all_width_post_event,
        "all_amplitude_pre_event": all_amplitude_pre_event,
        "all_amplitude_post_event": all_amplitude_post_event,
        "all_duration_pre_event": all_duration_pre_event,
        "all_duration_post_event": all_duration_post_event,
        "all_mouse_ids": all_mouse_ids,
        "mouse_description": mouse_description,
        "time_axis": time_axis
    }
