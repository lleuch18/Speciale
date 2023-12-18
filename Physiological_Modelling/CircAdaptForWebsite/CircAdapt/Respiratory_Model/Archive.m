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