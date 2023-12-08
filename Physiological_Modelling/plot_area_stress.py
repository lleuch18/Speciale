"""Plot of Patch properties."""

import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cmx
import numpy as np

# X-axis
V = np.linspace(0e-4, 2.5e-4, 11).reshape((-1, 1))


labels = ['Len', 'AWall', 'A0', 'p0', 'k']

# Plot Passive behavior
fig = plt.figure(1, figsize=(11, 4), clear=True)
for i_plot in range(5):
    ax = fig.add_subplot(1, 5, 1+i_plot)

    # parameters
    Len = 0.4
    AWall = 0.1139e-3
    A0 = 0.4971e-3
    p0 = 1.2166e4
    k = 8


     # (((A  + 0.5 * AWall) / (A0 + 0.5 * AWall))

    A = V / Len
    Anorm = A/AWall
    p_trans = (((Anorm + 0.5) / (A0 / AWall + 0.5)) ** (k / 3.0 - 1)) * p0
    p_trans /= 133

    # plt.plot(V*1e6, p_trans, zorder=99, c='k')

    # color_down = [0.2,0.5,0.9]
    # color_ref = [0.2,0.2,0.2]
    # color_up = [.9,.1,.1]

    color_down, color_ref, color_up = plt.cm.RdBu(np.linspace(0.2, .75, 3))
    color_ref[:3] = 1-color_ref[:3]

    if i_plot==0:
        Len = np.linspace(0.3, 0.5, 5)
        colors=[color_down, color_down, color_ref, color_up, color_up]
    if i_plot==1:
        AWall = AWall * np.exp(np.linspace(-6, 6, 5))
        colors=[color_down, color_down, color_ref, color_up, color_up]
    if i_plot==2:
        A0 = A0 * np.linspace(0.8, 1.2, 5)
        colors=[color_down, color_down, color_ref, color_up, color_up]
    if i_plot==3:
        p0 = p0 * np.linspace(0.8, 1.2, 5)
        colors=[color_down, color_down, color_ref, color_up, color_up]
    if i_plot==4:
        k = k * np.linspace(0.5, 1.5, 5)
        colors=[color_down, color_down, color_ref, color_up, color_up]
    A = V / Len
    Anorm = A/AWall
    p_trans = (((Anorm + 0.5) / (A0 / AWall + 0.5)) ** (k / 3.0 - 1)) * p0
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
