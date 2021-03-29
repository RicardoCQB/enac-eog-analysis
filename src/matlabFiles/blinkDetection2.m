% This code imports the ALLEEG as EOGh and EOGv for it to be used in the
% eogert_offline algorithm

% The index of the pre processed EEGLAB dataset
x = 2;

EOGh = ALLEEG(x).data(5,:); % 5 car les données EOG pour l'axe horizontal sont dans le channel 5
EOGv = ALLEEG(x).data(6,:); % 6 car les données EOG pour l'axe horizontal sont dans le channel 6

EOGh1 = double(EOGh);
EOGv1 = double(EOGv);

EOGh = EOGh1;
EOGv = EOGv1;

fs = 2048;