function Pmus = Pmus_Driver(t,PSTrigger)
%PMUS_DRIVER Outputs Pmus at current time, given that conditions of
%spontaneous breathing are met, and PS trigger hasn't been reached

global P

PS = P.resp.PS;
PEEP = P.resp.PEEP;
Trise = P.resp.Trise;
Tdeflate = P.resp.Tdeflate;
PmusTi = P.resp.PmusTi;
PmusTe = P.resp.PmusTe;
PmusPause = P.resp.PmusPause;
Tstart = 0;
PmusSet = P.resp.PmusSet; 
%A = Amplitude
%f = Frequency [Hz]
%Period = Length of 1 cycle [s]
%t=time of simulation

%f = 1/period;

%Pit = A*sin(2*pi*f*t)+Offset;

if PSTrigger
    Pmus = 0; %%%KEEP EYE ON FUNNY INTERACTIONS WHEN PSTRIGGER IS HIT    
else
    if t >= Tstart && t <= PmusTi %Monotonically increase during inspiration
        Pmus = PmusSet*sin((pi/(2*PmusTi))*t);
    elseif t > PmusTi && t <= PmusTi+PmusTe  %Monotonically decrease during expiration
        t = t-PmusTi; 
        Pmus = PmusSet*sin((pi*(t+PmusTe-2*PmusTi))/2*(PmusTe-PmusTi));
    elseif t > PmusTe-PmusTi && t <= PmusTe-PmusTi+PmusPause % 0 During pause between insp and exp
        Pmus = 0;
    end
end
end


