# -*- coding: utf-8 -*-
"""
Created on Mon Oct 30 06:02:09 2023

@author: Lasse
"""

"""
Tutorial CircAdapt VanOsta2022.

November 2022, by Nick van Osta

The goal of this tutorial is to understand the CircAdapt framework and to use
the VanOsta2022 model. This tutorial assumes little to no knowledge about
python. Therefore, basic python conventions and syntax will be discussed.
This tutorial assumes the installation is followed as described on the wiki
(https://wiki.circadapt.org/index.php?title=Circadapt_in_Python). This uses
Python >3.9 installed with anaconda and editted in Spyder. Other ways are
possible, but might not be in line with this tutorial.

Content
-------
    1. Basics of python
    2. Load the model
    3. Plot global hemodynamics
    4. Change parameters
    5. Multipatch and local dynamics
    6. Save and Load
"""

# Uncomment next lines if not installed
# import sys
# sys.path.append('../../../src/')

import circadapt

# Uncomment next lines if not installed
# circadapt.DEFAULT_PATH_TO_CIRCADAPT = "../../../CircAdapt_Library/out/build/x64-Release/CircAdaptLib.dll"

# %% 1. Basics of python
print('1. Basics of python')

# Always start the document with importing modules.
# Numpy is used for mathematics, Matplotlib for plots. These are conventionally
# imported as np and plt.
import numpy as np
import matplotlib.pyplot as plt

# Only import the class we need in this tutorial.
from circadapt.model import VanOsta2023
# CA = VanOsta2022()

# alternatively, you can import the whole package, but it changes the way you
# make the object.
# import circadapt
# CA = circadapt.VanOsta2022()

# Parameters types are automaticaly set or changed by the interpreter, but it
# is good to create an integer when you need an integer and float when needed.
i = 1                 # integer
f = 1.                # float
b = True              # bool
l = [1, 2, 3]         # list
d = {'a': 1, 'b': 2}  # dictionary

# get data from the list and dictionary
first_item_of_list = l[0]
item_from_dictionary = d['a']

# the use of numpy is advised for more complex use and for calculation
numpy_array = np.array(l)
print('Find if array is 2: ', (numpy_array == 2))
print('Multiply array with 2: ', (numpy_array * 2))

# In spyder, you can place bullits. While debugging, ipython will stop at these
# bullits. You can also press f9 to run a single line or selection and press
# crtl+<enter> to run a block seperated by # %%

# %% 2. load model
print('\n 2. Load model. ')
# Load predefined model with predefined parameterization
# More information on this model can be found here:
# https://wiki.circadapt.org/index.php?title=VanOsta2022
CA = VanOsta2023()

# CircAdapt tries to follow the syntax of python and numpy as much as possible.
# The object can be handled as a dictionary. Content can be printed in the
# console, and printed on request in the ipython console.
print('The result of printing the object gives information about the '
      'components: ')
print(CA)

# components can also be retrieved as a list of strings
components = CA.components
print('Components of this model: ', components, '\n')

# Similar to the object itself, components can be printed
print('Patches in this model: ')
print(CA['Patch2022'])

# Each component points to multiple c++ objects of that component type. The
# objects can also be obtained using
objects = CA['Patch2022'].objects
parameters = CA['Patch2022'].parameters
signals = CA['Patch2022'].signals

objects = CA['ArtVen'].objects
parameters = CA['ArtVen'].parameters
signals = CA['ArtVen'].signals

print(objects)
print(parameters)
print(signals)

objects = CA['ArtVen']
parameters = CA['ArtVen'].parameters
signals = CA['ArtVen'].signals

print(objects)
print(parameters)
print(signals)

# Signals are not stored, so they are only available after running a beat.
# Therefore the model should run. You can either run a number of beats, or run
# until the model is hemodynamically stable.
#CA.run(5)
CA.run(stable=True)

# %% 3. Plot global hemodynamics
# Here is an example code to plot the PV loop
# First we open a figure. Assigning this figure to a variable is optional, but
# is useful for design purposes.
fig = plt.figure(1)

# get volume and pressure of LV
Vlv = CA['Cavity']['V'][:, 6]*1e6
plv = CA['Cavity']['p'][:, 6]*7.5e-3

# get volume and pressure of RV
Vrv = CA['Cavity']['V'][:, 7]*1e6
prv = CA['Cavity']['p'][:, 7]*7.5e-3

# You can also use location names to get/set signals and parameters
# For this, use only the last part of the full object name, e.g. cLv for
# Model.Peri.TriSeg.cLv. You can get one signal or multiple signals
Vlv = CA['Cavity']['V'][:, 'cLv']*1e6
Vrv = CA['Cavity']['V'][:, 'cRv']*1e6
pressure = CA['Cavity']['p'][:, ['cLv', 'cRv']]*7.5e-3

# you can split the two pressure signals into two parameters using the
# following line. First transpose the pressure such that the first axis sets
# the signals
plv, prv = pressure.T

# Now we plot the two lines.
line1 = plt.plot(Vlv, plv, c='k', label='Lv')
line2 = plt.plot(Vrv, prv, c='r', label='Rv')
plt.ylabel('Pressure [mmHg]')
plt.xlabel('Volume [mL]')
plt.legend()

# %% 4. Change parameters
# Now reduce the contractility of all 3 ventricular walls, run the simulation,
# and plot the data
#CA['Patch2022']['Sf_act'][2:] = 60e3
#CA.run(stable=True)
#plt.plot(CA['Cavity']['V'][:, 'cLv']*1e6, CA['Cavity']['p'][:, 'cLv']*7.5e-3, 'k--', label='Lv Reduced Sf_act')
#plt.plot(CA['Cavity']['V'][:, 'cRv']*1e6, CA['Cavity']['p'][:, 'cRv']*7.5e-3, 'r--', label='Rv Reduced Sf_act')
plt.legend()


# %%  Presure/Time
t = CA.get('Solver.t') * 1e3
m=1
n=3
ax = plt.subplot(m,n,1)
#ax.plot(t, CA.get('Model.C.p')/133, label='Chamber', color='k')
ax.plot(t, CA.get('Model.SyArt.p')/133, label='SyArt', color='r')
ax.plot(t, CA.get('Model.SyVen.p')/133, label='SyVen', color='b')
plt.legend()
ax.set_ylabel('Pressure [mmHg]')
ax.set_xlabel('Time [ms]')

# =============================================================================
# ax = plt.subplot(m,n,2)
# #ax.plot(t, CA.get('Model.C.V')*1e6, label='Chamber', color='k')
# ax.set_ylabel('Volume [mL]')
# ax.set_xlabel('Time [ms]')
# plt.legend()
# =============================================================================

# =============================================================================
# ax = plt.subplot(m,n,3)
# ax.plot(t, CA.get('Model.CiSy.q')*1e3, label='ArtVen')
# ax.plot(t, CA.get('Model.ChaSyArt.q')*1e3, label='ChaSyArt')
# ax.plot(t, CA.get('Model.SyVenCha.q')*1e3, label='SyVenCha')
# plt.legend()
# =============================================================================

ax.axhline(0, color='k', linestyle='--')
ax.set_ylabel('Flow [mL/ms]')
ax.set_xlabel('Time [ms]')
plt.legend()

plt.suptitle('Simple one-ventricle model setup', fontsize=16, weight='bold')