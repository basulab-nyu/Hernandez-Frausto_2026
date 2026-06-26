# Behavioral Interaction Scripts

Provided are all the scripts used to generate the graphs as well as the data found for paper: _Behaviorally driven increased glutamatergic activity from lateral entorhinal cortex
to hippocampus supports object and spatial memory recall_


## Getting Started

### Dependencies 
- The matlab scripts being run require the peripherals provided within the df;f_ed folder
- In addition they are also pretty memory heavy 16gb+ would be preferred

### Executing the Program


Make sure the CalmAn-MATLAB and EventDetection folders are added to the MATLAB path 

Process the doric files through readdori.m into Matlab

Process Matlab files using doric_analysis.m, if the channel pathway remains absolute for the entirety of the files, use the automated however if otherwise make sure to check singularly in making sure Y = Data_Acquired(X).Data(Y).Data; is the right channel

event_fiber_photometry.m processes event related fiber photometric signals

export_csv.m to convert into csv for pipeline processing

#### Behavior Tracking

Two different Python scripts for two different mouse interactions once the behavior has been processed into csv from DeepLabCut

#### Python Pipeline for Alignment


- Manually adding session files through session_dict.py
- Otherwise utiilize session_dict_gen_remove.py 
- Everything should be easily ran through the respective notebooks



