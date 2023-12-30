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
            print("The mod you are trying to build has too much or not enough secondary stats (need 4, " + len(secondaries) + " provided)")

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
            print("The mod you are trying to build has too much or not enough secondary stats (need 4, " + len(secondaries) + " provided)")
    
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

def mostNeededModSet():
    # TODO
    return

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