function Housekeep(t, flow,V,Pvent,Pmus,Ppl,Pao)%Palv,
global P
%HOUSEKEEP saves results of state variables at each timestep
%   Appends the values calculated by the ODE solver at each timestep, to a
%   data structure for analysis purposes

P.resp.flow(t,1) = flow;
P.resp.V(t,1) = V;
P.resp.Pvent(t,1) = Pvent;
P.resp.Pmus(t,1) = Pmus;
P.resp.Ppl(t,1) = Ppl;
P.resp.Pao(t,1) = Pao;

end

