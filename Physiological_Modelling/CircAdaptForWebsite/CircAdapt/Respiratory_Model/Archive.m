%% Pmus_Driver when PSTrigger was cycle variable
function Pmus = Pmus_Driver(t,PSTrigger)
%PMUS_DRIVER Outputs Pmus at current time, given that conditions of
%spontaneous breathing are met, and PS trigger hasn't been reached

global P

PS = P.resp.PS;
PEEP = P.resp.PEEP;
Trise = P.resp.Trise;
Tdeflate = P.resp.Tdeflate;
PmusTi = P.resp.PmusTi;
PmusTe = P.resp.PmusExpLgth;
PmusPause = P.resp.PmusPause;
PmusExpLgth = P.resp.PmusExpLgth;
Tstart = 0;
PmusSet = P.resp.PmusSet; 



if isfield(P.resp, 'Pmus_Exp_PSTrigger') == 0
    disp(['value of exist(): ', num2str(isfield(P.resp, 'Pmus_Exp_PSTrigger'))])
    %Creates a pre-calculated version of Pmus at expiration, which is the
    %inverse of inspiratory Pmus, with a frequency defined by PmusTe
    %instead of PmusTi
    P.resp.t_exp = [0:P.resp.dt:PmusTe]';   
    P.resp.Pmus_Exp_PSTrigger = P.resp.PSTrigger*sin((pi/(2*PmusTe))*P.resp.t_exp); P.resp.Pmus_Exp_PSTrigger = P.resp.Pmus_Exp_PSTrigger(end:-1:1);
    
end

if PSTrigger    
    %Subtract TriggerTime, in order to access Pmus_Exp at its origin
    t = t-P.resp.TriggerTime

    disp(['t_exp:',num2str(find(abs(P.resp.t_exp-t)<0.001))])
    if t<=PmusTe
        %Acceses the pre-calculated Pmus at expiration, at index
        %corresponding to current time
    Pmus = P.resp.Pmus_Exp_PSTrigger(find(abs(P.resp.t_exp-t)<0.001))
    else
        Pmus=0;
    end
else
    if t >= Tstart && t <= PmusTi %Monotonically increase during inspiration
        Pmus = PmusSet*sin((pi/(2*PmusTi))*t);
        %disp(['Pmus ', num2str(Pmus), 'At t', num2str(t)])
    elseif t > PmusTi && t <= PmusTi+PmusTe  %Monotonically decrease during expiration
        t = t-PmusTi; 
        Pmus = -PmusSet*sin((pi*(t+PmusTe-2*PmusTi))/(2*(PmusTe-PmusTi)));
    elseif t > PmusTe-PmusTi && t <= PmusTe-PmusTi+PmusPause % 0 During pause between insp and exp
        Pmus = 0;
    end
end
end




%% State_Switch
%state = State_Switch(t);
%Unanswered Questions:
%%How to handle phases of breath cycle?
%We set a Ti and Te
%Ti is run at Δt intervals
%When mod(cnt_ti,Ti) = 0, we switch to Te and reset Ti
%Visa Verse when mod(cnt_te,Te) = 0



%% Earlier Versions of PmusDriver
%{disp(['t in PmusDriver: ',num2str(t)])
    %Pmus =  -P.resp.PSTrigger*sin((pi*(t+PmusTe-2*PmusTi))/(2*(PmusTe-PmusTi))); %%%KEEP EYE ON FUNNY INTERACTIONS WHEN PSTRIGGER IS HIT
    %Pmus = Pmus+(PmusSet*sin((pi/(2*PmusTi))*P.resp.TriggerTime)+P.resp.PSTrigger*sin((pi*((P.resp.TriggerTime+0.02)+PmusTe-2*PmusTi))/(2*(PmusTe-PmusTi))));
    

%% Original Driver Function
%if state == 'insp'
%Pao calc from Trise and Ti
%Pao = Activation_Function(tDummy);



%% Index_Mapping
index = find(P.resp.index_mapping==t); %Find the index which hold the given time_point
disp(['Current time: ', num2str(t)])
disp(['Current Pao: ', num2str(P.resp.Pao(index))])
disp(['Current Index: ', num2str(index)])


%% Flow Conditionals
 %{
    if t(i) == 0
        flow = 0;
    else    
    flow=(Pao-Ppl)/P.resp.R; %1. Calculate flow at each timestep 
    %Normal Resistance 2 to 3 cmH2O/L/sec.
    end

    %if t(i)>P.resp.Ti && t(i)<= P.resp.Ti+P.resp.Te
      %  flow = flow*-1;
    %end
 %}

%% Initial Ppl
%Ppl0 = Ppl0+P.resp.PEEP; %Default -3cmH2O + PEEP
%Ppl = Ppl0; %Set by user