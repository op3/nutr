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

# Copyright (C) 2020, 2021 Udo Friman-Gayer

from pathlib import Path
import os
os.chdir('@ANGCORR_PYTHON_DIR@')
from time import time

from asymmetry_plot import AngularCorrelation, AsymmetryPlotter
import state as st
import transition as tr

t_start = time()

ang_cor = AngularCorrelation(
    st.State(3, st.POSITIVE),
    [
        [tr.Transition(tr.ELECTRIC, 4, tr.MAGNETIC, 6, 0.), st.State(7, st.POSITIVE)],
        [tr.Transition(tr.EM_UNKNOWN, 2, tr.EM_UNKNOWN, 4, 0.), st.State(5, st.PARITY_UNKNOWN)],
    ],
    ['delta_1', 'delta_2']
)

arctan_deltas, asy_45, asy_90 = ang_cor.asymmetry_grid(n_delta_steps=301)

asy_plo = AsymmetryPlotter(ang_cor, arctan_deltas, asy_45, asy_90, scale_asymmetries=True,
asy_45_exp=[-0.4, 0.1, 0.1],
asy_90_exp=[-0.5, 0.1, 0.1],
show_polarization=[True, False])
output_file_single_2d = Path('@PROJECT_BINARY_DIR@') / 'test_plot_04_mixing_inelastic_asy_2d.pdf'
asy_plo.plot_single_2d(r'$\delta_1$', [r'$\delta_1$', r'$\delta_2 = \delta_1$'], False, output_file_single_2d)

output_file_single_3d = Path('@PROJECT_BINARY_DIR@') / 'test_plot_04_mixing_inelastic_asy_3d.pdf'
asy_plo.plot_single_3d(r'$\delta_1$', output_file_single_3d)

output_file_contour = Path('@PROJECT_BINARY_DIR@') / 'test_plot_04_mixing_inelastic_asy_contour.pdf'
asy_plo.plot_double_contour([r'$\delta_1$', r'$\delta_2$'], output_file_contour)

output_file_contour_inverse = Path('@PROJECT_BINARY_DIR@') / 'test_plot_04_mixing_inelastic_asy_contour_inv.pdf'
asy_plo.plot_double_contour_inverse([r'$\delta_1$', r'$\delta_2$'], output_file_contour_inverse, returns_to_initial_state=False)

print('Created output files\n\'{}\',\n\'{}\',\n\'{}\',\nand \'{}\'.\nExecution took {:4.2f} seconds.'.format(output_file_single_2d, output_file_single_3d, output_file_contour, output_file_contour_inverse, time() - t_start))