
function [] = export_csv()
    folder_path = uigetdir();

    mat_file = dir(strcat(folder_path,'/*.mat'));
    for i=1:size(mat_file,1)
        tic;
        fprintf(strcat("\nexporting fb data from ",mat_file(i).name," to csv...\n"));
        fb_struct = load(strcat(mat_file(i).folder,'/',mat_file(i).name));

        if isfield(fb_struct, 'AUC')
            fb_auc = fb_struct.AUC;
            fb_auc = fb_auc';

            fb_signal = fb_struct.F_dff;
            fb_signal = fb_signal';

            fb_events = fb_struct.Events{1,1}.onset_offset_time{1,1}(:,1);

            fb_duration = fb_struct.duration;
            fb_duration = fb_duration';

            fb_width = fb_struct.width;
            fb_width = fb_width';

            fb_amplitude = fb_struct.amplitude;
            fb_amplitude = fb_amplitude';
            
            fb_time = fb_struct.t;
            fb_time = fb_time';




        
            writematrix(fb_auc,strcat(folder_path,'/fb_auc_',strrep(mat_file(i).name,'.mat',''),'.csv'));
            writematrix(fb_duration,strcat(folder_path,'/fb_duration_',strrep(mat_file(i).name,'.mat',''),'.csv'));
            writematrix(fb_width,strcat(folder_path,'/fb_width_',strrep(mat_file(i).name,'.mat',''),'.csv'));
            writematrix(fb_amplitude,strcat(folder_path,'/fb_amplitude_',strrep(mat_file(i).name,'.mat',''),'.csv'));
            writematrix(fb_events,strcat(folder_path,'/fb_events_',strrep(mat_file(i).name,'.mat',''),'.csv'));
            writematrix(fb_signal,strcat(folder_path,'/fb_signal_',strrep(mat_file(i).name,'.mat',''),'.csv'));
        writematrix(fb_time,strcat(folder_path,'/fb_time_',strrep(mat_file(i).name,'.mat',''),'.csv'));

            
            fprintf('\n');
            toc;
            fprintf('\ndone!!!\n');
        end



    end
end