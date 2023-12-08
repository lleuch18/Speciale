function Housekeep(t, flow,V,Palv,Pao,Ppl)
global P
%HOUSEKEEP saves results of state variables at each timestep
%   Appends the values calculated by the ODE solver at each timestep, to a
%   data structure for analysis purposes

P.resp.flow(1,t) = flow;
P.resp.Palv(1,t) = V;
P.resp.Pao(1,t) = Palv;
P.resp.V(1,t) = Pao;
P.resp.Ppl(1,t) = Ppl; 

end

