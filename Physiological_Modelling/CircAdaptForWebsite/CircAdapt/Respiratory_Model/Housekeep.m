function Housekeep(t, flow,V,Pao,Ppl)%Palv,
global P
%HOUSEKEEP saves results of state variables at each timestep
%   Appends the values calculated by the ODE solver at each timestep, to a
%   data structure for analysis purposes

P.resp.flow(t,1) = flow;
P.resp.Pao(t,1) = Pao;
P.resp.V(t,1) = V;
P.resp.Ppl(t,1) = Ppl; 


end

