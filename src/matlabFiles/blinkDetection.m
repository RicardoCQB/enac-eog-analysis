
% Transformation du signal en signal BIPOLAIRE
% soustraction de l'électrode Droite (1) - Gauche (2) sur l'axe horizontal
% soustraction de l'électrode Bas (3) - Haut (4) sur l'axe vertical
x = 1 % ALLEEG(NUMERO) parce que le fichier d'intérêt est dans la NUMERO eme ligne, mais A CHANGER selon !
line1 = ALLEEG(x).data(1,:) ; 
line2 = ALLEEG(x).data(2,:) ;
line3 = ALLEEG(x).data(3,:) ;
line4 = ALLEEG(x).data(4,:) ;

H_bi = line1 - line2 ;
V_bi = line3 - line4 ; 

% Ajoute donnees bipolaires a matrice
ALLEEG(x).data(5,:) = H_bi
ALLEEG(x).data(6,:) = V_bi
ALLEEG(x).nbchan = 6

