"""
The purpose of this file is to create the tools and function needed to manage mods
"""

from dataclasses import dataclass
import collections
import constants
import sqlite3
import integrity
from itertools import combinations

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
            print("The mod you are trying to build has too much or not enough secondary stats (need 4, " + str(len(secondaries)) + " provided)")

    @classmethod
    def getMod(self):
        return [self.set, self.shape, self.primary, self.secondaries]
    
    @classmethod
    def setMod(self, set, shape, primary, secondaries):
        if len(secondaries) == 4:
            self.set = set
            self.shape = shape
            self.primary = primary
            self.secondaries = secondaries
        else:
            print("The mod you are trying to build has too much or not enough secondary stats (need 4, " + str(len(secondaries)) + " provided)")
    
    # @classmethod
    # def __str__(self):
    #     return "set : " + self.set + " /n shape : " + self.shape + " /n primary : " + self.primary + " /n secondaries : " + self.getMod()

"""
Check validity of selected secondary
"""
def secondaryNotValid(secondary, primary, secondaries):
    return(not (secondary in constants.potentialSecondary) or secondary in secondaries or secondary == primary)

"""
Create a list of four unique secondaries from potentialSecondary list excluding current primary stat
"""
def groupOfFourSecondaries(primary):
    secondaries = constants.potentialSecondary[:]
    if primary in secondaries:
        secondaries.remove(str(primary))
    return list(combinations(secondaries, 4))

"""
Return the a list of mod sets sort by number of appearance
"""
def mostWantedSet():
    con = sqlite3.connect(constants.dataBaseName)
    cur = con.cursor()
    cur.execute("SELECT Sets, COUNT(*) FROM mods GROUP BY Sets ORDER BY COUNT(*) DESC;")
    mod_id = cur.fetchall()
    print(mod_id)

"""
Add new character to database
"""
def addCharacterToDB():
    con = sqlite3.connect(constants.dataBaseName)
    cur = con.cursor()
    cur.execute("INSERT INTO secondaries (Name) VALUES ('criticalchance%');")
    con.commit()
    con.close()
    return 0

"""
Give the duplicates elements and their position in list.
IN : List
OUT : Dict
"""
def list_duplicates(seq, ignore=None):
    tally = collections.defaultdict(list)
    for i,item in enumerate(seq):
        if item != ignore:
            tally[item].append(i)
    return list((key,locs) for key,locs in tally.items() if len(locs)>1)

"""
Sort the given secondaries array with enum order
"""
def sort_secondaries(secondaries):
    order = {v:i for i,v in enumerate(constants.potentialSecondary)}
    res = sorted(secondaries, key=lambda x: order[x])
    return res

"""
Return if the given input is a valid input or not
"""
def not_a_valid_number(value, threshold):
    try:
        value = int(value)
    except ValueError:
        return False
    return (value <= 0 and value >= threshold)

"""
Remove duplicate from list
IN: List
OUT: List
EX:
removeDuplicateFromList([[1, 2], [4], [5, 6, 2], [1, 2], [3], [4]]) = [[1, 2], [3], [4], [5, 6, 2]]
"""
def removeDuplicateFromList(list):
    noDuplicate = []
    for i in list:
        if i not in noDuplicate:
            noDuplicate.append(i)
    return noDuplicate

"""
Search strings from list to another list
IN : List, List
OUT : BOOLEAN
EX: 
checkFromListToList([abc, def, ghi], [abd-156, abc-198, def-186, dgd-123]) = TRUE
checkFromListToList([abc, def, ghi], [abd-156, aba-198, ghi-186, dgd-123]) = TRUE
checkFromListToList([abc, def, ghi], [abd-156, ajc-198, dea-186, dgd-123]) = FALSE
"""
def checkFromListToList(toLookFor, toLookIn):
    return any(ext in toLookFor for ext in toLookIn)

"""
Return sets value (/!\ At this point we already verified all set from sets are in potentialSet)
IN : List
OUT : INT
EX:
computeSetValue(["criticaldamage","criticalchance"]) = 6 (GOOD)
computeSetValue(["defense","criticalchance","potency"]) = 6 (GOOD)
computeSetValue(["speed","criticaldamage"]) = 8 (BAD)
"""
def computeSetValue(sets):
    res = 0
    for set in sets:
        if set in constants.largeSets:
            res += 4
        else:
            res += 2
    return res

"""
Return all possible mods from given informations
IN: List, List, List
Out: List[List]
EX: 		
createModsFromLine(["speed","health"], ["offense%","speed","defense%","protection%","protection%","potency%"], ["potency%","speed","protection%","health%","offense%"]) 
= [["speed","square","offense%",["potency%","speed","protection%","health%"]], ["speed","arrow","speed",["potency%","protection%","health%,offense%"]], ...]
"""
def createModsFromLine(sets, primaries, secondaries, done):
    res = []
    sets = removeDuplicateFromList(sets)
    for set in sets:
        for idx,primary in enumerate(primaries):
            secondariesToKeep = []
            for secondary in secondaries:
                if secondary != primary and len(secondariesToKeep) < 4:
                    secondariesToKeep.append(secondary)
            secondariesToKeep = sort_secondaries(secondariesToKeep)
            res.append([set, constants.potentialShape[idx],primary, secondariesToKeep, done[idx]]) # CHANGE WITH tools.Mod TODO
    return removeDuplicateFromList(res)