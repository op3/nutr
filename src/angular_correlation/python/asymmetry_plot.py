# This file is part of nutr.

# nutr is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# nutr is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with nutr.  If not, see <https://www.gnu.org/licenses/>.

# Copyright (C) 2020 Udo Friman-Gayer

import os
import warnings
os.chdir('@ANGCORR_PYTHON_DIR@')

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.mplot3d import axes3d
import numpy as np

from angular_correlation import angular_correlation

class AngularCorrelation:
    def __init__(self, ini_sta, cas_ste, delta_dict):
        self.initial_state = ini_sta
        self.cascade_steps = cas_ste
        self.delta_dict = delta_dict
        self.n_variable_deltas = 0
	
        delta_1_found = False
        delta_2_found = False

        for cas_ste_delta in self.delta_dict:
            if cas_ste_delta == 'delta_1' and not delta_1_found: 
                delta_1_found = True
                self.n_variable_deltas += 1
            if cas_ste_delta == 'delta_2' and not delta_2_found: 
                delta_2_found = True
                self.n_variable_deltas += 1

    def asymmetry_grid(self, n_delta_steps=101, abs_delta_max=100.):
        arctan_deltas = np.linspace(
            np.arctan(-abs_delta_max),
            np.arctan( abs_delta_max),
            n_delta_steps)
        deltas = np.tan(arctan_deltas)

        asy_45 = np.zeros([n_delta_steps]*self.n_variable_deltas)
        asy_90 = np.zeros([n_delta_steps]*self.n_variable_deltas)

        if self.n_variable_deltas == 1:
            for i, delta in enumerate(deltas):
                self.set_deltas([delta])
                asy_45[i], asy_90[i] = self.calculate_asymmetry()

        else:
            for i, delta1 in enumerate(deltas):
                for j, delta2 in enumerate(deltas):
                    self.set_deltas([delta1, delta2])
                    asy_45[i][j], asy_90[i][j] = self.calculate_asymmetry()
        
        return (arctan_deltas, asy_45, asy_90)
        
    def set_deltas(self, deltas):
        for i, cas_ste_delta in enumerate(self.delta_dict):
            if isinstance(cas_ste_delta, (int, float)):
                self.cascade_steps[i][0].delta = cas_ste_delta
            if cas_ste_delta == 'delta_1':
                self.cascade_steps[i][0].delta = deltas[0]
            if cas_ste_delta == 'delta_2':
                self.cascade_steps[i][0].delta = deltas[1]
            
    def calculate_asymmetry(self):
        w_45_0  = angular_correlation(0.25*np.pi, 0.       , self.initial_state, self.cascade_steps)
        w_45_90 = angular_correlation(0.25*np.pi, 0.5*np.pi, self.initial_state, self.cascade_steps)
        w_90_0  = angular_correlation(0.50*np.pi, 0.       , self.initial_state, self.cascade_steps)
        w_90_90 = angular_correlation(0.50*np.pi, 0.5*np.pi, self.initial_state, self.cascade_steps)
        
        return ((w_45_0 - w_45_90)/(w_45_0 + w_45_90),
                (w_90_0 - w_90_90)/(w_90_0 + w_90_90))

class AsymmetryPlotter:
    def __init__(self, ang_cor, arctan_deltas, asy_45, asy_90, scale_asymmetries=True):

        ## Input data
        self.ang_cor = ang_cor
        self.arctan_deltas = arctan_deltas
        self.asy_45 = asy_45
        self.asy_90 = asy_90

        ## Determines the plot range for asymmetries.
        # If scale_asymmetries is False, they will be plotted in the range [-1, 1],
        # otherwise in the range [min(A(δ)), max(A(δ))].
        self.scale_asymmetries = scale_asymmetries
        # This factor can be used to create a margin around the plotted data.
        # If the data are in the range [a, b], a margin factor which is not unity
        # will set a plot range of [a - margin_factor*(b-a), b + margin_factor*(b-a)].
        self.margin_factor = 1.1

        # Axis labels for asymmetries
        self.asy_45_label = r'$A(\theta = 45^\circ)$'
        self.asy_90_label = r'$A(\theta = 90^\circ)$'

        self.asy_45_single_color = 'crimson'
        self.asy_90_single_color = 'purple'
        self.asy_asy_single_color = 'forestgreen'

        del_ticks_for_arctan = np.array([-10., -1.5, -0.4, 0.,
                                         0.4, 1.5, 10.])
        self.del_ticks = np.arctan(del_ticks_for_arctan)
        self.del_tick_labels = ['{:4.1f}'.format(tick)
                                  for tick in del_ticks_for_arctan]

        self.asy_45_lim = [-self.margin_factor, self.margin_factor]
        self.asy_90_lim = [-self.margin_factor, self.margin_factor]

        if self.scale_asymmetries:
            asy_45_min = np.min(self.asy_45)
            asy_45_max = np.max(self.asy_45)
            asy_45_range = asy_45_max - asy_45_min
            self.asy_45_lim = [asy_45_min - 0.1*asy_45_range, asy_45_max + 0.1*asy_45_range]
            asy_90_min = np.min(self.asy_90)
            asy_90_max = np.max(self.asy_90)
            asy_90_range = asy_90_max - asy_90_min
            self.asy_90_lim = [asy_90_min - 0.1*asy_90_range, asy_90_max + 0.1*asy_90_range]

        self.asy_ticks = [-1., -0.5, 0., 0.5, 1.]
        self.asy_tick_labels = ['{:4.1f}'.format(tick) for tick in self.asy_ticks]

        self.arctan_del_lim = [-0.5*np.pi*self.margin_factor,
                   0.5*np.pi*self.margin_factor]
        self.arctan_del_ticks = [-0.5*np.pi, -0.25*np.pi, 0., 0.25*np.pi, 0.5*np.pi]
        self.arctan_del_tick_labels = [r'$-\pi/2$', r'$-\pi/4$', 
                           '$0$', r'$\pi/4$', r'$\pi/2$']

    def plot_single_2d(self, delta_label, delta_labels_level_scheme, returns_to_initial_state=True, output_file=None):

        if not isinstance(self.asy_45[0], (int, float)):
            warnings.warn('Line plot requested when two multipole mixing ratios were varied. Assuming delta_1 = delta_2.')
            asy_45_single = np.diag(self.asy_45)
            asy_90_single = np.diag(self.asy_90)

            # Calculate new plot limits
            asy_45_min = np.min(asy_45_single)
            asy_45_max = np.max(asy_45_single)
            asy_45_range = asy_45_max - asy_45_min
            asy_45_single_lim = [asy_45_min - 0.1*asy_45_range, asy_45_max + 0.1*asy_45_range]
            asy_90_min = np.min(asy_90_single)
            asy_90_max = np.max(asy_90_single)
            asy_90_range = asy_90_max - asy_90_min
            asy_90_single_lim = [asy_90_min - 0.1*asy_90_range, asy_90_max + 0.1*asy_90_range]

        else:
            asy_45_single = self.asy_45
            asy_90_single = self.asy_90
            
            asy_45_single_lim = self.asy_45_lim
            asy_90_single_lim = self.asy_90_lim

        aux_line_asy_45_style = '--'
        aux_line_asy_90_style = '-'
        aux_line_color = 'grey'

        fontsize_ticks = 9

        markersize = 8
        markersize_asy_45 = 14
        markersize_asy_90 = 8
        delta_zero_marker = 'o'
        delta_infinity_marker = 'P'
        asy_45_min_marker = '+'
        asy_45_max_marker = 'x'
        asy_90_min_marker = 'v'
        asy_90_max_marker = '^'

        delta_zero_index = np.argmin(np.abs(self.arctan_deltas))
        if self.arctan_deltas[delta_zero_index] != 0.:
            warnings.warn('The value closest to δ = 0 which could be found is δ = {:f}'.format(self.arctan_deltas[delta_zero_index]))
        asy_45_min_index = np.argmin(asy_45_single)
        asy_45_max_index = np.argmax(asy_45_single)
        asy_90_min_index = np.argmin(asy_90_single)
        asy_90_max_index = np.argmax(asy_90_single)

        fig, ax = plt.subplots(2,2, figsize=(7, 7))
        plt.subplots_adjust(wspace=0.1, hspace=0.1)

        ax[0][0].tick_params(labelsize=fontsize_ticks)
        ax[0][0].set_xlim(asy_45_single_lim)
        ax[0][0].set_xticks([])
        ax[0][0].set_ylabel('arctan(' + delta_label + ')')
        ax[0][0].set_ylim(self.arctan_del_lim)
        ax[0][0].set_yticks(self.arctan_del_ticks)
        ax[0][0].set_yticklabels(self.arctan_del_tick_labels)

        ax[0][0].plot([asy_45_single[delta_zero_index]]*2,
                      [self.arctan_del_lim[0], self.arctan_deltas[delta_zero_index]],
                      aux_line_asy_45_style, color=aux_line_color)
        ax[0][0].plot([asy_45_single[asy_45_min_index]]*2,
                      [self.arctan_del_lim[0], self.arctan_deltas[asy_45_min_index]],
                      aux_line_asy_45_style, color=aux_line_color)
        ax[0][0].plot([asy_45_single[asy_45_max_index]]*2,
                      [self.arctan_del_lim[0], self.arctan_deltas[asy_45_max_index]],
                      aux_line_asy_45_style, color=aux_line_color)

        ax[0][0].plot(asy_45_single, self.arctan_deltas, color=self.asy_45_single_color)
        ax[0][0].plot(asy_45_single[delta_zero_index], [0.], delta_zero_marker,
                      markersize=markersize, color='black')
        ax[0][0].plot(asy_45_single[0], self.arctan_deltas[0], delta_infinity_marker,
                      markersize=markersize, color='black')
        ax[0][0].plot(asy_45_single[-1], self.arctan_deltas[-1], delta_infinity_marker,
                      markersize=markersize, color='black')
        ax[0][0].plot(asy_45_single[asy_45_min_index], self.arctan_deltas[asy_45_min_index],
                      marker=asy_45_min_marker, markersize=markersize_asy_45, color='black')
        ax[0][0].plot(asy_45_single[asy_45_max_index], self.arctan_deltas[asy_45_max_index],
                      marker=asy_45_max_marker, markersize=markersize_asy_45, color='black')

        ax00x = ax[0][0].twiny()
        ax00x.tick_params(labelsize=fontsize_ticks)
        ax00x.set_xlabel(self.asy_45_label)
        ax00x.set_xlim(asy_45_single_lim)
        if not self.scale_asymmetries:
            ax00x.set_xticks(self.asy_ticks)

        ax00y = ax[0][0].twinx()
        ax00y.tick_params(labelsize=fontsize_ticks)
        ax00y.set_ylabel(delta_label)
        ax00y.set_ylim(self.arctan_del_lim)
        ax00y.set_yticks(self.del_ticks)
        ax00y.set_yticklabels(self.del_tick_labels)

        ax[0][1].axis('off')
        ax[0][1].set_xlim(-1., 1.)
        ax[0][1].set_ylim(-1., 1.)
        lsplt = LevelSchemePlotter(ax[0][1], self.ang_cor.initial_state, self.ang_cor.cascade_steps,
                                   delta_labels_level_scheme,
                                   returns_to_initial_state=returns_to_initial_state)
        lsplt.plot()

        ax[1][0].tick_params(labelsize=fontsize_ticks)
        ax[1][0].set_xlabel(self.asy_45_label)
        ax[1][0].set_xlim(asy_45_single_lim)
        if not self.scale_asymmetries:
            ax[1][0].set_xticks(self.asy_ticks)
            ax[1][0].set_xticklabels(self.asy_tick_labels)
        ax[1][0].set_ylabel(self.asy_90_label)
        ax[1][0].set_ylim(asy_90_single_lim)
        if not self.scale_asymmetries:
            ax[1][0].set_yticks(self.asy_ticks)
            ax[1][0].set_yticklabels(self.asy_tick_labels)

        ax[1][0].plot([asy_45_single[delta_zero_index], self.asy_45_lim[1]],
                      [asy_90_single[delta_zero_index]]*2, aux_line_asy_90_style, color=aux_line_color)
        ax[1][0].plot([asy_45_single[asy_90_max_index], self.asy_45_lim[1]],
                      [asy_90_single[asy_90_max_index]]*2, aux_line_asy_90_style, color=aux_line_color)
        ax[1][0].plot([asy_45_single[asy_90_min_index], self.asy_45_lim[1]],
                      [asy_90_single[asy_90_min_index]]*2, aux_line_asy_90_style, color=aux_line_color)

        ax[1][0].plot([asy_45_single[delta_zero_index]]*2,
                      [asy_90_single[delta_zero_index], self.asy_90_lim[1]],
                      aux_line_asy_45_style, color=aux_line_color)
        ax[1][0].plot([asy_45_single[asy_45_min_index]]*2,
                      [asy_90_single[asy_45_min_index], self.asy_90_lim[1]],
                      aux_line_asy_45_style, color=aux_line_color)
        ax[1][0].plot([asy_45_single[asy_45_max_index]]*2,
                      [asy_90_single[asy_45_max_index], self.asy_90_lim[1]],
                      aux_line_asy_45_style, color=aux_line_color)

        ax[1][0].plot(asy_45_single, asy_90_single, color=self.asy_asy_single_color)
        ax[1][0].plot(asy_45_single[delta_zero_index], asy_90_single[delta_zero_index], delta_zero_marker,
                      markersize=markersize, color='black')
        ax[1][0].plot(asy_45_single[0], asy_90_single[0], delta_infinity_marker,
                      markersize=markersize, color='black')
        ax[1][0].plot(asy_45_single[asy_45_min_index], asy_90_single[asy_45_min_index],
                      marker=asy_45_min_marker, markersize=markersize_asy_45, color='black')
        ax[1][0].plot(asy_45_single[asy_45_max_index], asy_90_single[asy_45_max_index],
                      marker=asy_45_max_marker, markersize=markersize_asy_45, color='black')
        ax[1][0].plot(asy_45_single[asy_90_min_index], asy_90_single[asy_90_min_index],
                      marker=asy_90_min_marker, markersize=markersize_asy_90, color='black')
        ax[1][0].plot(asy_45_single[asy_90_max_index], asy_90_single[asy_90_max_index],
                      marker=asy_90_max_marker, markersize=markersize_asy_90, color='black')

        ax[1][1].tick_params(labelsize=fontsize_ticks)
        ax[1][1].set_xlabel('arctan(' + delta_label + ')')
        ax[1][1].set_xlim(self.arctan_del_lim)
        ax[1][1].set_xticks(self.arctan_del_ticks)
        ax[1][1].set_xticklabels(self.arctan_del_tick_labels)
        ax[1][1].set_yticks([])
        ax[1][1].set_ylim(asy_90_single_lim)

        ax[1][1].plot([self.arctan_del_lim[0], 0.], [asy_90_single[delta_zero_index]]*2,
                      aux_line_asy_90_style, color=aux_line_color)
        ax[1][1].plot([self.arctan_del_lim[0], self.arctan_deltas[asy_90_min_index]],
                      [asy_90_single[asy_90_min_index]]*2,
                      aux_line_asy_90_style, color=aux_line_color)
        ax[1][1].plot([self.arctan_del_lim[0], self.arctan_deltas[asy_90_max_index]],
                      [asy_90_single[asy_90_max_index]]*2,
                      aux_line_asy_90_style, color=aux_line_color)

        ax[1][1].plot(self.arctan_deltas, asy_90_single, color=self.asy_90_single_color)
        ax[1][1].plot(self.arctan_deltas[0], asy_90_single[0], delta_infinity_marker,
                      markersize=markersize, color='black')
        ax[1][1].plot(self.arctan_deltas[-1], asy_90_single[-1], delta_infinity_marker,
                      markersize=markersize, color='black')
        ax[1][1].plot([0.], asy_90_single[delta_zero_index], delta_zero_marker,
                      markersize=markersize, color='black')
        ax[1][1].plot(self.arctan_deltas[asy_90_min_index], asy_90_single[asy_90_min_index],
                      marker=asy_90_min_marker, markersize=markersize_asy_90, color='black')
        ax[1][1].plot(self.arctan_deltas[asy_90_max_index], asy_90_single[asy_90_max_index],
                      marker=asy_90_max_marker, markersize=markersize_asy_90, color='black')

        ax11x = ax[1][1].twinx()
        ax11x.tick_params(labelsize=fontsize_ticks)
        ax11x.set_ylim(asy_90_single_lim)
        if not self.scale_asymmetries:
            ax11x.set_yticks(self.asy_ticks)
            ax11x.set_yticklabels(self.asy_tick_labels)
        ax11x.set_ylabel(self.asy_90_label)

        ax11y = ax[1][1].twiny()
        ax11y.tick_params(labelsize=fontsize_ticks)
        ax11y.set_xlabel(delta_label)
        ax11y.set_xlim(self.arctan_del_lim)
        ax11y.set_xticks(self.del_ticks)
        ax11y.set_xticklabels(self.del_tick_labels)

        if output_file:
            plt.savefig(output_file)

    def plot_single_3d(self, delta_label, output_file=None):

        if not isinstance(self.asy_45[0], (int, float)):
            warnings.warn('Line plot requested when two multipole mixing ratios were varied. Assuming delta_1 = delta_2.')
            asy_45_single = np.diag(self.asy_45)
            asy_90_single = np.diag(self.asy_90)

            # Calculate new plot limits
            asy_45_min = np.min(asy_45_single)
            asy_45_max = np.max(asy_45_single)
            asy_45_range = asy_45_max - asy_45_min
            asy_45_single_lim = [asy_45_min - 0.1*asy_45_range, asy_45_max + 0.1*asy_45_range]
            asy_90_min = np.min(asy_90_single)
            asy_90_max = np.max(asy_90_single)
            asy_90_range = asy_90_max - asy_90_min
            asy_90_single_lim = [asy_90_min - 0.1*asy_90_range, asy_90_max + 0.1*asy_90_range]

        else:
            asy_45_single = self.asy_45
            asy_90_single = self.asy_90
            
            asy_45_single_lim = self.asy_45_lim
            asy_90_single_lim = self.asy_90_lim
        
        line_width = 3
        
        fig = plt.figure(figsize=(6,5))
        ax = fig.gca(projection='3d')

        ax.set_xlabel(self.asy_45_label)
        ax.set_xlim(asy_45_single_lim)

        ax.set_ylabel(self.asy_90_label)
        ax.set_ylim(asy_90_single_lim)

        ax.set_zlabel('arctan(' + delta_label + ')')
        ax.set_zlim(self.arctan_del_lim)
        ax.set_zticks(self.arctan_del_ticks)
        ax.set_zticklabels(self.arctan_del_tick_labels)

        ax.plot(asy_45_single, [asy_90_single_lim[1]]*len(self.arctan_deltas),
                self.arctan_deltas, color=self.asy_45_single_color, linewidth=line_width)
        ax.plot([asy_45_single_lim[0]]*len(self.arctan_deltas), asy_90_single, 
                self.arctan_deltas, color=self.asy_90_single_color, linewidth=line_width)
        ax.plot(asy_45_single, asy_90_single, 
                [self.arctan_del_lim[0]]*len(self.arctan_deltas),
                color=self.asy_asy_single_color, linewidth=line_width)
        
        for i in range(len(self.arctan_deltas)):
            ax.plot([asy_45_single[i]]*2, [asy_90_single[i], asy_90_single_lim[1]],
                    [self.arctan_deltas[i]]*2, color=self.asy_45_single_color, alpha=0.2)
            ax.plot([asy_45_single_lim[0], asy_45_single[i]], [asy_90_single[i]]*2, 
                    [self.arctan_deltas[i]]*2, color=self.asy_90_single_color, alpha=0.2)
            ax.plot([asy_45_single[i]]*2, [asy_90_single[i]]*2, 
                    [self.arctan_del_lim[0], self.arctan_deltas[i]],
                    color=self.asy_asy_single_color, alpha=0.2)

        ax.plot(asy_45_single, asy_90_single, self.arctan_deltas, 
                color='black', linewidth=line_width)

        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file)

    def plot_double_contour(self, delta_labels, output_file=None):

        arctan_deltas_1, arctan_deltas_2 = np.meshgrid(self.arctan_deltas, self.arctan_deltas)
        if isinstance(self.asy_45[0], (int, float)):
            warnings.warn('Contour plot requested when only a single multipole mixing ratio was varied.')
            asy_45_double = np.zeros((len(self.arctan_deltas), len(self.arctan_deltas)))
            asy_90_double = np.zeros((len(self.arctan_deltas), len(self.arctan_deltas)))
            for i in range(len(self.arctan_deltas)):
                asy_45_double[i] = self.asy_45
                asy_90_double[i] = self.asy_90
        else:
            asy_45_double = self.asy_45
            asy_90_double = self.asy_90

        contour_levels = 10
        
        alpha_shadow = 0.6
        color_shadow = 'pink'
        fontsize_axis_label = 12

        fig = plt.figure(figsize=(6, 8))
        gs = gridspec.GridSpec(2, 2, width_ratios=(1, 0.1))

        ax0 = plt.subplot(gs[0])
        ax0.set_xticks([])
        ax0.set_xlim(self.arctan_del_lim)        
        ax0.set_yticks(self.arctan_del_ticks)
        ax0.set_yticklabels(self.arctan_del_tick_labels)
        ax0.set_ylim(self.arctan_del_lim)

        cs0 = ax0.contourf(arctan_deltas_1, arctan_deltas_2, asy_45_double,
                           levels=contour_levels, cmap='viridis')
        ax0.contour(arctan_deltas_1, arctan_deltas_2, asy_45_double,
                    levels=contour_levels, colors='black')
        ax0.contour(arctan_deltas_1, arctan_deltas_2, asy_90_double,
                    levels=contour_levels, colors=color_shadow, alpha=alpha_shadow)
        ax0.set_ylabel('arctan(' + delta_labels[1] + ')', fontsize=fontsize_axis_label)
        ax1 = plt.subplot(gs[1])
        cb0 = fig.colorbar(cs0, ax1)
        cb0.set_label(self.asy_45_label, fontsize=fontsize_axis_label)

        ax0x = ax0.twiny()
        ax0x.set_xlim(self.arctan_del_lim)
        ax0x.set_xlabel(delta_labels[0], fontsize=fontsize_axis_label)
        ax0x.set_xticks(self.del_ticks)
        ax0x.set_xticklabels(self.del_tick_labels)

        ax0y = ax0.twinx()
        ax0y.set_ylim(self.arctan_del_lim)
        ax0y.set_ylabel(delta_labels[1], fontsize=fontsize_axis_label)
        ax0y.set_yticks(self.del_ticks)
        ax0y.set_yticklabels(self.del_tick_labels)        

        ax2 = plt.subplot(gs[2])
        ax2.set_xticks(self.arctan_del_ticks)
        ax2.set_xticklabels(self.arctan_del_tick_labels)
        ax2.set_xlim(self.arctan_del_lim)        
        ax2.set_yticks(self.arctan_del_ticks)
        ax2.set_yticklabels(self.arctan_del_tick_labels)
        ax2.set_ylim(self.arctan_del_lim)        
        cs2 = ax2.contourf(arctan_deltas_1, arctan_deltas_2, asy_90_double, 
                           levels=contour_levels, cmap='viridis')
        ax2.contour(arctan_deltas_1, arctan_deltas_2, asy_90_double, 
                    levels=contour_levels, colors='black')
        ax2.contour(arctan_deltas_1, arctan_deltas_2, asy_45_double, 
                    levels=contour_levels, colors=color_shadow, alpha=alpha_shadow)
        ax2.set_xlabel('arctan(' + delta_labels[0] + ')', fontsize=fontsize_axis_label)
        ax2.set_ylabel('arctan(' + delta_labels[1] + ')', fontsize=fontsize_axis_label)

        ax2y = ax2.twinx()
        ax2y.set_ylim(self.arctan_del_lim)
        ax2y.set_ylabel(delta_labels[1], fontsize=fontsize_axis_label)
        ax2y.set_yticks(self.del_ticks)
        ax2y.set_yticklabels(self.del_tick_labels) 

        ax3 = plt.subplot(gs[3])
        cb2 = fig.colorbar(cs2, ax3)
        cb2.set_label(self.asy_90_label, fontsize=fontsize_axis_label)

        plt.tight_layout()
        
        if output_file:
            plt.savefig(output_file)

    def plot_double_contour_inverse(self, delta_labels, output_file=None):

        if isinstance(self.asy_45[0], (int, float)):
            raise ValueError('Inverse contour plot requested when only one multipole mixing ratio was varied. This is not possible.')

        fontsize_ticks = 9

        label_delta_min = r'$\delta_{min}$'
        label_delta_max = r'$\delta_{max}$'
        label_delta_diff = label_delta_max + ' - ' + label_delta_min

        label_arctan_delta_min = r'$\mathrm{arctan}(\delta_{min})$'
        label_arctan_delta_max = r'$\mathrm{arctan}(\delta_{max})$'
        label_arctan_delta_diff = label_arctan_delta_max + ' - ' + label_arctan_delta_min

        arctan_delta_ticks_diff = [0., 0.25*np.pi, 0.5*np.pi, 0.75*np.pi, np.pi]
        arctan_delta_labels_diff = [r'$0$', r'$\pi/4$', '$\pi/2$', r'$3\pi/4$', r'$\pi$']

        arctan_deltas_1, arctan_deltas_2 = np.meshgrid(self.arctan_deltas, self.arctan_deltas)

        n_bins = 100
        bins_asy_45 = np.linspace(self.asy_45_lim[0], self.asy_45_lim[1], n_bins)
        bins_asy_90 = np.linspace(self.asy_90_lim[0], self.asy_90_lim[1], n_bins)

        hist_min_1 = np.ones((n_bins, n_bins))*np.pi
        hist_max_1 = np.ones((n_bins, n_bins))*-np.pi
        hist_counts_1 = np.zeros((n_bins, n_bins))
        hist_min_2 = np.ones((n_bins, n_bins))*np.pi
        hist_max_2 = np.ones((n_bins, n_bins))*-np.pi
        hist_counts_2 = np.zeros((n_bins, n_bins))

        for i in range(len(self.arctan_deltas)):
            for j in range(len(self.arctan_deltas)):
                asy_45_value = self.asy_45[i][j]
                asy_90_value = self.asy_90[i][j]

                asy_45_bin = np.argmin(np.abs(bins_asy_45-asy_45_value))
                asy_90_bin = np.argmin(np.abs(bins_asy_90-asy_90_value))

                arctan_delta_1 = arctan_deltas_1[i][j]
                
                if arctan_delta_1 < hist_min_1[asy_90_bin][asy_45_bin]:
                    hist_min_1[asy_90_bin][asy_45_bin] = arctan_delta_1
                if arctan_delta_1 > hist_max_1[asy_90_bin][asy_45_bin]:
                    hist_max_1[asy_90_bin][asy_45_bin] = arctan_delta_1
                hist_counts_1[asy_90_bin][asy_45_bin] += 1

                arctan_delta_2 = arctan_deltas_2[i][j]

                if arctan_delta_2 < hist_min_2[asy_90_bin][asy_45_bin]:
                    hist_min_2[asy_90_bin][asy_45_bin] = arctan_delta_2
                if arctan_delta_2 > hist_max_2[asy_90_bin][asy_45_bin]:
                    hist_max_2[asy_90_bin][asy_45_bin] = arctan_delta_2
                hist_counts_2[asy_90_bin][asy_45_bin] += 1

        bins_asy_45_grid, bins_asy_90_grid = np.meshgrid(bins_asy_45, bins_asy_90)

        hist_min_1[hist_counts_1 < 1] = np.nan
        hist_max_1[hist_counts_1 < 1] = np.nan
        hist_min_2[hist_counts_2 < 1] = np.nan
        hist_max_2[hist_counts_2 < 1] = np.nan

        fig = plt.figure(figsize=(10, 12))
        gs = gridspec.GridSpec(3, 4, width_ratios=(1, 0.1, 1., 0.1))

        ax0 = plt.subplot(gs[0])
        ax0.set_title(r'First column: $\delta_1$')
        ax0.tick_params(labelsize=fontsize_ticks)
        ax0.set_xticklabels([])
        ax0.set_ylabel(r'$A(\theta = 90^\circ)$')
        ax0.grid()
        cs0 = ax0.contourf(
            bins_asy_45_grid,
            bins_asy_90_grid,
            hist_max_1,
            levels=np.linspace(-0.5*np.pi, 0.5*np.pi, 9),
            cmap='coolwarm'
        )
        ax1 = plt.subplot(gs[1])
        cb0 = fig.colorbar(cs0, ax1)
        cb0.set_label(label_delta_max)
        cb0.ax.tick_params(labelsize=fontsize_ticks)
        cb0.set_ticks(self.del_ticks)
        cb0.ax.set_yticklabels(self.del_tick_labels)

        ax2 = plt.subplot(gs[2])
        ax2.set_title(r'Second column: $\delta_2$')
        ax2.tick_params(labelsize=fontsize_ticks)
        ax2.set_xticklabels([])
        ax2.set_yticklabels([])
        ax2.grid()
        cs2 = ax2.contourf(
            bins_asy_45_grid,
            bins_asy_90_grid,
            hist_max_2,
            levels=np.linspace(-0.5*np.pi, 0.5*np.pi, 9),
            cmap='coolwarm'
        )
        ax3 = plt.subplot(gs[3])
        cb2 = fig.colorbar(cs2, ax3)
        cb2.set_label(label_arctan_delta_max)
        cb2.ax.tick_params(labelsize=fontsize_ticks)
        cb2.set_ticks(self.arctan_del_ticks)
        cb2.ax.set_yticklabels(self.arctan_del_tick_labels)

        ax4 = plt.subplot(gs[4])
        ax4.tick_params(labelsize=fontsize_ticks)
        ax4.set_xticklabels([])
        ax4.set_ylabel(r'$A(\theta = 90^\circ)$')
        ax4.grid()
        cs4 = ax4.contourf(
            bins_asy_45_grid,
            bins_asy_90_grid,
            hist_min_1,
            levels=np.linspace(-0.5*np.pi, 0.5*np.pi, 9),
            cmap='coolwarm'
        )
        ax5 = plt.subplot(gs[5])
        cb4 = fig.colorbar(cs4, ax5)
        cb4.set_label(label_delta_min)
        cb4.ax.tick_params(labelsize=fontsize_ticks)
        cb4.set_ticks(self.del_ticks)
        cb4.ax.set_yticklabels(self.del_tick_labels)

        ax6 = plt.subplot(gs[6])
        ax6.tick_params(labelsize=fontsize_ticks)
        ax6.set_xticklabels([])
        ax6.set_yticklabels([])
        ax6.grid()
        cs6 = ax6.contourf(
            bins_asy_45_grid,
            bins_asy_90_grid,
            hist_min_2,
            levels=np.linspace(-0.5*np.pi, 0.5*np.pi, 9),
            cmap='coolwarm'
        )
        ax7 = plt.subplot(gs[7])
        cb6 = fig.colorbar(cs6, ax7)
        cb6.set_label(label_arctan_delta_min)
        cb6.ax.tick_params(labelsize=fontsize_ticks)
        cb6.set_ticks(self.arctan_del_ticks)
        cb6.ax.set_yticklabels(self.arctan_del_tick_labels)

        ax8 = plt.subplot(gs[8])
        ax8.tick_params(labelsize=fontsize_ticks)
        ax8.set_xlabel(r'$A(\theta = 45^\circ)$')
        ax8.grid()
        ax8.set_ylabel(r'$A(\theta = 90^\circ)$')
        cs8 = ax8.contourf(
            bins_asy_45_grid,
            bins_asy_90_grid,
            hist_max_1 - hist_min_1, 
            cmap='inferno', levels=np.linspace(0., np.pi, 9)
        )
        ax9 = plt.subplot(gs[9])
        cb9 = fig.colorbar(cs8, ax9)
        cb9.set_label(label_arctan_delta_diff)
        cb9.ax.tick_params(labelsize=fontsize_ticks)
        cb9.set_ticks(arctan_delta_ticks_diff)
        cb9.ax.set_yticklabels(arctan_delta_labels_diff)

        ax10 = plt.subplot(gs[10])
        ax10.tick_params(labelsize=fontsize_ticks)
        ax10.set_xlabel(r'$A(\theta = 45^\circ)$')
        ax10.set_yticklabels([])
        ax10.grid()
        cs10 = ax10.contourf(
            bins_asy_45_grid,
            bins_asy_90_grid,
            hist_max_2 - hist_min_2,
            cmap='inferno', levels=np.linspace(0., np.pi, 9)
        )
        ax11 = plt.subplot(gs[11])
        cb10 = fig.colorbar(cs10, ax11)
        cb10.set_label(label_arctan_delta_diff)
        cb10.ax.tick_params(labelsize=fontsize_ticks)
        cb10.set_ticks(arctan_delta_ticks_diff)
        cb10.ax.set_yticklabels(arctan_delta_labels_diff)

        fig.align_labels()
        plt.tight_layout()

        if output_file:
            plt.savefig(output_file)

class LevelSchemePlotter:
    def __init__(self, axis, initial_state, cascade_steps, delta_labels, returns_to_initial_state=False):
        self.ax = axis
        self.min_x, self.max_x = axis.get_xlim()
        self.range_x = self.max_x - self.min_x
        self.min_y, self.max_y = axis.get_ylim()
        self.range_y = self.max_y - self.min_y
        self.ini_sta = initial_state
        self.cas_ste = cascade_steps
        self.del_lab = delta_labels
        self.returns_to_initial_state = returns_to_initial_state        

        ## Parameters for the plot
        # Fonts
        self.fontsize = 12
        
        # State lines
        self.state_x = 0.4*self.range_x + self.min_x
        self.state_width = 0.4*self.range_x
        self.intermediate_state_x = 0.55*self.range_x + self.min_x
        self.intermediate_state_width = 0.25*self.range_x

        self.initial_state_y = 0.2*self.range_y + self.min_y
        self.excited_state_y = 0.8*self.range_y + self.min_y

        # State labels
        self.state_label_left_x = 0.25*self.range_x + self.min_x
        self.state_label_right_x = 0.9*self.range_x + self.min_x

        # Transition arrows
        self.excitation_arrow_x = 0.5*self.range_x + self.min_x
        self.decay_arrow_x = 0.7*self.range_x + self.min_x
        self.arrow_head_length = 0.04*self.range_y
        self.arrow_head_width = 0.04*self.range_x

        # Transition labels
        self.excitation_label_left_x = 0.25*self.range_x + self.min_x
        self.decay_label_right_x = 0.9*self.range_x + self.min_x
        
        # Multipole mixing ratio (delta) labels
        self.delta_label_left_x = 0.4*self.range_x + self.min_x
        self.delta_label_right_x = 0.74*self.range_x + self.min_x

    def plot(self):
        # Initial and excited state
        self.ax.plot([self.state_x, self.state_x + self.state_width],
                     [self.initial_state_y]*2, color='black')
        self.ax.text(self.state_label_left_x, self.initial_state_y, r'$' + str(self.ini_sta) + '$',
                     verticalalignment='center', fontsize=self.fontsize)
        self.ax.plot([self.state_x, self.state_x + self.state_width],
                     [self.excited_state_y]*2, color='black')
        self.ax.text(self.state_label_left_x, self.excited_state_y, r'$' + str(self.cas_ste[0][1]) + '$',
                     verticalalignment='center', fontsize=self.fontsize)

        # Excitation
        self.ax.arrow(self.excitation_arrow_x, self.initial_state_y, 0., 
                      self.excited_state_y-self.initial_state_y-self.arrow_head_length, width=0.01,
                      head_length=self.arrow_head_length,
                      head_width=self.arrow_head_width,
                      facecolor='blue', edgecolor='blue')
        self.ax.text(self.excitation_label_left_x,
                     0.5*(self.excited_state_y-self.initial_state_y)+self.initial_state_y,
                     str(self.cas_ste[0][0]),
                     verticalalignment='center', fontsize=self.fontsize)
        self.ax.text(self.delta_label_left_x,
                     0.5*(self.excited_state_y-self.initial_state_y)+self.initial_state_y,
                     self.del_lab[0],
                     verticalalignment='center', fontsize=self.fontsize, rotation=90)

        # Calculate position of states in decay cascade
        n_decay_steps = len(self.cas_ste)-1
        excitation_delta_y = self.excited_state_y - self.initial_state_y
        cascade_states_y = np.arange(1, n_decay_steps+1)

        if self.returns_to_initial_state:
            cascade_states_y = self.excited_state_y - cascade_states_y*excitation_delta_y/(n_decay_steps)
        else:
            cascade_states_y = self.excited_state_y - cascade_states_y*excitation_delta_y/(n_decay_steps+1)

        # States in cascade
        for i in range(n_decay_steps if not self.returns_to_initial_state else n_decay_steps-1):
            self.ax.plot([self.intermediate_state_x, self.intermediate_state_x + self.intermediate_state_width],
                         [cascade_states_y[i]]*2, color='black')            
            self.ax.text(self.state_label_right_x,
                         cascade_states_y[i], r'$' + str(self.cas_ste[i+1][1]) + '$',
                         verticalalignment='center', fontsize=self.fontsize)
            
        # First transition in cascade
        self.ax.plot([self.decay_arrow_x]*2, [self.excited_state_y, cascade_states_y[0] + self.arrow_head_length],
                  '--' if n_decay_steps > 1 else '-', color='red')
        self.ax.arrow(self.decay_arrow_x, cascade_states_y[0]+self.arrow_head_length,
                      0., -1.e-5*self.range_y, 
                      head_length=self.arrow_head_length,
                      head_width=self.arrow_head_width,
                      color='red')
        self.ax.text(self.decay_label_right_x,
                     0.5*(self.excited_state_y-cascade_states_y[0]) + cascade_states_y[0],
                     str(self.cas_ste[1][0]),
                     verticalalignment='center', fontsize=self.fontsize)
        self.ax.text(self.delta_label_right_x,
                     0.5*(self.excited_state_y-cascade_states_y[0]) + cascade_states_y[0],
                     self.del_lab[1],
                     verticalalignment='center', fontsize=self.fontsize, rotation=90)

        # Transitions in cascade
        for i in range(1, n_decay_steps):
            self.ax.plot([self.decay_arrow_x]*2, [cascade_states_y[i-1], cascade_states_y[i] + self.arrow_head_length],
                         '--' if i < n_decay_steps - 1 else '-', color='red')
            self.ax.arrow(self.decay_arrow_x, cascade_states_y[i]+self.arrow_head_length,
                      0., -1.e-5*self.range_y,
                      head_length=self.arrow_head_length,
                      head_width=self.arrow_head_width,
                      color='red')
            self.ax.text(self.decay_label_right_x,
                         0.5*(cascade_states_y[i-1]-cascade_states_y[i]) + cascade_states_y[i],
                         str(self.cas_ste[i][0]),
                         verticalalignment='center', fontsize=self.fontsize)