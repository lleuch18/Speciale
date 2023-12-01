"""Plot of Patch properties."""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np

# X-axis
V = np.linspace(0e-4, 2.5e-4, 101).reshape((-1, 1))


labels = ['p_ref', 'V_ref', 'k']

# Plot Passive behavior
fig = plt.figure(1, figsize=(8, 4), clear=True)
for i_plot in range(3):
    ax = fig.add_subplot(1, 3, 1+i_plot)

    # parameters
    k = 10
    V_ref = 1e-4
    p_ref = 133

    p_trans = p_ref * (V/V_ref)**k
    p_trans /= 133

    # plt.plot(V*1e6, p_trans, zorder=99, c='k')

    # color_down = [0.2,0.5,0.9]
    # color_ref = [0.2,0.2,0.2]
    # color_up = [.9,.1,.1]

    color_down, color_ref, color_up = plt.cm.RdBu(np.linspace(0.2, .75, 3))
    color_ref[:3] = 1-color_ref[:3]

    if i_plot==0:
        p_ref = 133 * np.array([0.2, 0.5, 1, 2, 5])
        colors=[color_down, color_down, color_ref, color_up, color_up]
    if i_plot==1:
        V_ref = np.linspace(0.5e-4, 1.5e-4, 5)
        colors=[color_down, color_down, color_ref, color_up, color_up]
    if i_plot==2:
        k = np.linspace(5, 15, 5)
        colors=[color_down, color_down, color_ref, color_up, color_up]
    p_trans = p_ref * (V/V_ref)**k
    p_trans /= 133
    [plt.plot(V*1e6, p_trans[:, i], c=c) for i, c in enumerate(colors)]



    plt.title(labels[i_plot])
    plt.xlabel(r'Volume [mL]')
    plt.ylabel(r'$p_{trans}$ [mmHg]')

    plt.axhline(0, c=[0.5, 0.5, 0.5], ls='-', lw=1)

    # plt.legend()
    ax.spines[['right', 'top']].set_visible(False)

    ax.set_ylim([0, 150])

    # Tension
    # ax = fig.add_subplot(2, 5, 6+i_plot)

    # ax.spines[['right', 'top']].set_visible(False)


plt.suptitle('Cavity volume - transmural pressure relationship',
             fontsize=15, fontweight='bold')
plt.tight_layout()
plt.show()
