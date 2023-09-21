function [ volumeChange, ejection, regurgitation ] = CalculateStrokeVolumes
%UNTITLED Summary of this function goes here
%   Detailed explanation goes here

global P;

cavityVolumes = GetFt( 'Cavity', 'V', { 'Lv', 'Rv' } );

volumeChange = max( cavityVolumes ) - min( cavityVolumes );

% Calculate flow volumes

aorticFlow = GetFt( 'Valve', 'q', 'LvSyArt' );
aorticEjectionIdxs = find( aorticFlow > 0 );
aorticForwardFlow = zeros( size( aorticFlow ) );
aorticForwardFlow( aorticEjectionIdxs ) = aorticFlow( aorticEjectionIdxs );

pulmonaryFlow = GetFt( 'Valve', 'q', 'RvPuArt' );
pulmonaryEjectionIdxs = find( pulmonaryFlow > 0 );
pulmonaryForwardFlow = zeros( size( pulmonaryFlow ) );
pulmonaryForwardFlow( pulmonaryEjectionIdxs ) = pulmonaryFlow( pulmonaryEjectionIdxs );

LvEjection = trapz( P.t, aorticForwardFlow );
RvEjection = trapz( P.t, pulmonaryForwardFlow );

ejection = [ LvEjection RvEjection ];

aorticRegurgitationIdxs = find( aorticFlow < 0 );
aorticBackwardFlow = zeros( size( aorticFlow ) );
aorticBackwardFlow( aorticRegurgitationIdxs ) = aorticFlow( aorticRegurgitationIdxs );

pulmonaryRegurgitationIdxs = find( pulmonaryFlow < 0 );
pulmonaryBackwardFlow = zeros( size( pulmonaryFlow ) );
pulmonaryBackwardFlow( pulmonaryRegurgitationIdxs ) = pulmonaryFlow( pulmonaryRegurgitationIdxs );

LvRegurgitation = trapz( P.t, aorticBackwardFlow );
RvRegurgitation = trapz( P.t, pulmonaryBackwardFlow );

regurgitation = [ LvRegurgitation RvRegurgitation ];

end

