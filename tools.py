"""
The purpose of this file is to create the tools and function needed to manage mods
"""

from dataclasses import dataclass
from enum import Enum
import sqlite3

""" Enum of the different mod shapes """


class Shape(Enum):
    SQUARE = 1
    ARROW = 2
    RHOMBUS = 3
    TRIANGLE = 4
    CIRCLE = 5
    CROSS = 6


""" Enum of the different mod sets """


class Set(Enum):
    HP = 1
    DEF = 2
    CD = 3
    CC = 4
    TEN = 5
    OFF = 6
    POT = 7
    SPEED = 8


""" Enum of the different mod primaries stats """


class Primaries(Enum):
    ACC = 1
    CA = 2
    CC = 3
    CD = 4
    DEF = 5
    HP = 6
    OFF = 7
    POT = 8
    PROT = 9
    SPEED = 10
    TEN = 11


""" Enum of the different mod secondaries stats """


class Secondaries(Enum):
    CC = 1
    DEFF = 2  # def+
    DEF = 3  # def%
    HPF = 4  # health+
    HP = 5  # health%
    OFFF = 6  # off+
    OFF = 7  # off%
    POT = 8
    PROTF = 9  # prot+
    PROT = 10  # prot%
    SPEED = 11
    TEN = 12


""" 
Class Mod 
"""


@dataclass
class Mod:
    shape: Shape
    set: Set
    prim: Primaries
    secon: list[Secondaries]


""" 
Class Potential Mod 
ex : [CC,CD] [off,speed,def,CD,prot,pot] [ten,speed,pot,off,off]
"""


@dataclass
class PotentialMod:
    _characterName: str
    _potentialMods: list[Mod]

    """




    TODO : trouver un moyen de construire les mods et de valider le fait qu'ils ont été trouvés





    """

    def __init__(self, name, set, primaries, secondaries):
        self._characterName = name
        print(set)
        print(primaries)
        print(secondaries)

    def toString(self):
        print(self._characterName, end=" : ")
        print(self._potentialMods)

    """
    Compare the mod entered by the user to his wanted mod list
    """

    def equalToMod(self, mod):
        print(self._potentialMods)


"""
Open the SWGOHCharacters file containing the list of all the characters along their mods
"""


def openModsFile():
    with open("SWGOHCharacters.tsv", "r") as f:
        potentialMods = []
        # saute les deux premières lignes
        lines = f.readlines()[2:]
        for line in lines:
            currentLine = line.split("\t")
            potentialMods.append(PotentialMod(currentLine[0], currentLine[3].split(","), currentLine[4].split(","),
                                              currentLine[5].split(",")))
            # potentialMods[len(potentialMods)-1].toString()
    return potentialMods


"""
Search for the wanted mod in the potentialMods list
"""


def comparePotentialWanted(potentialMods, wantedMod):
    resList = []
    for mod in potentialMods:
        if mod.equalToMod(wantedMod) != None:
            resList.append(mod.equalToMod(wantedMod))
    return resList


"""
Ask the user for the mod he have

TODO : Filtrer les statistiques possibles en fonction de la forme et la statistique primaire
"""


def askingForMod():
    nbSecondaries = 0
    secondaries = []
    correctSetValues = [set.name for set in Set]
    correctShapeValues = [shape.name for shape in Shape]
    correctPrimariesValues = [secondary.name for secondary in Primaries]
    correctSecondariesValues = [primary.name for primary in Secondaries]

    print("Please enter enter the mod you have.")

    print("First enter the mod Set : " + str(correctSetValues))
    setAsked = input().upper()
    while not setAsked in correctSetValues:
        print("You entered " + setAsked + " but the Set value must be one of those : " + str(correctSetValues))
        setAsked = input().upper()

    print("Then enter the mod Shape : " + str(correctShapeValues))
    shapeAsked = input().upper()
    while not shapeAsked in correctShapeValues:
        print("You entered " + shapeAsked + " but the Shape value must be one of those : " + str(correctShapeValues))
        shapeAsked = input().upper()

    print("Then enter the mod Primary : " + str(correctPrimariesValues))
    primaryAsked = input().upper()
    while not primaryAsked in correctPrimariesValues:
        print("You entered " + primaryAsked + " but the Primary value must be one of those : " + str(
            correctPrimariesValues))
        primaryAsked = input().upper()

    print("Finally enter the mod four Secondaries : ")
    while nbSecondaries < 4:
        print("The " + str(nbSecondaries + 1) + "th secondary among this list: " + str(correctSecondariesValues))
        secondaryAsked = input().upper()
        while not (secondaryAsked in correctSecondariesValues) or secondaryAsked in secondaries:
            print("You entered " + secondaryAsked + " but the Set value must be one of those and unique : " + str(
                correctSecondariesValues))
            secondaryAsked = input().upper()
        nbSecondaries += 1
        secondaries.append(secondaryAsked)

    return Mod(shapeAsked, setAsked, primaryAsked, secondaries)


def askForAction(resList):
    print(resList)
    return