"""
The purpose of this file is to create the tools and function needed to manage mods
"""

from dataclasses import dataclass
import collections
import constants
import csv
import os
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

def secondaryNotValid(secondary, primary, secondaries):
    return(not (secondary in constants.potentialSecondary) or secondary in secondaries or secondary == primary)

def groupOfFourSecondaries(primary):
    secondaries = constants.potentialSecondary[:]
    if primary in secondaries:
        secondaries.remove(str(primary))
    return list(combinations(secondaries, 4))


def DBGenerator():
    print("We're loading your tsv file. This part is critical please do not leave until the end")
    con = sqlite3.connect(constants.dataBaseName)
    cur = con.cursor()

    cur.execute("DROP TABLE IF EXISTS sets")
    cur.execute("DROP TABLE IF EXISTS shapes")
    cur.execute("DROP TABLE IF EXISTS primaries")
    cur.execute("DROP TABLE IF EXISTS secondaries")
    cur.execute("DROP TABLE IF EXISTS characters")
    cur.execute("DROP TABLE IF EXISTS mods")
    cur.execute("DROP TABLE IF EXISTS modForCharacter")

    cur.execute("CREATE TABLE sets (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE);")
    cur.execute("CREATE TABLE shapes (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE);")
    cur.execute("CREATE TABLE primaries (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE);")
    cur.execute("CREATE TABLE secondaries (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE);")
    cur.execute("CREATE TABLE characters (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE, Relic INTEGER);")
    cur.execute("CREATE TABLE mods (Id INTEGER NOT NULL PRIMARY KEY, Shape INTEGER NOT NULL, Sets INTEGER NOT NULL, Primaries INTEGER NOT NULL, Secondary1 INTEGER NOT NULL, Secondary2 INTEGER NOT NULL, Secondary3 INTEGER NOT NULL, Secondary4 INTEGER NOT NULL, FOREIGN KEY (Shape) REFERENCES shapes(Id), FOREIGN KEY (Sets) REFERENCES sets(Id), FOREIGN KEY (Primaries) REFERENCES primaries(Id), FOREIGN KEY (Secondary1) REFERENCES secondaries(Id), FOREIGN KEY (Secondary2) REFERENCES secondaries(Id), FOREIGN KEY (Secondary3) REFERENCES secondaries(Id), FOREIGN KEY (Secondary4) REFERENCES secondaries(Id), UNIQUE(Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4));")
    cur.execute("CREATE TABLE modForCharacter (Character_id INTEGER NOT NULL, Mod_id INTEGER NOT NULL, Number INTEGER NOT NULL, FOREIGN KEY(Character_id) REFERENCES characters(Id), FOREIGN KEY(Mod_id) REFERENCES mods(Id), UNIQUE(Character_id, Mod_id));")

    for set in constants.potentialSet:
        cur.execute("INSERT INTO sets (Name) VALUES (?);", (str(set),))

    for shape in constants.potentialShape:
        cur.execute("INSERT INTO shapes (Name) VALUES (?);", (str(shape),))

    for primary in constants.potentialPrimary:
        for prim in primary:
            cur.execute("INSERT OR IGNORE INTO primaries (Name) VALUES (?);", (str(prim),))

    for secondary in constants.potentialSecondary:
        cur.execute("INSERT INTO secondaries (Name) VALUES (?);", (str(secondary),))

    # create every possible combinations of mods
    for set in constants.potentialSet:
        for shape in constants.potentialShape:
            for primary in constants.potentialPrimary[constants.potentialShape.index(shape)]:
                for secondaries in groupOfFourSecondaries(primary):
                    secondaries = sort_secondaries(secondaries)
                    cur.execute("INSERT INTO mods (Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4) VALUES (?, ?, ?, ?, ?, ?, ?)", (set, constants.potentialShape.index(shape), primary, secondaries[0], secondaries[1], secondaries[2], secondaries[3]))

    con.commit()

    with open(constants.tsvFileName,'r') as swgohtsv:
        characters = csv.DictReader(swgohtsv, delimiter="\t")
        # scroll through characters
        for character in characters:
            # if name contain ' then we escape it (could be improve ?)
            if "'" in character['name']:
                name = character['name'].split("'")
                name[0] += "''"
                character['name'] = name[0] + name[1]
            cur.execute("INSERT INTO characters (Name, Relic) VALUES (?, ?)", (character['name'], character['relic']))
            # retrieve current character Id
            character_id = cur.lastrowid
            sets = character['sets'].split(",")
            primaries = character['primaries'].split(",")
            secondaries = character['secondaries'].split(",")
            done = character['done'].split(",")
            if len(sets) > 1 and len(primaries) == 6 and len(secondaries) > 3:
                # print((sets, primaries, secondaries))
                for set in sets:
                    # Shape number
                    primary_iter = 1
                    # If Mod hasn't been found yet
                    for primary in primaries:
                        if done[primary_iter-1] == "0":
                            number_needed = 1
                            secondaries = character['secondaries'].split(",")
                            secondary_iter = 0
                            # CHECK SIZE OF SECONDARIES (IF = 3 after the DEL -> PROBLEM)
                            while secondary_iter < 4 and len(secondaries) > 4:
                                if secondaries[secondary_iter] == primary:
                                    del secondaries[secondary_iter]
                                    break
                                secondary_iter += 1
                            # print((set, primary_iter, primary, secondaries[0], secondaries[1], secondaries[2], secondaries[3]))
                            # ordering the secondaries
                            secondaries = sort_secondaries(secondaries)
                            cur.execute("INSERT OR IGNORE INTO mods (Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4) VALUES (?, ?, ?, ?, ?, ?, ?)", (set, primary_iter, primary, secondaries[0], secondaries[1], secondaries[2], secondaries[3]))
                            cur.execute("SELECT Id FROM mods WHERE (Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4)=(?, ?, ?, ?, ?, ?, ?)", (set, primary_iter, primary, secondaries[0], secondaries[1], secondaries[2], secondaries[3]))
                            mod_id = cur.fetchall()[0][0]
                            cur.execute("SELECT COUNT(*) FROM modForCharacter WHERE Character_id=" + str(character_id) + " AND Mod_id=" + str(mod_id))
                            exist = cur.fetchall()[0][0]
                            if exist != 0:
                                number_needed += 1
                            # print((character_id, mod_id, number_needed))
                            cur.execute("INSERT OR REPLACE INTO modForCharacter (Character_id, Mod_id, Number) VALUES (?, ?, ?)", (character_id, mod_id, number_needed))
                        primary_iter += 1
    con.commit()
    con.close()
    print(constants.dataBaseName + " has been created succesfully.")
    return 0

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
def list_duplicates(seq):
    tally = collections.defaultdict(list)
    for i,item in enumerate(seq):
        tally[item].append(i)
    return ((key,locs) for key,locs in tally.items() if len(locs)>1)

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
Open the wanted tsv file and update the values to look like the expected ones 
"""
def refractor_tsv(name):
    dummy_name = name[1:]
    os.rename(name, dummy_name)

    # open tsv
    with open(dummy_name,'r') as swgohRead:
        reader = csv.DictReader(swgohRead, delimiter="\t")
        header = next(reader)
        with open(name, 'w', newline='') as swgohWrite:
            writer = csv.DictWriter(swgohWrite, list(header.keys()), delimiter="\t")
            writer.writerow(header)
            for row in reader:
                primaries = row['primary'].split(",")
                secondaries = row['secondaries'].split(",")
                for i in range(len(primaries)):
                    if primaries[i] != "speed" and primaries[i] != "" and primaries[i][-1] != "%":
                        primaries[i] += "%"
                for i in range(len(secondaries)):
                    if secondaries[i] == "tenacity" or secondaries[i] == "potency" or secondaries[i] == "criticalchance":
                        secondaries[i] += "%"
                for dup in sorted(list_duplicates(secondaries)):
                    secondaries[dup[1][0]] += "%"
                row['primaries'] = ",".join(primaries)
                row['secondaries'] = ",".join(secondaries)
                writer.writerow(row)
    os.remove(dummy_name)
    return 0

def mostNeededModSet():
    # TODO
    return