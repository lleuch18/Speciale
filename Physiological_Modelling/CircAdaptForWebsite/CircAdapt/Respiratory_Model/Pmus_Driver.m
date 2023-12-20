function Pmus = Pmus_Driver(t,Pmus_Cycle)
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

%disp(num2str(t));

if isfield(P.resp, 'Pmus_Exp_PSTrigger') == 0 && Pmus_Cycle == true
    disp(['value of exist(): ', num2str(isfield(P.resp, 'Pmus_Exp_PSTrigger'))])
    %Creates a pre-calculated version of Pmus at expiration, which is the
    %inverse of inspiratory Pmus, with a frequency defined by PmusTe
    %instead of PmusTi
    P.resp.t_exp = [0:P.resp.dt:PmusTe]';   
    P.resp.Pmus_Exp_PSTrigger = P.resp.Pmus_At_CV*sin((pi/(2*PmusTe))*P.resp.t_exp); P.resp.Pmus_Exp_PSTrigger = P.resp.Pmus_Exp_PSTrigger(end:-1:1);
    
end

if Pmus_Cycle    
    %Subtract TriggerTime, in order to access Pmus_Exp at its origin
    t = t-P.resp.PmusCycleTime;
   
    
    if t<=PmusTe
        if t < 0.006
            t
        end
        %Acceses the pre-calculated Pmus at expiration, at index
        %corresponding to current time
    Pmus = P.resp.Pmus_Exp_PSTrigger(find(abs(P.resp.t_exp-t)<0.001));
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


