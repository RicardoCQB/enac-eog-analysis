
% Transformation of the electrode's signals into bipolar signals
% Subtraction of the right electrode (1) - left (2) for the horizontal axis
% Subtraction of the lower electrode (3) - upper (4) for the vertical axis

% Number of the EEGLAB dataset to be read
x = 1;

% Each line corresponds to one electrode
line1 = ALLEEG(x).data(1,:); 
line2 = ALLEEG(x).data(2,:);
line3 = ALLEEG(x).data(3,:);
line4 = ALLEEG(x).data(4,:);

% Horizontal and Vertical EOG signal
H_bi = line1 - line2 ; % left - right electrode
V_bi = line4 - line3 ; % up - down electrode

% Adds the horizontal and vertical EOG to the eeglab dataset
ALLEEG(x).data(5,:) = H_bi;
ALLEEG(x).data(6,:) = V_bi;
ALLEEG(x).nbchan = 6;

