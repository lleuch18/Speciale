function SteadyRunner

global P;

stationary = 1;
counter  = 0;
while stationary > 0
    P.General.tEnd = P.t( end ) + 2 * P.General.DtSimulation;
    save P P;
    CircAdaptP;
    ErrVec = 1000 * log( P.Adapt.Out( end, : ) ./ P.Adapt.In( end, : ) );
    stationary = round( sqrt( mean( ErrVec .^ 2 ) ) )
    counter = counter + 1;
    if counter >= 200
        disp( 'Over 200 beats and not stable!' )
        break
    end
end

end

