#include "RadiatorTarget.hh"

#include <iostream>
#include <sstream>

#include "G4Box.hh"
#include "G4Tubs.hh"
#include "G4SubtractionSolid.hh"
#include "G4PVPlacement.hh"

#include "G4Color.hh"
#include "G4VisAttributes.hh"
#include "G4NistManager.hh"
#include "G4SystemOfUnits.hh"
#include "G4PhysicalConstants.hh"

using std::cout;
using std::endl;
using std::stringstream;

RadiatorTarget::RadiatorTarget(G4LogicalVolume *World_Log):World_Logical(World_Log){}

void RadiatorTarget::Construct(G4ThreeVector global_coordinates,G4String target_name, G4String target_material,G4double target_thickness,G4String attenuator_material,G4double attenuator_thickness)
{
	G4double target_z = target_thickness;

	G4Colour  white   (1.0, 1.0, 1.0) ;
	G4Colour  grey    (0.5, 0.5, 0.5) ;
	G4Colour  black   (0.0, 0.0, 0.0) ;
	G4Colour  red     (1.0, 0.0, 0.0) ;
	G4Colour  green   (0.0, 1.0, 0.0) ;
	G4Colour  blue    (0.0, 0.0, 1.0) ;
	G4Colour  cyan    (0.0, 1.0, 1.0) ;
	G4Colour  magenta (1.0, 0.0, 1.0) ;
	G4Colour  yellow  (1.0, 1.0, 0.0) ;
	G4Colour  orange (1.0, 0.5, 0.0) ;
	G4Colour  light_blue  (1.0, 0.82, 0.36) ;

	G4NistManager* man = G4NistManager::Instance();

	G4Material* Cu = man->FindOrBuildMaterial("G4_Cu");

	radiator_Mother_x = 70.*mm;
	radiator_Mother_y = 200.*mm;
	
	// Some dimensions needed to calculate the size of the mother volume
	G4double radiator_Cover_Window_Small_z = 2.*mm;
	G4double radiator_Cover_Window_Medium_z = 3.*mm;
	G4double radiator_Cover_Window_Large_z = 5.*mm;

	G4double radiator_Cover_z=0.;

	if(target_material == "Cu"){
		radiator_Mother_z = 10.*mm + target_z; 
		radiator_Cover_z = target_z;
	}
	else {
		if(target_z < 1.*mm){
			radiator_Mother_z = 10.*mm + radiator_Cover_Window_Small_z; 
			radiator_Cover_z = radiator_Cover_Window_Small_z;
		}
		if(target_z >= 1.*mm && target_z < 2.*mm){
			radiator_Mother_z = 10.*mm + radiator_Cover_Window_Medium_z; 
			radiator_Cover_z = radiator_Cover_Window_Medium_z;
		}
		if(target_z >= 2.*mm && target_z < 4.*mm){
			radiator_Mother_z = 10.*mm + radiator_Cover_Window_Large_z; 
			radiator_Cover_z = radiator_Cover_Window_Large_z;
		}
		if(target_z > 4.*mm){
			cout << "Error: __FILE__:__LINE__ RadiatorTarget(): No available target holder for a target with a thickness of " << target_z << " mm. Aborting ..." << endl;
			abort();
		}
	}

	//*************************************************
	// Radiator target holder:
	// A frame with an integrated water pipe
	//*************************************************

	G4double radiator_Holder_x = 70.*mm;
	G4double radiator_Holder_y = 50.*mm;
	G4double radiator_Holder_z = 10.*mm;

	// Gives the position of the center of the target relative to the center of the mother volume. Can be used for positioning in the DetectorConstruction
	radiator_Window_Position = (radiator_Mother_y - radiator_Holder_y)*0.5;

	//*************************************************
	// Cover for target holder and/or target (in case of a Cu target, the cover is the target)
	//*************************************************
	
	G4double radiator_Cover_x = 70.*mm;
	G4double radiator_Cover_y = 50.*mm;

	G4double window_Small_x = 26.*mm;
	G4double window_Small_y = 26.*mm;
	G4double window_Small_z = 1.*mm;

	G4double window_Large_x = 30.*mm;
	G4double window_Large_y = 30.*mm;

	if (target_z > 0.) {
		if(target_material == "Cu"){
			radiator_Cover_z = target_z;	

			G4Box *target_Solid = new G4Box("target_Solid", radiator_Cover_x*0.5, radiator_Cover_y*0.5, radiator_Cover_z*0.5);

			G4LogicalVolume *target_Logical = new G4LogicalVolume(target_Solid, Cu, target_name);
			target_Logical->SetVisAttributes(orange);

			new G4PVPlacement(0, global_coordinates + G4ThreeVector(0,radiator_Window_Position,0) +G4ThreeVector(0., -radiator_Mother_y*0.5 + radiator_Holder_y*0.5, -radiator_Mother_z*0.5 + radiator_Cover_z*0.5), target_Logical, target_name, World_Logical, false, 0);

		}
		else{

			G4Box *radiator_Cover_Block_Solid = new G4Box("radiator_Cover_Block_Solid", radiator_Cover_x*0.5, radiator_Cover_y*0.5, radiator_Cover_z*0.5);

			G4Box *radiator_Cover_Window_Small_Solid = new G4Box("radiator_Cover_Window_Small_Solid", window_Small_x*0.5, window_Small_y*0.5, window_Small_z*0.6);

			G4Box *radiator_Cover_Window_Large_Solid = new G4Box("radiator_Cover_Window_Large_Solid", window_Large_x*0.5, window_Large_y*0.5, (radiator_Cover_z - window_Small_z)*0.5);

			G4SubtractionSolid* radiator_Cover1 = new G4SubtractionSolid("radiator_Cover1", radiator_Cover_Block_Solid, radiator_Cover_Window_Small_Solid, 0, G4ThreeVector(0., 0., -0.5*(radiator_Cover_z - window_Small_z)));

			G4SubtractionSolid* radiator_Cover2 = new G4SubtractionSolid("radiator_Cover2", radiator_Cover1, radiator_Cover_Window_Large_Solid, 0, G4ThreeVector(0., 0., -0.5*(-radiator_Cover_z + (radiator_Cover_z - window_Small_z))));

			G4LogicalVolume* radiator_Cover_Logical = new G4LogicalVolume(radiator_Cover2, Cu, "radiator_Cover_Logical");
			radiator_Cover_Logical->SetVisAttributes(orange);

			new G4PVPlacement(0, global_coordinates + G4ThreeVector(0,radiator_Window_Position,0) +G4ThreeVector(0., -radiator_Mother_y*0.5 + radiator_Holder_y*0.5, -0.5*radiator_Mother_z + radiator_Cover_z*0.5), radiator_Cover_Logical, "radiator_Cover", World_Logical, false, 0);

			stringstream target_material_database_name;
			target_material_database_name << "G4_" << target_material;

			G4Material *targetMaterial = man->FindOrBuildMaterial(target_material_database_name.str());

			G4Box *target_Solid = new G4Box("target_Solid", window_Large_x*0.5, window_Large_y*0.5, target_z*0.5);

			G4LogicalVolume *target_Logical = new G4LogicalVolume(target_Solid, targetMaterial, target_name);
			target_Logical->SetVisAttributes(yellow);

			new G4PVPlacement(0, global_coordinates + G4ThreeVector(0,radiator_Window_Position,0) +G4ThreeVector(0., -radiator_Mother_y*0.5 + radiator_Holder_y*0.5, -0.5*radiator_Mother_z + radiator_Cover_z*0.5 + window_Small_z*0.5), target_Logical, target_name, World_Logical, false, 0);
		}
	}

	if(attenuator_thickness > 0.){
		stringstream attenuator_material_database_name;
		attenuator_material_database_name << "G4_" << attenuator_material;

		G4Material *attenuatorMaterial = man->FindOrBuildMaterial(attenuator_material_database_name.str());

		G4Box *attenuator_Solid = new G4Box("attenuator_Solid", radiator_Holder_x*0.5, radiator_Holder_y*0.5, attenuator_thickness*0.5);

		G4LogicalVolume *attenuator_Logical = new G4LogicalVolume(attenuator_Solid, attenuatorMaterial, "attenuator_Logical");
		attenuator_Logical->SetVisAttributes(grey);

		new G4PVPlacement(0, global_coordinates + G4ThreeVector(0,radiator_Window_Position,0) +G4ThreeVector(0., -radiator_Mother_y*0.5 + radiator_Holder_y*0.5, -0.5*radiator_Mother_z + radiator_Holder_z + radiator_Cover_z + attenuator_thickness*0.5), attenuator_Logical, "Attenuator", World_Logical, false, 0);
	}
}
