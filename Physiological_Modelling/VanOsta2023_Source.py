# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 10:36:55 2023

@author: Lasse
"""

class VanOsta2023(Model, ModelAdapt):
    def __init__(self,
                 solver: str = None,
                 path_to_circadapt: str = None,
                 model_state: dict = None,
                 ):
        if solver is None:
            solver = 'backward_differential'

        self._local_save_reference = True

        ModelAdapt.__init__(self)
        Model.__init__(self,
                       solver,
                       path_to_circadapt=path_to_circadapt,
                       model_state=model_state,
                       )

    def build(self):
        self.add_smart_component('ArtVen', build='SystemicCirculation')
        self.add_smart_component('ArtVen', build='PulmonaryCirculation')
        self.add_smart_component('Heart', patch_type='Patch2022')
        self.add_smart_component('Timings')
        self.add_smart_component('PressureFlowControl')

        self.set_component("Peri.RaRv.wPapMus", "Peri.TriSeg.wRv")
        self.set_component("Peri.LaLv.wPapMus", "Peri.TriSeg.wLv")

    def set_reference(self):
        self['Chamber2022']['buckling'] = False
        self['Valve2022']['soft_closure'] = True
        self['Valve2022']['papillary_muscles'] = True

        self['Solver']['dt'] = 0.001
        self['Solver']['dt_export'] = 0.002
        self.set('Solver.order',  2)

        self.set('Model.t_cycle', 0.85)

        self.set('Model.PFC.fac',  0.5)
        self.set('Model.PFC.epsilon', 0.1)
        self.set('Model.PFC.fac_pfc', 1)
        self.set('Model.PFC.stable_threshold', 0.001)


        self['Tube0D']['A0'] = [0.0004982 , 0.00049959, 0.00045184, 0.00051768]
        self['Tube0D']['A_wall'] = [1.13597208e-04, 3.79106863e-05, 8.91394588e-05, 4.26698697e-05]
        self['Tube0D']['k'] = [1.66666667, 2.33333333, 1.        , 2.33333333]
        self['Tube0D']['l'] = [0.4, 0.4, 0.1, 0.1]
        self['Tube0D']['p0'] = [12154.79898845,   213.26733196,  1913.05480512,   600.72294959]

        self['ArtVen']['p0'] = [6345.26731406,  950.        ]
        self['ArtVen']['q0'] = [4.5e-05, 4.5e-05]
        self['ArtVen']['k'] = [1.  , 1.72]


        if True:
            self.set('Model.SyArt.V', 2e-4)
            self.set('Model.PuArt.V', 1e-4)
            self.set('Model.SyVen.V', 4e-4)
            self.set('Model.PuVen.V', 2e-4)

            self.set('Model.Peri.TriSeg.V', 56e-6)
            self.set('Model.Peri.TriSeg.Y', 36e-3)

            self.set('Model.Peri.TriSeg.cLv.V',  150e-6)
            self.set('Model.Peri.TriSeg.cRv.V',  110e-6)
            self.set('Model.Peri.La.V',  25e-6)
            self.set('Model.Peri.Ra.V',  150e-6)


        self['Patch2022']['l_se'] = 0.04
        self['Patch2022']['l_s_ref'] = 2.0
        self['Patch2022']['l_s0'] = 1.8
        self['Patch2022']['dl_s_pas'] = 0.6
        self['Patch2022']['k1'] = 10
        self['Patch2022']['dt'] = 0
        self['Patch2022']['C_rest'] = 0
        self['Patch2022']['l_si0'] = 1.51
        self['Patch2022']['LDAD'] = [1.057, 1.057, 0.64 , 0.64 , 0.64 ]
        self['Patch2022']['ADO'] = [0.65, 0.65, 0.75, 0.75, 0.75]
        self['Patch2022']['LDCC'] = [4. , 4. , 3.2, 3.2, 3.2]
        self['Patch2022']['v_max'] = 7.
        self['Patch2022']['v_max'][:2] = 14.

        self['Patch2022']['tr'] = [0.4 , 0.4 , 0.24, 0.24, 0.24]
        self['Patch2022']['td'] = [0.4 , 0.4 , 0.23, 0.23, 0.23]


        self['Patch2022']['Sf_act'] = [80e3, 80e3, 120e3, 120e3, 120e3]
        self['Patch2022']['Am_ref'] = [0.00458522, 0.00381765, 0.00806997, 0.00454307, 0.01176514]
        self['Patch2022']['V_wall'] = [2.75050615e-05, 1.25959326e-05, 8.80910385e-05, 3.46281364e-05,
               5.16086110e-05]
        self['Patch2022']['Sf_pas'] = [ 16.51117993,  17.0639141 , 580.39235927, 569.67392472,
               606.50514861]


        self['Valve2022']['adaptation_A_open_fac'] = [1.  , 1.11, 1.  , 1.  , 1.11, 1.  ]
        self['Valve2022']['A_open'] = [0.00050042, 0.00050203, 0.00045228, 0.00051764, 0.00055321,
               0.00049838]
        self['Valve2022']['A_leak'] = [2.64705882e-04, 2.64705882e-10, 2.64705882e-10, 2.64705882e-04,
               2.64705882e-10, 2.64705882e-10]
        self['Valve2022']['l'] = 0.01626978
        self['Valve2022']['rho_b'] = 1050
        self['Valve2022']['papillary_muscles'] = True
        self['Valve2022']['papillary_muscles_slope'] = 100
        self['Valve2022']['papillary_muscles_min'] = 0.1
        self['Valve2022']['papillary_muscles_A_open_fac'] = 0.1
        self['Valve2022']['soft_closure'] = True

        self['Bag']['k'] = 10
        self['Bag']['V_ref'] = [0.00051968]
        self['Bag']['p_ref'] = 100

        self.set('Model.Peri.TriSeg.Y', 0.035)

        self['Timings']['law_tauAv'] = 2
        self['Timings']['c_tauAv0'] = 0.172
        self['Timings']['c_tauAv1'] = -0.485*60e-3


        self['Patch2022']['adapt_gamma'] = 0.5
        self.set('Solver.store_beats', 1)

        self['PressureFlowControl']['stable_threshold'] = 1e-3

        self['Patch2022']['SfPasMaxT'] = [6400., 6400.,  6600.,  6600.,  6600.]
        self['Patch2022']['FacSfActT'] = [0.44, 0.44, 0.61, 0.61, 0.61]
        self['Patch2022']['SfPasActT'] = [4800., 4800., 6600., 6600., 6600.]
        self['Patch2022']['LsPasActT'] = [3.  , 3.  , 2.23, 2.23, 2.23]

        self.run(stable=True)

        return


        options = self.get_adapt_options()
        self['General']['q0'] = options['exercise']['q0']
        self['General']['t_cycle'] = options['exercise']['t_cycle']
        self.run(stable=True)

        reference_y = np.array([
            self['Patch2022']['SfEcmMax'],
            self['Patch2022']['SfActMax'],
            self['Patch2022']['SfPasAct'],
            self['Patch2022']['LsPasAct'],
            ]).T

        targets = np.array([
            np.mean(reference_y[:2, :], axis=0),
            np.mean(reference_y[2:, :], axis=0),
            ])
        targets[:, 1] /= self['Patch2022']['Sf_act'][:][[0, 2]]

        # targets = np.array(
        #     [[5.5e+05, 1.9e-01, 3.5e+03, 2.2e+00],
        #      [6.0e+03, 4.9e-01, 4.0e+03, 2.3e+00],
        #      ])

        self['Patch2022']['SfPasMaxT'] = targets[[0, 0, 1, 1, 1], 0]
        self['Patch2022']['FacSfActT'] = targets[[0, 0, 1, 1, 1], 1]
        self['Patch2022']['SfPasActT'] = targets[[0, 0, 1, 1, 1], 2]
        self['Patch2022']['LsPasActT'] = targets[[0, 0, 1, 1, 1], 3]

        self['Patch2022']['adapt_gamma'] = 0.1
        self.adapt(verbose=True)
        self['Patch2022']['adapt_gamma'] = 0.5
        self.adapt(verbose=True)

        # Set adaptation constants
        self.calculate_and_set_matrix(verbose=True)

        # set resting state
        self['General']['q0'] = options['rest']['q0']
        self['General']['t_cycle'] = options['rest']['t_cycle']
        self.run(stable=True)

    def get_unittest_targets(self):
        """Hardcoded results after initializing and running 1 beat."""
        return {
            'LVEDV': 119.7,
            'LVESV':  47.2,
            }

    def get_unittest_results(self, model):
        """Real-time results after initializing and running 1 beat."""
        LVEDV = np.max(model['Cavity']['V'][:, 'cLv'])*1e6
        LVESV = np.min(model['Cavity']['V'][:, 'cLv'])*1e6
        return {
            'LVEDV': LVEDV,
            'LVESV': LVESV,
            }

    def plot(self, fig=None):
        # TODO
        self.plot_extended(fig)

    def plot_extended(self, fig=None):
        if fig is None:
            fig = 1
        if isinstance(fig, int):
            fig = plt.figure(fig, clear=True, figsize=(12, 8))

        # Settings
        grid_size = [32, 32]

        def get_lim(module, signal, locs=slice(None, None, None)):
            signal = self[module][signal][:, locs]
            lim = np.array([np.min(signal), np.max(signal)])
            lim += np.array([-1, 1]) * 0.1*np.diff(lim)
            return lim

        lim_V = get_lim('Cavity', 'V', ['cRv', 'Ra', 'La', 'cLv']) * 1e6
        lim_V[0] = 0
        lim_p = get_lim('Cavity', 'p', ['cRv', 'Ra', 'La', 'cLv']) / 133
        lim_p[0] = np.min([lim_p[0], 0])
        lim_Ls = get_lim('Patch2022', 'l_s')
        lim_Sf = get_lim('Patch2022', 'Sf') * 1e-3
        lim_q = get_lim('Valve2022', 'q',
                        ['LaLv', 'RaRv', 'LvSyArt', 'RaPuArt']) * 1e6

        all_lim = [lim_V, lim_p, lim_Ls, lim_Sf, lim_q]
        if (np.any(np.isnan(all_lim)) or np.any(np.isinf(all_lim))):
            lim_V = [0, 200]
            lim_p = [0, 150]
            lim_Ls = [1.5, 2.0]
            lim_Sf = [0, 100]
            lim_q = [-1e-3, 1e-3]

        # Pressure Volume plot
        axPV = plt.subplot2grid(grid_size, (0, 17), rowspan=15, colspan=15, fig=fig)
        axPV.plot(self['Cavity']['V'][:, 'cLv']*1e6, self['Cavity']['p'][:, 'cLv']/133)
        axPV.plot(self['Cavity']['V'][:, 'cRv']*1e6, self['Cavity']['p'][:, 'cRv']/133)
        axPV.plot(self['Cavity']['V'][:, 'La']*1e6, self['Cavity']['p'][:, 'La']/133)
        axPV.plot(self['Cavity']['V'][:, 'Ra']*1e6, self['Cavity']['p'][:, 'Ra']/133)
        axPV.spines[['top', 'right']].set_visible(False)
        axPV.set_title('Pressure-Volume loop', weight='bold')
        axPV.set_xlabel('Volume [mL]')
        axPV.set_ylabel('Pressure [mmHg]')
        axPV.spines[['bottom', 'left']].set_position(('outward', 5))

        ylabel_x_left = -0.25
        ylabel_x_right = 1.25

        # Volumes
        t = self['Solver']['t']*1e3
        t -= t[0]

        axVRv = plt.subplot2grid(grid_size, (0, 0), rowspan=8, colspan=6, fig=fig)
        axVRv.plot(t, self['Cavity']['V'][:, 'cRv']*1e6)
        axVRv.plot(t, self['Cavity']['V'][:, 'Ra']*1e6)
        axVRv.set_ylim(lim_V)
        axVRv.set_ylabel('Volume\n[mL]')
        axVRv.spines[['top', 'right']].set_visible(False)
        axVRv.set_title('Right Heart')
        # axVRv.set_xticks([])
        axVRv.tick_params(axis='both', direction='in')
        axVRv.yaxis.set_label_coords(ylabel_x_left, 0.5)


        axVLv = plt.subplot2grid(grid_size, (0, 6), rowspan=8, colspan=6, fig=fig)
        axVLv.plot(t, self['Cavity']['V'][:, 'cLv']*1e6)
        axVLv.plot(t, self['Cavity']['V'][:, 'La']*1e6)
        axVLv.set_ylabel('Volume\n[mL]')
        axVLv.set_ylim(lim_V)
        axVLv.yaxis.set_ticks_position('right')
        axVLv.yaxis.set_label_position('right')
        axVLv.spines['right'].set_position(('outward', 0))
        axVLv.spines[['top', 'left']].set_visible(False)
        axVLv.set_title('Left Heart')
        # axVLv.set_xticks([])
        axVLv.tick_params(axis='both', direction='in')
        axVLv.yaxis.set_label_coords(ylabel_x_right, 0.5)

        # Pressures
        axpRv = plt.subplot2grid(grid_size, (8, 0), rowspan=8, colspan=6, fig=fig)
        axpRv.plot(t, self['Cavity']['p'][:, 'cRv']/133)
        axpRv.plot(t, self['Cavity']['p'][:, 'Ra']/133)
        axpRv.plot(t, self['Cavity']['p'][:, 'PuArt']/133)
        axpRv.spines[['top', 'right']].set_visible(False)
        # axpRv.set_xticks([])
        axpRv.tick_params(axis='both', direction='in')
        axpRv.set_ylim(lim_p)
        axpRv.set_ylabel('Pressure\n[mmHg]')
        axpRv.yaxis.set_label_coords(ylabel_x_left, 0.5)

        axpLv = plt.subplot2grid(grid_size, (8, 6), rowspan=8, colspan=6, fig=fig)
        axpLv.plot(t, self['Cavity']['p'][:, 'cLv']/133)
        axpLv.plot(t, self['Cavity']['p'][:, 'La']/133)
        axpLv.plot(t, self['Cavity']['p'][:, 'SyArt']/133)
        axpLv.yaxis.set_ticks_position('right')
        axpLv.yaxis.set_label_position('right')
        axpLv.spines['right'].set_position(('outward', 0))
        axpLv.spines[['top', 'left']].set_visible(False)
        # axpLv.set_xticks([])
        axpLv.tick_params(axis='both', direction='in')
        axpLv.set_ylim(lim_p)
        axpLv.set_ylabel('Pressure\n[mmHg]')
        axpLv.yaxis.set_label_coords(ylabel_x_right, 0.5)

        # Valves
        ax = plt.subplot2grid(grid_size, (16, 0), rowspan=6, colspan=6, fig=fig)
        ax.plot(t, self['Valve2022']['q'][:, 'RaRv']*1e6)
        ax.plot(t, self['Valve2022']['q'][:, 'RvPuArt']*1e6)
        ax.spines[['top', 'right']].set_visible(False)
        ax.set_ylim(lim_q)
        # ax.set_xticks([])
        ax.set_ylabel('Flow\n[mL/s]')
        ax.yaxis.set_label_coords(ylabel_x_left, 0.5)

        ax = plt.subplot2grid(grid_size, (16, 6), rowspan=6, colspan=6, fig=fig)
        ax.plot(t, self['Valve2022']['q'][:, 'LaLv']*1e6)
        ax.plot(t, self['Valve2022']['q'][:, 'LvSyArt']*1e6)
        ax.spines[['top', 'left']].set_visible(False)
        ax.set_ylim(lim_q)
        ax.yaxis.set_ticks_position('right')
        ax.yaxis.set_label_position('right')
        # ax.set_xticks([])
        ax.set_ylabel('Flow\n[mL/s]')
        ax.yaxis.set_label_coords(ylabel_x_right, 0.5)

        # Stress
        ax = plt.subplot2grid(grid_size, (22, 0), rowspan=4, colspan=6, fig=fig)
        ax.plot(t, self['Patch2022']['Sf'][:, 'pRv0']*1e-3)
        ax.plot(t, self['Patch2022']['Sf'][:, 'pRa0']*1e-3)
        ax.spines[['top', 'right']].set_visible(False)
        # ax.set_xticks([])
        ax.set_ylim(lim_Sf)
        ax.set_ylabel('Total\nstress [kPa]')
        ax.yaxis.set_label_coords(ylabel_x_left, 0.5)

        ax = plt.subplot2grid(grid_size, (22, 6), rowspan=4, colspan=6, fig=fig)
        ax.plot(t, self['Patch2022']['Sf'][:, 'pLv0']*1e-3)
        ax.plot(t, self['Patch2022']['Sf'][:, 'pSv0']*1e-3)
        ax.plot(t, self['Patch2022']['Sf'][:, 'pLa0']*1e-3)
        ax.spines[['top', 'left']].set_visible(False)
        ax.yaxis.set_ticks_position('right')
        ax.yaxis.set_label_position('right')
        # ax.set_xticks([])
        ax.set_ylim(lim_Sf)
        ax.set_ylabel('Total\nstress [kPa]')
        ax.yaxis.set_label_coords(ylabel_x_right, 0.5)

        # Sarcomere Length
        ax = plt.subplot2grid(grid_size, (26, 0), rowspan=6, colspan=6, fig=fig)
        ax.plot(t, self['Patch2022']['l_s'][:, 'pRv0'])
        ax.plot(t, self['Patch2022']['l_s'][:, 'pRa0'])
        ax.spines[['top', 'right']].set_visible(False)
        ax.spines['bottom'].set_position(('outward', 5))
        ax.set_ylim(lim_Ls)
        ax.set_ylabel('Sarcomere\nlength [$\mu$m]')
        ax.yaxis.set_label_coords(ylabel_x_left, 0.5)

        ax = plt.subplot2grid(grid_size, (26, 6), rowspan=6, colspan=6, fig=fig)
        ax.plot(t, self['Patch2022']['l_s'][:, 'pLv0'])
        ax.plot(t, self['Patch2022']['l_s'][:, 'pSv0'])
        ax.plot(t, self['Patch2022']['l_s'][:, 'pLa0'])
        ax.spines[['top', 'left']].set_visible(False)
        ax.spines['bottom'].set_position(('outward', 5))
        ax.yaxis.set_ticks_position('right')
        ax.yaxis.set_label_position('right')
        ax.set_ylim(lim_Ls)
        ax.set_ylabel('Sarcomere\nlength [$\mu$m]')
        ax.yaxis.set_label_coords(ylabel_x_right, 0.5)

        # ax.set_xlabel('Time [ms]')
        # ax.xaxis.set_label_coords(0, -0.3)


        # Plot TriSeg
        titles = ['Pre-A', 'Onset QRS', 'Peak LV \n pressure', 'AV close']
        idx = [0,
               np.argmax(np.diff(self['Patch2022']['C'][:, 'pLv0'])>0),
               np.argmax(self['Cavity']['p'][:, 'cLv']),
               len(t) - 1 - np.argmax(
                   np.diff(self['Valve2022']['q'][:, 'LvSyArt'][::-1])>0)
               ]

        for i in range(4):
            ax = plt.subplot2grid(grid_size, (26, 16+4*i),
                                  rowspan=5, colspan=4, fig=fig)
            triseg2022(self, ax, idx[i])
            ax.spines[['top', 'right', 'bottom', 'left']].set_visible(False)
            ax.set_xticks([])
            ax.set_yticks([])
            plt.xlabel(titles[i], fontsize=12)

        # Plot settings
        plt.subplots_adjust(
            top=0.96,
            bottom=0.05,
            left=0.075,
            right=0.98,
            hspace=5,
            wspace=0.5)
        plt.draw()

        # Plot MMode
        ax_mmode = plt.subplot2grid(grid_size, (17, 17),
                              rowspan=8, colspan=15, fig=fig)
        circadapt.plot.triseg.mmode(self, ax_mmode)
        ax_mmode.axhline(0, c='k', ls='--')
        ax_mmode.spines[['top', 'right']].set_visible(False)

        # Plot Y
        # ax_mmode = plt.subplot2grid(grid_size, (17, 25),
        #                       rowspan=8, colspan=7, fig=fig)
        ax_mmode.plot(t, self['TriSeg2022']['Y']*1e3 * np.array([[1, -1]]), c='k')
        ax_mmode.spines[['top', 'right']].set_visible(False)
        plt.ylabel('MMode and Y [mm]')