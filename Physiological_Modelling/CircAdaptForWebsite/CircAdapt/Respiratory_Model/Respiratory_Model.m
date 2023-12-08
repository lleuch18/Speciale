%Unanswered Questions:
%%How to handle phases of breath cycle?
%We set a Ti and Te
%Ti is run at Δt intervals
%When mod(cnt_ti,Ti) = 0, we switch to Te and reset Ti
%Visa Verse when mod(cnt_te,Te) = 0

%%%REMEMBER
%Add mechanism to simulate patient initiated breath
%Memory Allocation



%3. Calculate Flow
%Q = Pao-Palv/R
flow=(Pao-Palv)/R; %Calculate flow at each timestep


%4. Calculate Palv
dPa = (flow*dT)/C; %Change in pressure (L/Timestep)/(L/P) =P/Timestep
Palv = Palv+dPalv;



%5. Calculate Volume
dV = flow*dT %Volume is flow over time
V=V+dV;

%6. Calculate Pao
dPao = R*flow+(1/C)*V;
Pao = Pao + dPao;

%7. Calculate Ppl




%%%%%%%%%%%%%%TO DO%%%%%%%%%

%1. Calibrate Parameters
%%%%Do Last

%%%Parameters
R = 2; %Resistance CmH2Os/Liter
C_al = 0.033; %Alveolar Compliance V/P
C_Lungs = 40 %%%%%%PATIENT SPECIFIC%%%%%%%%
Va(1) = 3; %Initiel volumen 3L
Pa(1) = 5; %Initielt alveolært tryk 5CmH2O (PEEP)
Pinsp = 20; %Leveret Tryk



%2. Input Settings
%%%%Do Last

