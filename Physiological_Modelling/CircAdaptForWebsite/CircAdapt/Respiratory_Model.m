global P


state = State_Switch(t);

%Unanswered Questions:
%%How to handle phases of breath cycle?
%We set a Ti and Te
%Ti is run at Δt intervals
%When mod(cnt_ti,Ti) = 0, we switch to Te and reset Ti
%Visa Verse when mod(cnt_te,Te) = 0

if state == 'insp'
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
Housekeep(t,flow,V,Palv,Pao,Ppl);
elseif state == 'exp'
    
end


%%%%%%%%%%%%%%TO DO%%%%%%%%%

%1. Calibrate Parameters
%%%%Do Last



%2. Input Settings
%%%%Do Last















