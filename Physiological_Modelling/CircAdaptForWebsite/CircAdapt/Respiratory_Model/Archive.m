%% State_Switch
%state = State_Switch(t);
%Unanswered Questions:
%%How to handle phases of breath cycle?
%We set a Ti and Te
%Ti is run at Δt intervals
%When mod(cnt_ti,Ti) = 0, we switch to Te and reset Ti
%Visa Verse when mod(cnt_te,Te) = 0






%% Original Driver Function
%if state == 'insp'
%Pao calc from Trise and Ti
%Pao = Activation_Function(tDummy);



%% Index_Mapping
index = find(P.resp.index_mapping==t); %Find the index which hold the given time_point
disp(['Current time: ', num2str(t)])
disp(['Current Pao: ', num2str(P.resp.Pao(index))])
disp(['Current Index: ', num2str(index)])
