# -*- coding: utf-8 -*-
import sys

# check if should include path for development modus
# try:
#     __import__('circadapt')
# except:
#     sys.path.append('../../../src/')

# actual import
from circadapt import CircAdapt
import numpy as np
import matplotlib.pyplot as plt
from circadapt import components
from circadapt.components import solver


import time

def create_model():
    ###
    n_beat = 10

    dt = 0.001
    solver = "forward_euler"

    # open model
    model = CircAdapt(solver)

    model.set('Solver.dt', dt)
    model.set('Solver.dt_export', dt)

    # Build the cavity C using a Chamber2022 object. This object automatically
    # gets an Wall2022 object with no patches, so a patch must be added.
    model.add_component('Chamber2022', 'C')
    model.add_component('Patch2022', 'P', 'C.wC')

    # Use 'smart component' function to add an ArtVen combination.
    model.add_smart_component('ArtVen')

    # Add and connect valves for inflow and outflow of the cavity
    model.add_component('Valve2022', 'ChaSyArt')
    model.add_component('Valve2022', 'SyVenCha')

    model.set_component('ChaSyArt.Prox', 'C')
    model.set_component('ChaSyArt.Dist', 'SyArt')
    model.set_component('SyVenCha.Prox', 'SyVen')
    model.set_component('SyVenCha.Dist', 'C')

    # set state variables
    model.set('Model.C.V', 125e-6)
    model.set('Model.SyArt.V',   200e-6)
    model.set('Model.SyVen.V',   300e-6)

    # parameterize patch
    model['Patch2022']['dt'] = 0.1
    model['Patch2022']['Sf_act'] = 200e3
    model['Patch2022']['Sf_pas'] = 5e3
    model['Patch2022']['Am_ref'] = 0.014
    model['Patch2022']['k1'] = 10
    model['Patch2022']['v_max'] = 7
    model['Patch2022']['V_wall'] = 1e-04
    # model['Patch2022']['l_si'] = par_Lsi
    model['Patch2022']['tr'] = 0.25
    model['Patch2022']['td'] = 0.25
    model['Patch2022']['time_act'] =  0.5
    model.set('Model.C.wC.P.l_si', 2.0)


    model['ArtVen']['p0'][0] = 9000

    # Run beats
    t0 = time.time()
    model.run(n_beat)
    print(time.time()-t0)

    return model

# %% Run model and plot
if __name__ == '__main__':
    model = create_model()
    plt.figure(1, clear=True, figsize=(9, 3))

    t = model.get('Solver.t') * 1e3

    m=1
    n=3

    ax = plt.subplot(m,n,1)
    ax.plot(t, model.get('Model.C.p')/133, label='Chamber', color='k')
    ax.plot(t, model.get('Model.SyArt.p')/133, label='SyArt', color='r')
    ax.plot(t, model.get('Model.SyVen.p')/133, label='SyVen', color='b')
    plt.legend()
    ax.set_ylabel('Pressure [mmHg]')
    ax.set_xlabel('Time [ms]')

    ax = plt.subplot(m,n,2)
    ax.plot(t, model.get('Model.C.V')*1e6, label='Chamber', color='k')
    ax.set_ylabel('Volume [mL]')
    ax.set_xlabel('Time [ms]')
    plt.legend()

    ax = plt.subplot(m,n,3)
    ax.plot(t, model.get('Model.CiSy.q')*1e3, label='ArtVen')
    ax.plot(t, model.get('Model.ChaSyArt.q')*1e3, label='ChaSyArt')
    ax.plot(t, model.get('Model.SyVenCha.q')*1e3, label='SyVenCha')
    plt.legend()

    ax.axhline(0, color='k', linestyle='--')
    ax.set_ylabel('Flow [mL/ms]')
    ax.set_xlabel('Time [ms]')
    plt.legend()

    plt.suptitle('Simple one-ventricle model setup', fontsize=16, weight='bold')


    # ax = plt.subplot(m,n,4)
    # ax.axhline(0, color='k', linestyle='--', lw=1)
    # ax.set_ylabel('C')
    # plt.legend()

    plt.tight_layout()
    plt.draw()
    plt.show()
