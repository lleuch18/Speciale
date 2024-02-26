close all; clear all;
% CircAdaptMain
% Theo Arts, Tammo Delhaas, Joost Lumens
% Version CircAdapt.I5 May, 2008
% email: t.arts@bf.unimaas.nl
%
% CircAdapt is a lumped model of the dynamic circulation. Size of heart
% and bloodvessels adapt to load, as generated by the model itself.
% All variables and parameter are stored in the structure P with file
% name 'P'. Hemodynamic data are displayed graphically
% Map of structure 'P' obtained by execution of 'mapstructure(P)'
% Used functions: PNew, CircAdapt, CircAdaptDisplay

clear
global P;

Num_Beats = 1;

Original = 1;

addpath(pwd);% add current directory to path




if exist('P.mat','file'); % if P.mat file is available
    FileName='P';
    PathName=[pwd,'\'];
    ShowMenu=1;
    while ShowMenu;
        c2=input('[N]ew, [R]eference, [L]oad, [C]ontinue <Enter>: ','s');
        a=[c2,'c']; c=a(1); % convert <Enter> to 'c'
        switch lower(c)
            case('l'); % load file with P-structure
                [FileName,PathName] = uigetfile('*.mat','Choose file: ');
                load([PathName,FileName]);
                c='c';ShowMenu=false;
            case('r') % load reference file with P-structure
                load('PRef');
                c='c';ShowMenu=false;
            case('n'); % new P-structure from scratch
                PNew;
                c='c';ShowMenu=false;
            case('c'); % continuation of simulation
                load([PathName,FileName]);
                c='c';ShowMenu=false;
            otherwise
                ShowMenu=true;
        end
    end
else
    if exist('PRef.mat','file');
        c2=input('[N]ew, [R]eference, [L]oad,: ','s');
        a=[c2,'c']; c=a(1); % convert <Enter> to 'c'
        switch lower(c)
            case('l'); % load file with P-structure
                [FileName,PathName] = uigetfile('*.mat','Choose file: ');
                load([PathName,FileName]);
                c='c';ShowMenu=false;
            case('r')
                load('PRef');
                c='c';
            otherwise
                PNew;
                c='c';
        end
    else
        PNew; % Parameter initialization, some remodeling rules inclusive
        % Generates parameter structure Par and initial conditions of the variables P
        c='c';
    end
end


% Default initialization
G=P.General;
G.DtSimulation=Num_Beats*G.tCycle; % standard duration of simulation

P.Adapt.FunctionName='Adapt0P'; % No adaptation
P.Adapt.Fast= 0; % regular beat to beat sequence

%XXXX Menu for changing hemodynamic variables and adaptation condition
OK=1; NY='NY';
while OK;
    disp(' ');
    disp(['[PA]tient                  number: (2-14)']);
    disp(['[P]ressure                  (kPa): ',num2str(G.p0/1e3)]);
    disp(['[F]low                     (ml/s): ',num2str(G.q0*1e6)]);
    disp(['[T]ime of beat               (ms): ',num2str(G.tCycle*1e3)]);
    disp(['[D]uration simulation         (s): ',num2str(G.DtSimulation)]);
    disp(['Adapt n[O]ne [R]est,[E]xercise   : ',P.Adapt.FunctionName]);
    disp(['Faster steady state [Y]/[N]      : ',NY(P.Adapt.Fast+1)]);
    disp( '<Enter> = Continue');
    c1=input('Choose Letter <Enter>: ','s');
    switch lower(c1);
        case 'pa'
            patient=num2str(input('Patient Number: '));
            pt = load(['..\Data\to Lasse 2023\DataP',patient,'PS.mat']);
            P.Patient=pt;
            P.Patient.Name = {'time','ecg1 (mV)','ecg2(mV)','Airway Pressure (cmH2O)','flow (ml/sec)', 'FeCO2 (%)','FeO2 (%)', 'Arterial Pressure (mmHg)'}
        case 'p'
            G.p0=input('Mean Arterial Pressure (kPa): ')*1e3;
        case 'f'
            G.q0=input('Systemic Flow (ml/s): ')/1e6;
        case 't'
            G.tCycle=input('Cycle Time (ms): ')*1e-3;
        case 'd'
            G.DtSimulation=input('Duration of simulation (s): ');
        case 'o'
            P.Adapt.FunctionName='Adapt0P';
            G.DtSimulation=1.5*G.tCycle;
        case 'r'
            P.Adapt.FunctionName='AdaptRestP';
            G.DtSimulation=50*G.tCycle;
        case 'e'
            P.Adapt.FunctionName='AdaptExcP';
            G.DtSimulation=100*G.tCycle;
        case 'y'
            P.Adapt.Fast=1;
            G.DtSimulation=max(30*G.tCycle,G.DtSimulation);
        case 'n'
            P.Adapt.Fast=0;
        otherwise
            OK=0;
    end
end

% === Solves SVar for problem defined in parameter structure 'P'
G.tEnd=P.t(end)+G.DtSimulation;
P.General=G;

if Original
    CircAdaptP; %generate solution
else
    Copy_of_CircAdaptP
end

%=== Saving State Variables and Model Parameters
save P P; %save compact solution as structure P in file 'P'
disp('Differential equation has been solved');

CircDisplayP; % graphical display
% Structure P has been extended with solution for all variables as a
% function of time
%{
disp('Average Pressures')
disp(['SyArt: ',num2str(mean(P.Node.p(:,1)))]);
disp(['SyVen: ',num2str(mean(P.Node.p(:,2)))]);
disp(['PuArt: ',num2str(mean(P.Node.p(:,3)))]);
disp(['PuVen: ',num2str(mean(P.Node.p(:,4)))]);
disp(['La: ',num2str(mean(P.Node.p(:,5)))]);
disp(['Ra: ',num2str(mean(P.Node.p(:,6)))]);
disp(['Lv: ',num2str(mean(P.Node.p(:,7)))]);
disp(['Rv: ',num2str(mean(P.Node.p(:,8)))]);
%}


