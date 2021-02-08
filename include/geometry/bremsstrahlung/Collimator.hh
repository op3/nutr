/*
    This file is part of nutr.

    nutr is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    nutr is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with nutr.  If not, see <https://www.gnu.org/licenses/>.

    Copyright (C) 2021 Oliver Papst
*/

#pragma once

#include <vector>
#include <array>

#include "G4LogicalVolume.hh"

using std::vector;
using std::array;

class Collimator
{
public:
    Collimator(G4LogicalVolume *World_Logical, const G4String a_name, const G4String a_material, G4double a_width, G4double a_height) : world_logical(World_Logical), name(a_name), collimator_material(a_material), width(a_width), height(a_height) {};

    void addBlock(G4double depth, G4double hole_radius);
    void Construct(G4ThreeVector global_coordinates, G4double dist_from_center);
private:
    G4LogicalVolume *world_logical; /**< Logical volume in which the detector will be placed. */
    const G4String name;            /**< Name of the collimator. This name will be used as a prefix for all parts of the collimator. */

    G4String collimator_material; /**< Collimator material given as G4Material name. */
    G4double width;
    G4double height;
    vector<G4double> depths;
    vector<G4double> hole_radii;
};