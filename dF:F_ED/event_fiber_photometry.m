function [] = event_fiber_photometry()
    
    addpath(genpath('CaImAn-MATLAB'));
    addpath(genpath('EventDetection'));

    % choose folder and list .mat files
    folder_path = uigetdir();
    if isequal(folder_path,0)
        fprintf('No folder selected. Exiting.\n');
        return;
    end
    mat_files = dir(fullfile(folder_path, '*.mat'));



    % Loop through all .mat files in chosen folder
    for file_index = 1:numel(mat_files)
        tic;
        fprintf('\nDoing analysis on %s\n', mat_files(file_index).name);
        file_fullpath = fullfile(folder_path, mat_files(file_index).name);

        % Load the .mat file
        data = load(file_fullpath);

        %  expects variables F_dff and C_df 

        if ~isfield(data, 'F_dff') || ~isfield(data, 'C_df')
            warning('File %s does not contain required variables ''F_dff'' and ''C_df''. Skipping.', mat_files(file_index).name);
            continue;
        end


        baselineWindowSize = 150000;
        ITERATIONS = 2;
        SD_ONSET = 2;
        SD_OFFSET = 0.2;
        MIN_DURATION = 0.2;

        % Prepare Imaging struct
        dt = 1/2000;
        t = dt*(1:length(data.C_df));
        clear Imaging;
        Imaging{1}.trace = data.F_dff';
        Imaging{1}.time = t';
        Imaging{1}.time_restricted = t';
        Imaging{1}.trace_restricted = data.F_dff';
        I1 = Imaging;

        % Correct drifting baseline
        sessions = length(Imaging);
        options.msbackadj = 1;
        options.windwith = baselineWindowSize;
        options.dispfig = 0;
        for i = 1:sessions
            if options.msbackadj == true
                [Imaging{i}] = baselinesub(Imaging{i}, options);
            else
                Imaging{i}.options.msbackadj = 0;
            end
        end
        clear options;

        % Event detection options
        options.restricted = 1;
        options.iterations = ITERATIONS;
        options.SDOFF = SD_OFFSET;
        options.msbackadj = 1;
        options.SDON = SD_ONSET;
        options.mindurevent = MIN_DURATION;
        for i = 1:sessions
            [Events{i}] = detect_events2(Imaging{i}, options);
        end
        clear options;

        % Events analysis
        options.exclude = 0;
        options.mindist = 10;
        options.STD_pro = 2;
        for i = 1:sessions
            [Events{i}] = event_analysis_no_behavior(Events{i}, Imaging{i}, options);
        end
        clear options;

        % Plot and save figure
        clf;
        fig = figure('position',[50,75,1300,600]);
        subplot(1,2,1);
        plot(Imaging{1}.time, Imaging{1}.trace_baselinesub);
        hold on;
        plot(Events{1}.onset_offset_time{1}(:,1), ones(1,size(Events{1}.onset_offset{1},1)),'r.');
        plot(Events{1}.onset_offset_time{1}(:,2), ones(1,size(Events{1}.onset_offset{1},1)),'k.');
        xlabel('Time (s)');
        ylabel('df/f');

        amplitude = Events{1}.properties.amplitude{1};
        peak = Events{1}.properties.peak{1};
        meanVals = Events{1}.properties.mean{1};
        AUC = Events{1}.properties.AUC{1};
        width = Events{1}.properties.width{1}/2000;
        duration = Events{1}.properties.duration{1}/2000;

        subplot(3,4,3); hist(amplitude,50); title('Amplitude');
        subplot(3,4,4); hist(peak,50); title('Peak');
        subplot(3,4,7); hist(meanVals,50); title('Mean');
        subplot(3,4,8); hist(AUC,50); title('AUC');
        subplot(3,4,11); hist(width,50); title('Width');
        subplot(3,4,12); hist(duration,50); title('Duration');

        % Save figure into output folder
        [~, name, ~] = fileparts(mat_files(file_index).name);
        print(fullfile(out_folder, strcat('fig_', name, '.pdf')),'-dpdf','-r300','-bestfit');

        % Append results back to the original .mat file
        save(file_fullpath, "-append");

        close all;
        elapsed = toc;
        fprintf('Finished %s in %.2f seconds.\n', mat_files(file_index).name, elapsed);
    end
end
