import csv, sqlite3
import tools
import constants

def DBGenerator():
    con = sqlite3.connect("swgoh.db")
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
    cur.execute("CREATE TABLE modForCharacter (Character_id INTEGER NOT NULL, Mod_id INTEGER NOT NULL, Number INTEGER NOT NULL, FOREIGN KEY(Character_id) REFERENCES characters(Id) ON DELETE CASCADE, FOREIGN KEY(Mod_id) REFERENCES mods(Id) ON DELETE CASCADE, UNIQUE(Character_id, Mod_id));")

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

    with open('SWGOHCharacters.tsv','r') as swgohtsv:
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
            if len(sets) > 1 and len(primaries) == 6 and len(secondaries) > 3:
                # print((sets, primaries, secondaries))
                for set in sets:
                    # Shape number
                    primary_iter = 1
                    for primary in primaries:
                        number_needed = 1
                        secondaries = i['secondaries'].split(",")
                        secondary_iter = 0
                        # CHECK SIZE OF SECONDARIES (IF = 3 after the DEL -> PROBLEM)
                        while secondary_iter < 4 and len(secondaries) > 4:
                            if secondaries[secondary_iter] == primary:
                                del secondaries[secondary_iter]
                                break
                            secondary_iter += 1
                        print((set, primary_iter, primary, secondaries[0], secondaries[1], secondaries[2], secondaries[3]))
                        # ordering the secondaries (order defined in tools.py)
                        secondaries = tools.sort_secondaries(secondaries)
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
    return 0

"""
Search the mod in database and return a list of character that might want it
"""
def searchForMod(wantedMod):
    resList = []
    con = sqlite3.connect("swgoh.db")
    cur = con.cursor()
    wantedMod.secondaries = tools.sort_secondaries(wantedMod.secondaries)
    print(wantedMod)
    print(constants.potentialShape.index(wantedMod.shape)+1)
    cur.execute("SELECT Id FROM mods WHERE (Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4)=(?, ?, ?, ?, ?, ?, ?)", (wantedMod.set, constants.potentialShape.index(wantedMod.shape)+1, wantedMod.primary, wantedMod.secondaries[0], wantedMod.secondaries[1], wantedMod.secondaries[2], wantedMod.secondaries[3]))
    mod_id = cur.fetchall()[0]
    con.close()
    return resList

"""
Add new character to database
"""
def addCharacterToDB():
    con = sqlite3.connect("swgoh.db")
    cur = con.cursor()
    cur.execute("INSERT INTO secondaries (Name) VALUES ('criticalchance%');")
    con.commit()
    con.close()
    return 0