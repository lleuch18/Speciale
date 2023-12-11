%% Parameters
clear all;
close all;

global P

P.resp.R = 2; %Resistance CmH2Os/Liter
P.resp.Calv = 0.033; %Alveolar Compliance V/P
P.resp.Clungs = 40; %%%%%%PATIENT SPECIFIC%%%%%%%%
P.resp.PS = 20; %Leveret Tryk
P.resp.PEEP = 5;
P.resp.RR = 12; %Respiratory rate in bpm
P.resp.TCT = 60/P.resp.RR; %Total Cycle Time in seconds
P.resp.Ti = 1.5 %Inspiratory time seconds
P.resp.Te = 2.5 %Inspiratory time seconds
P.resp.Trise = P.resp.Ti*0.2; % 20percent of Ti
P.resp.dt = 0.002; %2ms time steps
P.resp.sim_lgth = 4; %Simulation length in seconds


%Initial Values
P.resp.V0 = 3; %Initiel volumen 3L
P.resp.Palv0 = 5; %Initielt alveolært tryk 5CmH2O (PEEP)
P.resp.Pao0 = 0; %cmH2O
P.resp.flow0 = 0; %L/min
P.resp.Ppl0 = -3; %cmH2O
P.resp.PaoPrev = 0; %cmH2O Used for calculating dPao

%initial value vector
P.resp.SV0 = [P.resp.V0,P.resp.flow0,P.resp.Ppl0];%P.resp.Palv0, P.resp.Pao0,

%% One-Breath-Cycle
clc;

%Allocate Memory
Memory_Allocation;

%Set simulation duration
time_points = 0:P.resp.dt:P.resp.sim_lgth; %maybe from 0.02 since t0 may be initial value
sim_duration; %Pre calculates the driver function
P.resp.index_mapping = time_points' %Maps timesteps to indexes, in order to access correct indexes in driver function

%Set Options
tol=1e-4; %tol= 1e-4 or 1e-5: trade off accuracy and calculation speed
opt = odeset('RelTol',tol,'AbsTol',tol);


diary Outputs
[tDummy,SVar] = ode113(@Respiratory_Modelfn,...
        time_points,P.resp.SV0,opt);
diary off

P.resp.V = SVar(:,1);
P.resp.flow = SVar(:,2);
P.resp.Ppl = SVar(:,3);

%% Plotting Results
%subplot(4,1,1);
plot(P.resp.Pao)
title('Pao/dT (cmH2O/s)')



%% Activation_Function Testing
%{
%t = [0:0.002:0.01]; %Condition 1
%t = [0.01:0.002:P.resp.Trise]; %Condition 2
%t = [P.resp.Trise:0.002:P.resp.Ti]; %Condition 3
%t = [P.resp.Ti:0.002:P.resp.Te+P.resp.Ti]; %Condition 4
t = [0:0.002:P.resp.Te+P.resp.Ti]; %Full Duration

cnt = 1;

P.resp.Pao = zeros(length(t),1);

for i = 1:length(t);
    %disp(['i is: ',num2str(i)]);
    %disp(['t is: ',num2str(t(i))]);
    P.resp.Pao(cnt) = Activation_Function(t(i));
    cnt = cnt + 1;

end

plot(t,P.resp.Pao);
%}
