from dataclasses import dataclass
from enum import Enum

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
    DEFF = 2 # def+
    DEF = 3 # def%
    HPF = 4 # health+
    HP = 5 # health%
    OFFF = 6 # off+
    OFF = 7 # off%
    POT = 8
    PROTF = 9 # prot+
    PROT = 10 # prot%
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
    secon: Secondaries

""" 
Class Potential Mod 
ex : [CC,CD] [off,speed,def,CD,prot,pot] [ten,speed,pot,off,off]
"""
@dataclass
class PotentialMod:
    _characterName: str
    _potentialSet: [Set]
    _potentialPrimaries: [[Primaries, Shape]]
    _potentialSecondaries: [Secondaries]

    def __init__(self, name, set, primaries, secondaries):
        self._characterName = name
        self._potentialSet = set
        self._potentialPrimaries = []
        if len(primaries) > 1:
            for i in range(len(primaries)):
                self._potentialPrimaries.append([primaries[i], Shape(i + 1).name])
        self._potentialSecondaries = secondaries

    def toString(self):
        print(self._characterName, end=" : ")
        print(self._potentialSet, end=", ")
        print(self._potentialPrimaries, end=", ")
        print(self._potentialSecondaries)

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
            potentialMods.append(PotentialMod(currentLine[0], currentLine[3].split(","), currentLine[4].split(","), currentLine[5].split(",")))
            #potentialMods[len(potentialMods)-1].toString()
    return potentialMods

def comparePotentialWanted():
    # TODO
    return

def askingForMod():
    # TODO
    return

def askForAction():
    # TODO
    return