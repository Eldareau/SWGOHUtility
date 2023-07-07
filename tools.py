"""
The purpose of this file is to create the tools and function needed to manage mods
"""

from dataclasses import dataclass
import collections
import modConst

""" 
Class Mod 
"""
@dataclass
class Mod:
    def __init__(self, set, shape, primary, secondaries):
        if len(secondaries) == 4:
            self.set = set
            self.shape = shape
            self.primary = primary
            self.secondaries = secondaries
        else:
            print("The mod you are trying to build has too much or not enough secondary stats (need 4, " + len(secondaries) + " provided)")

    def getMod(self):
        return [self.set, self.shape, self.primary, self.secondaries]
    
    def setMod(self, set, shape, primary, secondaries):
        if len(secondaries) == 4:
            self.set = set
            self.shape = shape
            self.primary = primary
            self.secondaries = secondaries
        else:
            print("The mod you are trying to build has too much or not enough secondary stats (need 4, " + len(secondaries) + " provided)")

def secondaryValid(secondary, primary, secondaries):
    return(not (secondary in modConst.potentialSecondary) or secondary in secondaries or secondary == primary)

"""
Ask the user for the mod he have

TODO : Filtrer les statistiques possibles en fonction de la forme et la statistique primaire
"""
def askingForMod():
    nbSecondaries = 0
    secondaries = []

    print("Please enter enter the mod you have.")

    print("First enter the mod Set : " + str(modConst.potentialSet))
    setAsked = input().lower()
    while not setAsked in modConst.potentialSet:
        print("You entered " + setAsked + " but the Set value must be one of those : " + str(modConst.potentialSet))
        setAsked = input().lower()

    print("Then enter the mod Shape : " + str(modConst.potentialShape))
    shapeAsked = input().lower()
    while not shapeAsked in modConst.potentialShape:
        print("You entered " + shapeAsked + " but the Shape value must be one of those : " + str(modConst.potentialShape))
        shapeAsked = input().lower()

    correctPrimariesValues = modConst.potentialPrimary[modConst.potentialShape.index(shapeAsked)]

    print("Then enter the mod Primary : " + str(correctPrimariesValues))
    primaryAsked = input().lower()
    while not primaryAsked in correctPrimariesValues:
        print("You entered " + primaryAsked + " but the Primary value must be one of those : " + str(
            correctPrimariesValues))
        primaryAsked = input().lower()

    print("Finally enter the mod four Secondaries : ")
    while nbSecondaries < 4:
        print("The " + str(nbSecondaries + 1) + "th secondary among this list: " + str(modConst.potentialSecondary))
        secondaryAsked = input().lower()
        while secondaryValid(secondaryAsked, primaryAsked, secondaries):
            print("You entered " + secondaryAsked + " but the Set value must be one of those and unique : " + str(
                modConst.potentialSecondary))
            secondaryAsked = input().lower()
        nbSecondaries += 1
        secondaries.append(secondaryAsked)

    return Mod(setAsked, shapeAsked, primaryAsked, secondaries)

def askForAction(resList):
    print(resList)
    return

"""
Give the duplicates elements and their position in list.
IN : List
OUT : Dict
"""
def list_duplicates(seq):
    tally = collections.defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)

"""
Sort the given secondaries array with enum order
"""
def sort_secondaries(secondaries):
    order = {v:i for i,v in enumerate(modConst.potentialSecondary)}
    res = sorted(secondaries, key=lambda x: order[x])
    return res
