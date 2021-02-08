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

#include "G4NistManager.hh"
#include "G4Color.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4Box.hh"
#include "G4SubtractionSolid.hh"
#include "G4Tubs.hh"
#include "G4VisAttributes.hh"

#include <Collimator.hh>

void Collimator::addBlock(G4double depth, G4double hole_radius)
{
    depths.emplace_back(depth);
    hole_radii.emplace_back(hole_radius);
}

void Collimator::Construct(G4ThreeVector global_coordinates, G4double dist_from_center)
{
    auto nist = G4NistManager::Instance();
    auto material = nist->FindOrBuildMaterial(collimator_material);
    auto light_orange = G4Colour(1.0, 0.82, 0.36);

    for (size_t i = 0; i < depths.size(); ++i) {
        auto depth = depths[i];
        auto hole_radius = hole_radii[i];
        auto slice_name = (name + "_Slice" + std::to_string(i));

        auto block = new G4Box((slice_name + "_Block_Solid").c_str(), .5 * width, .5 * height, .5 * depth);
        auto hole = new G4Tubs((slice_name + "_Hole_Solid").c_str(), 0. * mm, hole_radius, depth, 0. * deg, 360. * deg);
        auto slice = new G4SubtractionSolid((slice_name + "_Solid").c_str(), block, hole);

        auto slice_logical = new G4LogicalVolume(
            slice,
            material,
            (slice_name + "_Logical").c_str(),
            0, 0, 0);
        slice_logical->SetVisAttributes(light_orange);
        
        new G4PVPlacement(
            0,
            global_coordinates + G4ThreeVector(0., 0., -(dist_from_center + .5 * depth)),
            slice_logical,
            slice_name.c_str(),
            world_logical, 0, 0
        );

        dist_from_center += depth;
    }
}