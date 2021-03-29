% code pour importer les données de ALLEEG sous EOGh et EOHv afin de les
% entrer dans eogert_offline pour la détection des saccades
x = 2 % le nombre x est la ligne dans laquelle se trouvent les données dans ALLEEG
EOGh = ALLEEG(x).data(5,:); % 5 car les données EOG pour l'axe horizontal sont dans le channel 5
EOGv = ALLEEG(x).data(6,:); % 6 car les données EOG pour l'axe horizontal sont dans le channel 6

EOGh1 = double(EOGh);
EOGv1 = double(EOGv);

EOGh = EOGh1;
EOGv = EOGv1;

fs = 2048;