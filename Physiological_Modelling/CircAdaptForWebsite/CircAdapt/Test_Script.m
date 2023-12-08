clc;
clear all;
close all;

global P

%%%Parameters
P.resp.R = 2; %Resistance CmH2Os/Liter
P.resp.Calv = 0.033; %Alveolar Compliance V/P
P.resp.Clungs = 40; %%%%%%PATIENT SPECIFIC%%%%%%%%
P.resp.Pvent = 20; %Leveret Tryk
P.resp.RR = 12; %Respiratory rate in bpm
P.resp.TCT = 60/P.resp.RR; %Total Cycle Time in seconds
P.resp.Ti = 1.5 %Inspiratory time seconds
P.resp.Te = 2.5 %Inspiratory time seconds

%Initial Values
P.resp.V0 = 3; %Initiel volumen 3L
P.resp.Palv0 = 5; %Initielt alveolært tryk 5CmH2O (PEEP)
P.resp.Pao0 = 0; %cmH2O
P.resp.flow0 = 0; %L/min
P.resp.Ppl0 = -3; %cmH2O

%initial value vector
SV0 = [P.resp.V0, P.resp.Palv0, P.resp.Pao0,flow0,Ppl0]