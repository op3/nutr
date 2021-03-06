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

include_directories(${PROJECT_SOURCE_DIR}/include/sensitive_detector)
include_directories(${PROJECT_BINARY_DIR}/include/sensitive_detector)

find_package(Geant4 REQUIRED)
link_libraries(${Geant4_LIBRARIES})
include(${Geant4_USE_FILE})

configure_file(${PROJECT_SOURCE_DIR}/include/sensitive_detector/AnalysisManager.hh.in ${PROJECT_BINARY_DIR}/include/sensitive_detector/AnalysisManager.hh)
add_library(analysisManager AnalysisManager.cc)
target_compile_options(analysisManager PUBLIC -Wall -Wextra)

add_library(nDetectorHit NDetectorHit.cc)
target_compile_options(nDetectorHit PUBLIC -Wall -Wextra)

add_library(nRunAction NRunAction.cc)
target_compile_options(nRunAction PUBLIC -Wall -Wextra)

configure_file(${PROJECT_SOURCE_DIR}/include/sensitive_detector/NEventAction.hh.in ${PROJECT_BINARY_DIR}/include/sensitive_detector/NEventAction.hh)
add_library(nEventAction NEventAction.cc)
target_link_libraries(nEventAction nRunAction)
target_compile_options(nEventAction PUBLIC -Wall -Wextra)

add_library(nSensitiveDetector NSensitiveDetector.cc)
target_compile_options(nSensitiveDetector PUBLIC -Wall -Wextra)
