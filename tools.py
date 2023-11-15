"""
The purpose of this file is to create the tools and function needed to manage mods
"""

from dataclasses import dataclass
import collections
import constants
import csv
import os
import sqlite3

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

def secondaryValid(secondary, primary, secondaries):
    return(not (secondary in constants.potentialSecondary) or secondary in secondaries or secondary == primary)

def DBGenerator():
    con = sqlite3.connect(constants.dataBaseName)
    cur = con.cursor()

    cur.execute("DROP TABLE sets")
    cur.execute("DROP TABLE shapes")
    cur.execute("DROP TABLE primaries")
    cur.execute("DROP TABLE secondaries")
    cur.execute("DROP TABLE characters")
    cur.execute("DROP TABLE mods")
    cur.execute("DROP TABLE modForCharacter")

    cur.execute("CREATE TABLE sets (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE);")
    cur.execute("CREATE TABLE shapes (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE);")
    cur.execute("CREATE TABLE primaries (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE);")
    cur.execute("CREATE TABLE secondaries (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE);")
    cur.execute("CREATE TABLE characters (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE, Relic INTEGER);")
    cur.execute("CREATE TABLE mods (Id INTEGER NOT NULL PRIMARY KEY, Shape INTEGER NOT NULL, Sets INTEGER NOT NULL, Primaries INTEGER NOT NULL, Secondary1 INTEGER NOT NULL, Secondary2 INTEGER NOT NULL, Secondary3 INTEGER NOT NULL, Secondary4 INTEGER NOT NULL, FOREIGN KEY (Shape) REFERENCES shapes(Id), FOREIGN KEY (Sets) REFERENCES sets(Id), FOREIGN KEY (Primaries) REFERENCES primaries(Id), FOREIGN KEY (Secondary1) REFERENCES secondaries(Id), FOREIGN KEY (Secondary2) REFERENCES secondaries(Id), FOREIGN KEY (Secondary3) REFERENCES secondaries(Id), FOREIGN KEY (Secondary4) REFERENCES secondaries(Id), UNIQUE(Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4));")
    cur.execute("CREATE TABLE modForCharacter (Character_id INTEGER NOT NULL, Mod_id INTEGER NOT NULL, Number INTEGER NOT NULL, FOREIGN KEY(Character_id) REFERENCES characters(Id), FOREIGN KEY(Mod_id) REFERENCES mods(Id), UNIQUE(Character_id, Mod_id));")

    cur.execute("INSERT INTO sets (Name) VALUES ('health');")
    cur.execute("INSERT INTO sets (Name) VALUES ('defense');")
    cur.execute("INSERT INTO sets (Name) VALUES ('criticaldamage');")
    cur.execute("INSERT INTO sets (Name) VALUES ('criticalchance');")
    cur.execute("INSERT INTO sets (Name) VALUES ('tenacity');")
    cur.execute("INSERT INTO sets (Name) VALUES ('offense');")
    cur.execute("INSERT INTO sets (Name) VALUES ('potency');")
    cur.execute("INSERT INTO sets (Name) VALUES ('speed');")

    cur.execute("INSERT INTO shapes (Name) VALUES ('square');")
    cur.execute("INSERT INTO shapes (Name) VALUES ('arrow');")
    cur.execute("INSERT INTO shapes (Name) VALUES ('rhombus');")
    cur.execute("INSERT INTO shapes (Name) VALUES ('triangle');")
    cur.execute("INSERT INTO shapes (Name) VALUES ('circle');")
    cur.execute("INSERT INTO shapes (Name) VALUES ('cross');")

    cur.execute("INSERT INTO primaries (Name) VALUES ('accuracy%');")
    cur.execute("INSERT INTO primaries (Name) VALUES ('criticalavoidance%');")
    cur.execute("INSERT INTO primaries (Name) VALUES ('criticalchance%');")
    cur.execute("INSERT INTO primaries (Name) VALUES ('criticaldamage%');")
    cur.execute("INSERT INTO primaries (Name) VALUES ('defense%');")
    cur.execute("INSERT INTO primaries (Name) VALUES ('health%');")
    cur.execute("INSERT INTO primaries (Name) VALUES ('offense%');")
    cur.execute("INSERT INTO primaries (Name) VALUES ('potency%');")
    cur.execute("INSERT INTO primaries (Name) VALUES ('protection%');")
    cur.execute("INSERT INTO primaries (Name) VALUES ('speed');")
    cur.execute("INSERT INTO primaries (Name) VALUES ('tenacity%');")

    cur.execute("INSERT INTO secondaries (Name) VALUES ('criticalchance%');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('defense');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('defense%');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('health');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('health%');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('offense');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('offense%');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('potency%');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('protection');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('protection%');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('speed');")
    cur.execute("INSERT INTO secondaries (Name) VALUES ('tenacity%');")

    with open(constants.tsvFileName,'r') as swgohtsv:
        dr = csv.DictReader(swgohtsv, delimiter="\t")
        # scroll through characters
        for i in dr:
            # if name contain ' then we escape it (could be improve ?)
            if "'" in i['name']:
                name = i['name'].split("'")
                name[0] += "''"
                i['name'] = name[0] + name[1]
            cur.execute("INSERT INTO characters (Name, Relic) VALUES (?, ?)", (i['name'], i['relic']))
            # retrieve current character Id
            character_id = cur.lastrowid
            sets = i['sets'].split(",")
            primaries = i['primaries'].split(",")
            secondaries = i['secondaries'].split(",")
            done = i['done'].split(",")
            if len(sets) > 1 and len(primaries) == 6 and len(secondaries) > 3:
                # print((sets, primaries, secondaries))
                for set in sets:
                    # Shape number
                    primary_iter = 1
                    # If Mod hasn't been found yet
                    for primary in primaries:
                        if done[primary_iter-1] == "0":
                            number_needed = 1
                            secondaries = i['secondaries'].split(",")
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
    print(constants.dataBaseName + " has been created succesfully")
    return 0

"""
Search the mod in database and return a list of character that might want it
"""
def searchForMod(wantedMod):
    char_name = []
    con = sqlite3.connect(constants.dataBaseName)
    cur = con.cursor()
    # sort secondaries for easier search in database
    wantedMod.secondaries = sort_secondaries(wantedMod.secondaries)
    print("Looking for this Mod : " + wantedMod.set + ", " + wantedMod.shape + ", " + wantedMod.primary + ", " + str(wantedMod.secondaries))
    cur.execute("SELECT Id FROM mods WHERE (Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4)=(?, ?, ?, ?, ?, ?, ?)", (wantedMod.set, constants.potentialShape.index(wantedMod.shape)+1, wantedMod.primary, wantedMod.secondaries[0], wantedMod.secondaries[1], wantedMod.secondaries[2], wantedMod.secondaries[3],))
    mod_id = cur.fetchall()[0][0]
    cur.execute("SELECT Character_id FROM modForCharacter WHERE (Mod_id)=(?)", (mod_id,))
    char_ids = cur.fetchall()
    # iter through all the found characters
    for char_id in char_ids:
        cur.execute("SELECT Name FROM characters WHERE (Id)=(?)", (char_id[0],))
        char_name.append(cur.fetchall()[0][0])
    con.close()
    return char_name

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
Ask the user for the mod he have
"""
def askingForMod():
    nbSecondaries = 0
    secondaries = []

    print("Please enter enter the mod you have.")

    print("First enter the mod Set : " + str(constants.potentialSet))
    setAsked = input().lower()
    while not setAsked in constants.potentialSet:
        print("You entered " + setAsked + " but the Set value must be one of those : " + str(constants.potentialSet))
        setAsked = input().lower()

    print("Then enter the mod Shape : " + str(constants.potentialShape))
    shapeAsked = input().lower()
    while not shapeAsked in constants.potentialShape:
        print("You entered " + shapeAsked + " but the Shape value must be one of those : " + str(constants.potentialShape))
        shapeAsked = input().lower()

    correctPrimariesValues = constants.potentialPrimary[constants.potentialShape.index(shapeAsked)]

    print("Then enter the mod Primary : " + str(correctPrimariesValues))
    primaryAsked = input().lower()
    while not primaryAsked in correctPrimariesValues:
        print("You entered " + primaryAsked + " but the Primary value must be one of those : " + str(
            correctPrimariesValues))
        primaryAsked = input().lower()

    print("Finally enter the mod four Secondaries : ")
    while nbSecondaries < 4:
        print("The " + str(nbSecondaries + 1) + "th secondary among this list: " + str(constants.potentialSecondary))
        secondaryAsked = input().lower()
        while secondaryValid(secondaryAsked, primaryAsked, secondaries):
            print("You entered " + secondaryAsked + " but the secondary value must be one of those and unique : " + str(
                constants.potentialSecondary))
            secondaryAsked = input().lower()
        nbSecondaries += 1
        secondaries.append(secondaryAsked)

    return Mod(setAsked, shapeAsked, primaryAsked, secondaries)

"""
Ask the user for input if a mod has been found
"""
def askForAction(resList):
    res = -1
    if len(resList) > 0:
        print("We found matches for your Mod : \n")
        for i in range(len(resList)):
            print(str(i+1) + " : " + str(resList[i]) + " \n")
        print("You can now either equip it with the associated number or sell it/do nothing with 0 : (only number are accepted)")
        answer = input()
        while not_a_valid_number(answer, len(resList)):
            print("Please select a number between 0 and " + str(len(resList)))
            answer = input()
        if int(answer) == 0:
            print("You chose 0 : nothing to do")
            res = 0
        else:
            print("You chose : " + str(answer) + ", we are updating the database")
            res = int(answer)
    else:
        print("No one would want this Mod, you can sell it")
        res = 0
    return res

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
Update the tsv file
"""
def update_tsv(mod, charactersName):
    print(mod)
    print(charactersName)
    # retrieve shape name from shape id
    modNb = constants.potentialShape.index(mod.shape)+1
    name = constants.tsvFileName
    print("This part is critical please do not leave until the end")
    dummy_name = name[1:]

    # open tsv
    with open(name,'r') as swgohRead:
        reader = csv.DictReader(swgohRead, delimiter="\t")
        header = next(reader)
        print(header)
        input()
        with open(dummy_name, 'w', newline='') as swgohWrite:
            writer = csv.DictWriter(swgohWrite, list(header.keys()), delimiter="\t")
            writer.writerow(header)
            for row in reader:
                if row['name'] == charactersName:
                    done = row['done'].split(",")
                    done[modNb] = mod.set
                    row['done'] = ",".join(done)
                writer.writerow(row)

    os.remove(name)
    os.rename(dummy_name, name)
    return 0

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

def findMod():
    """ ask for the wanted mod """
    # wantedMod = askingForMod()
    wantedMod = Mod("speed", "square", "offense%", ["health%", "health", "potency%", "speed"])

    """ retrieve the list of character that want the wanted mod """
    charactersNameList = searchForMod(wantedMod)

    """ display the result & ask for response """
    updateDatabase = askForAction(charactersNameList)

    if updateDatabase > 0:
        """ update the database depending on the wanted action """
        update_tsv(wantedMod, charactersNameList[updateDatabase-1])
    elif updateDatabase == -1:
        print("Something went wrong ..")

def mostNeededModSet():
    # TODO
    return