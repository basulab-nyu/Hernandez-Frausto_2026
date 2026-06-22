
function [Events]=event_analysis_no_behavior(Events, Imaging, options)

%% Import data

% standard deviation of noise
options.STD_off=Events.STD_noise;
options.restricted=Events.options.restricted;

%Calcium trace
if Imaging.options.msbackadj== true && options.restricted==true
C_df=Imaging.trace_restricted_baselinesub;  
elseif Imaging.options.msbackadj== true && options.restricted==false
C_df=Imaging.trace_baselinesub;
elseif Imaging.options.msbackadj== false && options.restricted==true
C_df=Imaging.trace_restricted;
elseif Imaging.options.msbackadj== false && options.restricted==false
C_df=Imaging.trace; 
end

%Time 
if options.restricted==true
Cdf_time=Imaging.time_restricted;
elseif options.restricted==false
Cdf_time=Imaging.time;
end

%Events
onset_offset{1}=Events.onset_offset;
% onset_offset{2}=Events.Run.run_onset_offset;
% onset_offset{3}=Events.NoRun.norun_onset_offset;
onset_binary{1}=Events.onset_binary; 
% onset_binary{2}=Events.Run.run_onset_binary;
% onset_binary{3}=Events.NoRun.norun_onset_binary;
onset_ones{1}=Events.onset_ones; 
% onset_ones{2}=Events.Run.run_onset_ones;
% onset_ones{3}=Events.NoRun.norun_onset_ones;
mean_fr=mean(diff(Cdf_time));
rec_dur{1}=(Cdf_time(end)-Cdf_time(1))/60;
% rec_dur{2}=sum(Behavior.run_ones)/(1/mean_fr)/60;
% rec_dur{3}=rec_dur{1}-rec_dur{2};

%% Measure Ca2+ events properties 
for i=1
%     if isempty(cell2mat(onset_offset{i}))
%         continue
%     end
[Event_Properties{i}]=event_properties(C_df, onset_offset{i}, options);
end
%% Network properties
% for i=1
% %     if isempty(cell2mat(onset_offset{i}))
% %         continue
% %     end
% [Network_Properties{i}] = network_properties(Event_Properties{i},rec_dur{i},C_df,Cdf_time, options);
% end
%% Distribution histogram and PCA
% for i=1:1
% [hist_events]= histo_events(Event_Properties{i},options);
% end

%% PCA 
%for i=1:3
%[PCA_Properties{i}]= PCA_analysis(Event_Properties{i} ,Network_Properties{i});
%end
%% Make structure
Events.properties=Event_Properties{1};
Events.options.properties=options;
% Events.Run.properties=Event_Properties{2};
%Events.NoRun.properties=Event_Properties{3};
% Network=Network_Properties{1};
% Network.Run=Network_Properties{2};
%Network.NoRun=Network_Properties{3};

% Figure.Histogram_Events=hist_events;
%PCA=PCA_Properties{1};
%PCA.Run=PCA_Properties{2};
%PCA.NoRun=PCA_Properties{3};
end

