function Memory_Allocation
%MEMORY_ALLOCATION Allocates Memory to the state variables of the
%respiratory module

%   State Variables are stored in the global P (parameter) variable
global P

%Nr. of time intervals
nt = P.resp.sim_lgth;

%Construct Matrix
mem_mat = zeros(nt,1); %Zeros matrix of lgth time intervals

%For each state variable, allocate the zeros matrix
P.resp.flow = mem_mat;
P.resp.Palv = mem_mat;
P.resp.Pao = mem_mat;
P.resp.V = mem_mat;
P.resp.Ppl = mem_mat;




end

