function [C_df,F_dff,C_dec,S,expDffMedZeroed,kernel] = single_source_CNMF(Y)
    % [C_df,F_dff,C_dec,S,expDffMedZeroed,kernel] = single_source_CNMF(Y)
    %
    % INPUT
    % Y: Original trace
    %
    % OUTPUT
    % C_df: Original signal in df/f
    % F_dff: Detrended signal in df/f
    % C_dec: Inferred calcium trace, detrended - very similar to F_dff
    % S: Deconvolved signal, marking putative calcium events
    % expDffMedZeroed: Estimated trace from deconvolving and reconvolving
    %                   the detrended signal, with the median subtracted
    % kernel: Structure containing parameters used for deconvolving    
    
    %%
    FOV = [1,1]; % Image resolution 
    d1 = FOV(1);
    d2 = FOV(2);  
    tau = 1;                                          % std of gaussian kernel (size of neuron)
    K = 1;
    p = 2;                                            % order of autoregressive system (p = 0 no dynamics, p=1 just decay, p = 2, both rise and decay)
    merge_thr = 0.8;                                  % merging threshold
    options = CNMFSetParms(...
                           'd1',d1,'d2',d2,...                        % dimensions of datasets
                           'search_method','dilate','dist',3,...       % search locations when updating spatial components
                           'deconv_method','constrained_foopsi',...    % activity deconvolution method
                           'temporal_iter',2,...                       % number of block-coordinate descent steps
                           'fudge_factor',0.98,...                     % bias correction for AR coefficients
                           'merge_thr',merge_thr,...                    % merging threshold
                           'gSig',tau...
                           );
    
               
    Y = reshape(Y,1,1,[]);
    %%
    [P,Y] = preprocess_data(Y,p);
    A = 1;
    C = Y;
    
    [d1,d2,T] = size(Y);      % dimensions of dataset
    d = d1*d2;
    options.d1 = d1;
    options.d2 = d2;
    
    Yr = @(x) reshape(x,d,T);
    Y = Yr(Y);
    %%
    
    Ain = 1;
    Cin = Y;
    bin = 0;
    fin = zeros(size(Y));
    
    [A,b,Cin] = update_spatial_components(Y,Cin,fin,[Ain,bin],P,options);
    
    P.p = 0;    % set AR temporarily to zero for speed
    Y = single(Y);
%     A = single(full(A));
    b = single(b);
    Cin = single(Cin);
    fin = single(fin);
    
    [C,f,P,S,YrA] = update_temporal_components_jm(Y,A,b,Cin,fin,P,options);
    
    A2=A;
    b2=b;
    C2=C;
    P2=P;
    f2=f;
    S2=S;
    YrA2=YrA;

   %% Extract DF/F 
    fprintf('\nExtract DF/F\n');
    [C_df,~] = extract_DF_F(Y,A2,C2,P2,options);
    clear Y;
    %New df/f extract
    alpha=0.05;
    [expDffMedZeroed, expDff,dff,F,bf,dfc] = dff_extract_3(YrA, A2,C2, double(b2),f2,alpha);
    
    %% detrend fluorescence and extract DF/F values
    options.df_window = 1000; 
    [F_dff,F0] = detrend_df_f(A2,double(b),C2,f2,YrA2,options);
    
    %% deconvolve data
    nNeurons = size(F_dff,1);
    C_dec = zeros(size(F_dff));
    S = zeros(size(F_dff));
    kernels = cell(nNeurons,1);
    min_sp = 3;    % find spikes resulting in transients above min_sp x noise level
    for i = 1:nNeurons
        % Skip over traces that are just too weird. Otherwise deconvCa can 
        % get stuck in an infinite loop - Jason Moore, 8/27/19
        if(max(abs(F_dff(i,:)))>1000)
            continue;
        end
        [C_dec(i,:),S(i,:),kernels{i}] = deconvCa(F_dff(i,:), [], min_sp, true, false, [], 20, [], 0);
    end
   
    kernel = kernels{1};
end