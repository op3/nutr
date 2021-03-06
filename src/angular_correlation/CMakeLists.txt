#    This file is part of nutr.
#
#    nutr is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    nutr is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with nutr.  If not, see <https://www.gnu.org/licenses/>.
#
#    Copyright (C) 2020, 2021 Udo Friman-Gayer

find_package(GSL REQUIRED)
include_directories(${GSL_INCLUDE_DIRS})

find_package(Geant4 REQUIRED)
link_libraries(${Geant4_LIBRARIES})
include(${Geant4_USE_FILE})

include_directories(${PROJECT_SOURCE_DIR}/include/angular_correlation/)

add_library(fCoefficient FCoefficient.cc)
target_link_libraries(fCoefficient ${GSL_LIBRARIES})
target_compile_options(fCoefficient PUBLIC -Wall -Wextra)

add_library(avCoefficient AvCoefficient.cc)
target_link_libraries(avCoefficient fCoefficient)
target_compile_options(avCoefficient PUBLIC -Wall -Wextra)

add_library(w_gamma_gamma W_gamma_gamma.cc)
target_compile_options(w_gamma_gamma PUBLIC -Wall -Wextra)

add_library(w_dir_dir W_dir_dir.cc)
target_link_libraries(w_dir_dir avCoefficient uvCoefficient)
target_compile_options(w_dir_dir PUBLIC -Wall -Wextra -fPIC)

add_library(kappa_coefficient KappaCoefficient.cc)
target_link_libraries(kappa_coefficient ${GSL_LIBRARIES})
target_compile_options(kappa_coefficient PUBLIC -Wall -Wextra -fPIC)

add_library(alphavCoefficient AlphavCoefficient.cc)
target_link_libraries(alphavCoefficient fCoefficient kappa_coefficient)
target_compile_options(alphavCoefficient PUBLIC -Wall -Wextra)

add_library(evCoefficient EvCoefficient.cc)
target_link_libraries(evCoefficient fCoefficient)
target_compile_options(evCoefficient PUBLIC -Wall -Wextra)

add_library(uvCoefficient UvCoefficient.cc)
target_link_libraries(uvCoefficient ${GSL_LIBRARIES})
target_compile_options(uvCoefficient PUBLIC -Wall -Wextra)

add_library(w_pol_dir W_pol_dir.cc)
target_link_libraries(w_pol_dir alphavCoefficient avCoefficient w_dir_dir)
target_compile_options(w_pol_dir PUBLIC -Wall -Wextra)

add_library(angular_correlation SHARED AngularCorrelation.cc)
target_link_libraries(angular_correlation euler_angle_rotation w_dir_dir w_pol_dir)
target_compile_options(angular_correlation PUBLIC -Wall -Wextra)
configure_file(python/angular_correlation.py python/angular_correlation.py @ONLY)
configure_file(python/state.py python/state.py)
configure_file(python/transition.py python/transition.py)

add_library(euler_angle_rotation EulerAngleRotation.cc)
target_compile_options(euler_angle_rotation PUBLIC -Wall -Wextra)

add_library(spherePointSampler SpherePointSampler.cc)
target_link_libraries(spherePointSampler ${GSL_LIBRARIES})
target_compile_options(spherePointSampler PUBLIC -Wall -Wextra)

add_library(sphereIntegrator SphereIntegrator.cc)
target_link_libraries(sphereIntegrator spherePointSampler)
target_compile_options(sphereIntegrator PUBLIC -Wall -Wextra)

add_library(sphereRejectionSampler SphereRejectionSampler.cc)
target_compile_options(sphereIntegrator PUBLIC -Wall -Wextra)

add_library(angcorrRejectionSampler AngCorrRejectionSampler.cc)
target_link_libraries(angcorrRejectionSampler sphereRejectionSampler w_gamma_gamma)
target_compile_options(angcorrRejectionSampler PUBLIC -Wall -Wextra)

enable_testing()
add_executable(test_f_coefficient test_f_coefficient.cc)
target_link_libraries(test_f_coefficient fCoefficient)
add_test(test_f_coefficient test_f_coefficient)

add_executable(test_uv_coefficient test_Uv_coefficient.cc)
target_link_libraries(test_uv_coefficient uvCoefficient)
add_test(test_uv_coefficient test_uv_coefficient)

add_executable(test_w_dir_dir test_w_dir_dir.cc)
target_link_libraries(test_w_dir_dir w_dir_dir)
add_test(test_w_dir_dir test_w_dir_dir)

add_executable(test_kappa_coefficient test_kappa_coefficient.cc)
target_link_libraries(test_kappa_coefficient kappa_coefficient)
add_test(test_kappa_coefficient test_kappa_coefficient)

add_executable(test_ev_coefficient test_Ev_coefficient.cc)
target_link_libraries(test_ev_coefficient alphavCoefficient evCoefficient)
add_test(test_ev_coefficient test_ev_coefficient)

add_executable(test_w_pol_dir test_w_pol_dir.cc)
target_link_libraries(test_w_pol_dir w_pol_dir ${GSL_LIBRARIES})
add_test(test_w_pol_dir test_w_pol_dir)

add_executable(test_unobserved test_unobserved.cc)
target_link_libraries(test_unobserved w_dir_dir ${GSL_LIBRARIES})
add_test(test_unobserved test_unobserved)

add_executable(test_euler_angle_rotation test_euler_angle_rotation.cc)
target_link_libraries(test_euler_angle_rotation euler_angle_rotation ${GSL_LIBRARIES})
add_test(test_euler_angle_rotation test_euler_angle_rotation)

add_executable(test_angular_correlation test_angular_correlation.cc)
target_link_libraries(test_angular_correlation angular_correlation w_dir_dir w_pol_dir ${GSL_LIBRARIES})
add_test(test_angular_correlation test_angular_correlation)

add_executable(test_angular_correlation_io test_angular_correlation_io.cc)
target_link_libraries(test_angular_correlation_io angular_correlation)
add_test(test_angular_correlation_io test_angular_correlation_io)

find_package(ROOT COMPONENTS RGL)
if(ROOT_FOUND)
    add_executable(test_plots_tgl test_plots_tgl.cc)
    target_link_libraries(test_plots_tgl w_pol_dir ROOT::Core ROOT::RGL)
    add_test(test_plots_tgl test_plots_tgl)

    add_executable(test_plots_tpolymarker3d test_plots_tpolymarker3d.cc)
    target_link_libraries(test_plots_tpolymarker3d w_pol_dir spherePointSampler ROOT::Core ROOT::RGL)
    add_test(test_plots_tpolymarker3d test_plots_tpolymarker3d)    
endif()

add_executable(test_elliptic_integral test_elliptic_integral.cc)
target_link_libraries(test_elliptic_integral spherePointSampler ${GSL_LIBRARIES})
add_test(test_elliptic_integral test_elliptic_integral)

add_executable(test_spiral_segment test_spiral_segment.cc)
target_link_libraries(test_spiral_segment spherePointSampler ${GSL_LIBRARIES})
add_test(test_spiral_segment test_spiral_segment)

add_executable(test_find_c test_find_c.cc)
target_link_libraries(test_find_c spherePointSampler)
add_test(test_find_c test_find_c)

add_executable(test_sphere_integrator test_sphere_integrator.cc)
target_link_libraries(test_sphere_integrator sphereIntegrator)
add_test(test_sphere_integrator test_sphere_integrator)

add_executable(test_normalization test_normalization.cc)
target_link_libraries(test_normalization sphereIntegrator w_dir_dir w_pol_dir)
add_test(test_normalization test_normalization)

add_executable(test_find_Theta_j test_find_Theta_j.cc)
target_link_libraries(test_find_Theta_j spherePointSampler)
add_test(test_find_Theta_j test_find_Theta_j)

add_executable(test_upper_limit test_upper_limit.cc)
target_link_libraries(test_upper_limit spherePointSampler w_dir_dir w_gamma_gamma w_pol_dir)

add_executable(test_sphere_rejection_sampler test_sphere_rejection_sampler.cc)
target_link_libraries(test_sphere_rejection_sampler sphereRejectionSampler w_dir_dir)

configure_file(python/angular_correlation_plot.py python/angular_correlation_plot.py)
configure_file(python/asymmetry_plot.py python/asymmetry_plot.py)
configure_file(python/level_scheme_plotter.py python/level_scheme_plotter.py)
configure_file(python/test_plots_mixing_single.py python/test_plots_mixing_single.py)
configure_file(python/test_plots_patterns.py python/test_plots_patterns.py)
configure_file(python/test_plots_mixing_double.py python/test_plots_mixing_double.py)
