%%%Parameters
R = 2; %Resistance CmH2Os/Liter
C_al = 0.033; %Alveolar Compliance V/P
C_Lungs = 40 %%%%%%PATIENT SPECIFIC%%%%%%%%
Va(1) = 3; %Initiel volumen 3L
Pa(1) = 5; %Initielt alveolært tryk 5CmH2O (PEEP)
Pinsp = 20; %Leveret Tryk



%Flow 
%Q = Pvent-Pal/R
flow=(Pinsp-Pa)/R; %Calculate flow at each timestep
dPa = (flow*timestep)/C; %Change in pressure (L/Timestep)/(L/P) =P/Timestep
Pa = Pa+dPa;


%Volume
Vdt = flow*timestep %Volume is flow over time
V=V+Vdt;


%%%Pao
%Pao = RQ+EV+PEEP
Pao = R*flow+(1/C)*V+PEEP;








