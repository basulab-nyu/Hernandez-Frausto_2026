
% Prompt user to select folder containing .doric files
folder_path = uigetdir();
doric_files = dir(fullfile(folder_path, '*.doric'));

if isempty(doric_files)
    disp('No .doric files found.');
    return;
end

for i = 1:length(doric_files)
    %--- Set up filename and workspace ---
    filename = fullfile(doric_files(i).folder, doric_files(i).name);


    fprintf('Processing %s...\n', doric_files(i).name);

    %--- Extract with your custom function ---
    Data_Acquired = ExtractDataAcquisition(filename);

    for k = 1:length(Data_Acquired)
        figure
        Datatmp = Data_Acquired(k);
        % plot(Datatmp.Data(2).Data, Datatmp.Data(1).Data) don't need plot
        % title(Datatmp.Name)
        %drawnow
         % close  % optional: remove if you want to inspect plots
    end

    %--- H5 manual read section ---
    try
        SignalIn = h5read(filename, '/DataAcquisition/FPConsole/Signals/Series0001/AnalogIn/AIN01');
        SignalInInfo = h5info(filename, '/DataAcquisition/FPConsole/Signals/Series0001/AnalogIn/AIN01').Attributes;

        TimeIn = h5read(filename, '/DataAcquisition/FPConsole/Signals/Series0001/AnalogIn/Time');
        TimeInInfo = h5info(filename, '/DataAcquisition/FPConsole/Signals/Series0001/AnalogIn/Time').Attributes;

        figure
        plot(TimeIn, SignalIn)
        title('AnalogIn Signal')
        drawnow
        close
    catch ME
        warning('Could not read AnalogIn data from %s\n%s', filename, ME.message);
    end

    %--- Save full workspace ---
    [path, name, ~] = fileparts(filename);
    save(fullfile(path, [name, '.mat']));

    fprintf('Saved workspace \n');

    %--- Optional: clear everything except loop controls ---
    clearvars -except folder_path doric_files i
end