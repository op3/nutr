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
#    Copyright (C) 2021 Oliver Papst

find_package(Geant4 REQUIRED)
link_libraries(${Geant4_LIBRARIES})
include(${Geant4_USE_FILE})

set(SENSITIVE_DETECTOR_DIR flux CACHE STRING "Required to be flux" FORCE)

add_library(detectorConstruction DetectorConstruction.cc Collimator.cc RadiatorTarget.cc)
set_property(TARGET detectorConstruction PROPERTY CXX_STANDARD 14)
target_include_directories(detectorConstruction PUBLIC ${PROJECT_SOURCE_DIR}/include/detectors ${PROJECT_SOURCE_DIR}/include/geometry ${PROJECT_SOURCE_DIR}/include/geometry/bremsstrahlung ${PROJECT_SOURCE_DIR}/include/sensitive_detector/${SENSITIVE_DETECTOR_DIR})
target_link_libraries(detectorConstruction nDetectorConstruction SensitiveDetector)
target_compile_options(detectorConstruction PUBLIC -Wall -Wextra)