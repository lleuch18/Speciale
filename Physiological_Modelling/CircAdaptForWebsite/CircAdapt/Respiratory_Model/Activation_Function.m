function Pao = Activation_Function(t)
global P
%ACTIVATION_FUNCTION Function which simulates the delivered pressure from
%the ventilator
%   Ti: Inspiratory time
%   Trise: Rise time, 20% of Ti
%   Te: Expiratory time

if t >= 0 && t <= 0.01
    Pao = 0 + P.resp.PEEP;
elseif t > 0.01 && t <= P.resp.Trise
    Pao = P.resp.PS*(t/P.resp.Trise)+P.resp.PEEP;
elseif t > P.resp.Trise && t <= P.resp.Ti
    Pao = P.resp.PS+P.resp.PEEP;
elseif t > P.resp.Ti && t <= P.resp.Te + P.resp.Ti;
    Pao = P.resp.PEEP;
end

end
