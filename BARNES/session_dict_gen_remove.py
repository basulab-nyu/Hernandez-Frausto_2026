import os
import glob
import re

def build_session_dict(photometry_dir, behavior_dir):
    """
    Scans the directories for photometry and behavior files and automatically 
    constructs the session dictionaries by matching Mouse ID, Day, and Phase.
    """
    sessions = []
    
    # Regex to extract Mouse ID, Day, and Phase from the filename
    # Matches: "MHF200" or "M211", followed by "BARNES", then "D1", then "PH1" or "TD"
    pattern = re.compile(r'(MHF\d+|M\d+)_.*?BARNES(D\d+)(PH\d+|TD)')
    
    # 1. Gather all DeepLabCut behavior files and map them by their metadata
    behavior_files = glob.glob(os.path.join(behavior_dir, "**", "*DLC*_events.csv"), recursive=True)
    behavior_lookup = {}
    
    for b_file in behavior_files:
        match = pattern.search(os.path.basename(b_file))
        if match:
            mouse_id, day, phase = match.groups()
            behavior_lookup[(mouse_id, day, phase)] = b_file

    # 2. Gather all Photometry signal files and build the session map
    signal_files = glob.glob(os.path.join(photometry_dir, "**", "fb_signal_*.csv"), recursive=True)
    
    for sig_file in signal_files:
        match = pattern.search(os.path.basename(sig_file))
        if not match:
            continue
            
        mouse_id, day, phase = match.groups()
        time_file = sig_file.replace("fb_signal_", "fb_time_")
        event_file = sig_file.replace("fb_signal_", "fb_events_")
        
        # Try to find the matching behavior file using the metadata key
        beh_file = behavior_lookup.get((mouse_id, day, phase))
        
        # Add to dictionary if all files exist, ignoring index mismatches (0000 vs 0001)
        if beh_file and os.path.exists(time_file) and os.path.exists(event_file):
            sessions.append({
                'id': mouse_id,
                'day': day,
                'phase': phase,
                'time': time_file,
                'signal': sig_file,
                'event': event_file,
                'behavior': beh_file
            })

    return sessions


build_session_dict('')
if __name__ == "__main__":
    # Test block to verify it works standalone
    photometry_dir = '/Volumes/basulab/basulabspace/MHF/FIBER_PHOTOMETRY/2024/042024/BARNES/CNMF-ANALYSIS/MHF200CAMKIIRGECO'
    behavior_dir = '/Volumes/basulab/basulabspace/TS/Data/Barnes/barnes_behavior/200'
    found_sessions = build_session_dict(photometry_dir, behavior_dir)
    print(f"Found {len(found_sessions)} valid sessions.")
    print("Sample session entry:", found_sessions[0] if found_sessions else "No sessions found.")