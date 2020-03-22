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

    Copyright (C) 2020 Udo Friman-Gayer
*/

#include "ActionInitialization.hh"
#include "EventAction.hh"
#include "TupleManager.hh"
#include "PrimaryGeneratorAction.hh"
#include "RunAction.hh"

ActionInitialization::ActionInitialization()
 : G4VUserActionInitialization()
{}

ActionInitialization::~ActionInitialization()
{}

void ActionInitialization::BuildForMaster() const
{
	TupleManager *tuple = new TupleManager();

	SetUserAction(new RunAction(tuple));
}

void ActionInitialization::Build() const
{
	TupleManager *tuple = new TupleManager();

	SetUserAction(new PrimaryGeneratorAction);
	SetUserAction(new RunAction(tuple));
	SetUserAction(new EventAction(tuple));
}