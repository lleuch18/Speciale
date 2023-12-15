function [pao_plot,ppl_plot,flow_plot,V_plot] = plots(pao,ppl,flow,v)

pao_plot = false;
ppl_plot = false;
flow_plot = false;
V_plot = false;

if pao == true
pao_plot = true;
end

if ppl == true
ppl_plot = true;
end

if flow == true
flow_plot = true;
end

if v == true;
V_plot = true;
end
end

