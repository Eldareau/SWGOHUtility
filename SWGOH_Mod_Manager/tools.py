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
    res = genSetDict()
    con = sqlite3.connect(constants.dataBaseName)
    cur = con.cursor()
    cur.execute("SELECT Mod_id FROM modForCharacter WHERE Done=0")
    mod_ids = cur.fetchall()
    if mod_ids != []:
        mod_ids = list_elements_in_tuple(mod_ids)
        for mod_id in mod_ids:
            cur.execute("SELECT Sets FROM mods WHERE (id)=(?)", mod_id[0])
            set = cur.fetchall()
            if set != []:
                res[set[0][0]] += len(mod_id[1])
            else:
                print("We couldn't find this mod in database..")
    else:
        print("No more mods to find, you found them all !")
    res = dict(sorted(res.items(), key=lambda x:x[1], reverse=True))
    i = 1
    for key,value in res.items():
        print(str(i) + " : " + str(key) + " (" + str(value) + ")")
        i += 1

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
IN : List, seq element type
OUT : Dict
EX:
list_duplicates([1, 2, 3, 1, 2, 1, 0, 2, 0, 4]) = [(1, [0, 3, 5]), (2, [1, 4, 7]), (0, [6, 8])]
list_duplicates(["hello", "my", "hello", "hello", "my", "name", "is", "hello"]) = [('hello', [0, 2, 3, 7]) = [('hello', [0, 2, 3, 7]), ('my', [1, 4])]
"""
def list_duplicates(seq, ignore=None):
    tally = collections.defaultdict(list)
    for i,item in enumerate(seq):
        if item != ignore:
            tally[item].append(i)
    return list((key,locs) for key,locs in tally.items() if len(locs)>1)

"""
Give the elements and their position in list.
IN : List
OUT : Dict
EX:
list_elements_in_tuple([1, 2, 3, 1, 2, 1, 0, 2, 0, 4]) = [(1, [0, 3, 5]), (2, [1, 4, 7]), (3, [2]), (0, [6, 8]), (4, [9])]
list_elements_in_tuple(["hello", "my", "hello", "hello", "my", "name", "is", "hello"]) = [('hello', [0, 2, 3, 7]), ('my', [1, 4]), ('name', [5]), ('is', [6])]
"""
def list_elements_in_tuple(seq):
    tally = collections.defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return list((key,locs) for key,locs in tally.items())

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

"""
Generate dictory with potentialSet as keys
"""
def genSetDict():
    res = {}
    for set in constants.potentialSet:
        res[set] = 0
    return res