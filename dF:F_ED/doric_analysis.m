function doric_analysis()
    
    % if want to automate
    folder_path = uigetdir();
    
    mat_files = dir(fullfile(folder_path, '*.mat'));

    for i = 1:numel(mat_files)
        tic;
        fprintf('\nDoing analysis on %s\n', mat_files(i).name);
        
        file_path = fullfile(folder_path, mat_files(i).name);

        % Load the .mat file
        dataStruct = load(fullfile(folder_path, mat_files(i).name));
        vars_in_file = who('-file', file_path);




        % Check if Data_Acquired exists
        if isfield(dataStruct, 'Data_Acquired')
            try
                % Adjust indices [4,2] if needed
                Y = dataStruct.Data_Acquired(5).Data(1).Data;

                % Run CNMF
                [C_dec,C_df,F_dff,S,expDffMedZeroed,kernel] = single_source_CNMF(Y);

                % Append results back into same .mat file
                save(fullfile(folder_path, mat_files(i).name), ...
                     "kernel", "expDffMedZeroed", "S", "F_dff", "C_df", "C_dec", "Y", '-append');

                % Call your follow-up function (if it doesn’t need inputs)

                
                
                toc;
            catch ME
                warning('Error processing %s: %s', mat_files(i).name, ME.message);
            end
        else
            warning('Data_Acquired not found in %s', mat_files(i).name);
        end
    end
end 