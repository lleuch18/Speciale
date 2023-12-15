function Respiratory_Modelfn(Ppl0,start_time,end_time)
%Computes the system of equations governing the equation of motion as a
%continious time derivative, controlled by driver function Pao
%   Detailed explanation goes here

global P
%% Plots
[Pao_plot,Ppl_plot,flow_plot,V_plot] = plots(1,1,1,1);

%% Loop Parameters
t = [start_time:P.resp.dt:end_time]; 


%% Initial Values
Pmus = 0+P.resp.PEEP; %Techically Ppl = -3 at start insp, but we assume the driving pressure creating flow, to be equal to PEEP 
Pao = P.resp.PEEP; %Initial Pao is PEEP [cmH2O]
V = (P.resp.Crs*P.resp.PEEP)*10^-3; %Initiel Volumen [L]
flow = 0;

%% System of Equations
for i = 1:length(t)     
    %% Pmus Activation 
    % If Pmus reaches PSTrigger threshold, the Pvent is delivered
    if Pmus == P.resp.PSTrigger
        PSTrigger = true;
    else
        PSTrigger = false;
    end
    
    % Pmus adds dP caused by patient breathing effort
    Pmus = Pmus_Driver(t(i),PSTrigger);

    Pmus = Pmus+dPpl; % Calculate Ppl
    %% Pvent Activation

    Pvent = Pvent_Driver(t(i)); %Pressure delivered by vent at t [cmH2O]

    %Flow is driven by the dP of Pvent-Pmus
    flow=((Pvent-Pmus)/8); %[L/s] -> [L/min] at plot    
    
    % The flow created by the dP, adds an amount of dV
    dV = (flow*P.resp.dt); 
    V = V + dV; %
    
    % dV then creates a dPao, through either in- or deflation
    dPao = dV/(P.resp.Crs*10^-3); %Change in pressure ((L/dt)*dt)/(L/P) =(P/dt)*dt = P
    Pao = Pao+dPao;
    
    
    
    %% Housekeeping
    Housekeep(i,flow,V,Pvent,Pmus);    

end

disp('Simulation Done')

if Pao_plot
figure(1)
plot(t,P.resp.Pao)
title('Pao')
ylabel('Pao (cmH2O)')
xlabel('Time (S)')
end

if Ppl_plot
figure(2)
plot(t,P.resp.Ppl)
title('Ppl')
ylabel('Ppl (cmH2O)')
xlabel('Time (S)')
end

if flow_plot
figure(3)
plot(t,P.resp.flow*60);
title('flow')
ylabel('flow (L/min)')
xlabel('Time (S)')
end

if V_plot
figure(4)
plot(t,P.resp.V)
title('V')
ylabel('V (L)')
xlabel('Time (S)')
yticks([0,0.5,1,1.5,2,2.5,3,3.5,4])
%yline((P.resp.CL*P.resp.PEEP)*10^-3)
end



end

