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

#include <memory>
#include <vector>

using std::make_unique;

#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4LogicalVolume.hh"
#include "G4NistManager.hh"
#include "G4PVPlacement.hh"
#include "G4SystemOfUnits.hh"
#include "G4VisAttributes.hh"

#include "DetectorConstruction.hh"
#include "Collimator.hh"
#include "RadiatorTarget.hh"

G4VPhysicalVolume *DetectorConstruction::Construct()
{
    G4NistManager *nist_manager = G4NistManager::Instance();

    auto *world_vis = new G4VisAttributes(true, G4Color::Red());
    world_vis->SetForceWireframe(true);

    const auto world_x = 12. * mm;
    const auto world_y = 12. * mm;
    const auto world_z = 5. * cm;

    world_solid = make_unique<G4Box>("world_solid", .5 * world_x, .5 * world_y, .5 * world_z);
    world_logical = make_unique<G4LogicalVolume>(world_solid.get(), nist_manager->FindOrBuildMaterial("G4_AIR"), "world_logical");
    world_logical->SetVisAttributes(world_vis);
    world_phys = make_unique<G4PVPlacement>(new G4RotationMatrix(), G4ThreeVector(), world_logical.get(), "world", nullptr, false, 0);

    //const G4int n_blocks = 10;
    //const G4double distcollimatortotarget = 162. * mm;
    //const G4double colholeradius_min = 6. * mm;
    //const G4double colholeradius_max = 10. * mm;
    //auto collimator = Collimator(world_logical.get(), "DHIPS_Collimator", "G4_Cu", world_x, world_y);
    //for (int i = 0; i < n_blocks; ++i)
    //{
    //    collimator.addBlock(
    //        95. * mm,
    //        colholeradius_max - i * (colholeradius_max - colholeradius_min) / (n_blocks - 1));
    //}
    //collimator.Construct(G4ThreeVector(), distcollimatortotarget - 0.5 * world_z);

    RadiatorTarget RadiatorTarget(world_logical.get());
    RadiatorTarget.Construct(G4ThreeVector(0, 0, -0.5 * world_z + 15. * mm), "Radiator1", "Au", 2.5 * mm, "Al", 0.); // Position guesstimated
    //RadiatorTarget.Construct(G4ThreeVector(0, 0, -1130. * mm + 0.5 * world_z), "Radiator2", "Au", 0., "Al", 0.);       // Position guesstimated

    // TODO: Everything here was guessed
    //const auto exit_window_distance = -150. * mm;
    //const auto exit_window_thickness = 0.01 * mm;
    //const auto sdalinac_length = 5. * cm;
    //const auto sdalinac_radius = 14. * mm;
    //auto sdalinac_vacuum = new G4Tubs(
    //    "sdalinac_vacuum_solid", 0. * mm, sdalinac_radius, .5 * sdalinac_length, 0. * deg, 360. * deg);
    //auto sdalinac_cap = new G4Tubs(
    //    "sdalinac_cap_solid", 0. * mm, sdalinac_radius, .5 * exit_window_thickness, 0. * deg, 360. * deg);
    //auto sdalinac_vacuum_logical = new G4LogicalVolume(
    //    sdalinac_vacuum, nist_manager->FindOrBuildMaterial("G4_Galactic"), "target_logical");
    //auto sdalinac_cap_logical = new G4LogicalVolume(
    //    sdalinac_cap, nist_manager->FindOrBuildMaterial("G4_Al"), "target_logical");
    //sdalinac_vacuum_logical->SetVisAttributes(G4Color::Cyan());
    //sdalinac_cap_logical->SetVisAttributes(G4Color::Gray());
    //new G4PVPlacement(
    //    new G4RotationMatrix(),
    //    G4ThreeVector(0., 0., exit_window_distance - .5 * sdalinac_length + 0.5 * world_z),
    //    sdalinac_vacuum_logical, "sdalinac_vacuum", world_logical.get(), false, 0);
    //new G4PVPlacement(
    //    new G4RotationMatrix(),
    //    G4ThreeVector(0., 0., exit_window_distance + .5 * exit_window_thickness + 0.5 * world_z),
    //    sdalinac_cap_logical, "sdalinac_cap", world_logical.get(), false, 0);

    const auto target_radius = 5. * mm;
    auto target = new G4Tubs(
        "NRF_target_solid", 0. * mm, target_radius, .5 * mm, 0. * deg, 360. * deg);
    auto target_logical = new G4LogicalVolume(
        target, nist_manager->FindOrBuildMaterial("G4_AIR"), "NRF_target_logical");
    target_logical->SetVisAttributes(G4Color::Red());
    new G4PVPlacement(new G4RotationMatrix(), G4ThreeVector(0, 0, .5 * world_z - .5 * mm), target_logical, "NRF_target", world_logical.get(), false, 0);

    std::vector<G4LogicalVolume *> sensitive_volumes{target_logical};
    RegisterSensitiveLogicalVolumes(sensitive_volumes);

    return world_phys.get();
}