from preprocessing import get_zscore_traces, process
from dataloader import load_session_data
from plotting import plot_dual_trace, plot_auc_bar, plot_total_events, plot_events_per_second
import numpy as np

def calculate_mean_trace(traces_a, traces_b, trunc_time):
    """
    Calculates the mean traces for A and B and the corresponding time axis
    without plotting.
    """
    time_interval = 0.01660136795
    truncate = round(trunc_time / time_interval)

    min_len = truncate
    if not traces_a.empty:
        min_len = min(min_len, traces_a.shape[0])
    if not traces_b.empty:
        min_len = min(min_len, traces_b.shape[0])

    mean_A = traces_a.mean(axis=1)[:min_len] if not traces_a.empty else np.array([])
    mean_B = traces_b.mean(axis=1)[:min_len] if not traces_b.empty else np.array([])

    start_time = -10
    time_axis = np.arange(start_time, start_time + min_len * time_interval, time_interval)[:min_len]

    return mean_A, mean_B, time_axis

def nornol_session(session, all_traces, all_aucs, all_events, all_rates, action="", zscore="", trunc_time="", group="", condition=""):            
            
            

            # Load and align data
            beh_dfs, signal, event, auc,  signal_trace, auc_means_a, auc_means_b, total_events_a, total_events_b, event_rate_a, event_rate_b = load_session_data(session)

            # Extract aligned traces for entrance/exit A/B
            traces_a, traces_b = process(beh_dfs, action)

        
            # Z-score if needed
            if zscore:
                traces_a, traces_b = get_zscore_traces(traces_a, traces_b, signal)


            mean_A, mean_B, time_axis = plot_dual_trace(traces_a, traces_b, group, condition, zscore, trunc_time, title=f"Calcium Trace {group} {condition}")


            # combine all the values from each session
            all_traces[group][condition]['A'].append(mean_A)
            all_traces[group][condition]['B'].append(mean_B)
            
            all_aucs[group][condition]['A'].append(auc_means_a)
            all_aucs[group][condition]['B'].append(auc_means_b)

            all_events[group][condition]['A'].append(total_events_a)
            all_events[group][condition]['B'].append(total_events_b)

            all_rates[group][condition]['A'].append(event_rate_a)
            all_rates[group][condition]['B'].append(event_rate_b)


def barnes_session(session, all_traces, all_aucs, all_events, all_rates, action="", zscore="", trunc_time=""):            
            
            

            # Load and align data
            beh_dfs, signal, event, auc,  signal_trace, auc_means_a, auc_means_b, total_events_a, total_events_b, event_rate_a, event_rate_b = load_session_data(session)

            # Extract aligned traces for entrance/exit A/B
            traces_a, traces_b = process(beh_dfs, action)

        
            # Z-score if needed
            if zscore:
                traces_a, traces_b = get_zscore_traces(traces_a, traces_b, signal)


            mean_A, mean_B, time_axis = plot_dual_trace(traces_a, traces_b,  zscore, trunc_time, group=False, condition=False, title=f"Calcium Trace")


            # combine all the values from each session
            all_traces['A'].append(mean_A)
            all_traces['B'].append(mean_B)
            
            all_aucs['A'].append(auc_means_a)
            all_aucs['B'].append(auc_means_b)

            all_events['A'].append(total_events_a)
            all_events['B'].append(total_events_b)

            all_rates['A'].append(event_rate_a)
            all_rates['B'].append(event_rate_b)
