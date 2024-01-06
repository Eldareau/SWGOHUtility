import constants
import sqlite3
import tools
import csv
import tsvManagement

"""
Generate sqlite database from tsv file
"""
def DBGenerator():
    # check csv file
    nbTSVErrors = tsvManagement.checkTsv()

    if nbTSVErrors > 0:
        # try to correct tsv file
        print("Current tsv file might be fixable, launching tsv manager")
        nbTSVErrors = tsvManagement.refractorTsv(nbTSVErrors)

    if nbTSVErrors == 0:

        # generate basic informations to database
        generateBasicInformations()

        # add tsv file informations
        addCharsAndModsToDB()
        
        print(constants.dataBaseName + " has been created succesfully.")
    
    else:

        print("tsv manager couldn't fix current tsv file.")

    return nbTSVErrors

def generateBasicInformations():
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
    cur.execute("CREATE TABLE mods (Id INTEGER NOT NULL PRIMARY KEY, Shape INTEGER NOT NULL, Sets INTEGER NOT NULL, Primaries INTEGER NOT NULL, Secondary1 INTEGER NOT NULL, Secondary2 INTEGER NOT NULL, Secondary3 INTEGER NOT NULL, Secondary4 INTEGER NOT NULL, FOREIGN KEY (Shape) REFERENCES shapes(Id), FOREIGN KEY (Sets) REFERENCES sets(Id), FOREIGN KEY (Primaries) REFERENCES primaries(Id), FOREIGN KEY (Secondary1) REFERENCES secondaries(Id), FOREIGN KEY (Secondary2) REFERENCES secondaries(Id), FOREIGN KEY (Secondary3) REFERENCES secondaries(Id), FOREIGN KEY (Secondary4) REFERENCES secondaries(Id), UNIQUE(Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4));")
    cur.execute("CREATE TABLE characters (Id INTEGER NOT NULL PRIMARY KEY, Name TEXT NOT NULL UNIQUE, Relic INTEGER);")
    cur.execute("CREATE TABLE modForCharacter (Character_id INTEGER NOT NULL, Mod_id INTEGER NOT NULL, Done BOOLEAN NOT NULL CHECK (Done IN (0, 1)), FOREIGN KEY(Character_id) REFERENCES characters(Id), FOREIGN KEY(Mod_id) REFERENCES mods(Id), UNIQUE(Character_id, Mod_id));")

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
                for secondaries in tools.groupOfFourSecondaries(primary):
                    secondaries = tools.sort_secondaries(secondaries)
                    cur.execute("INSERT INTO mods (Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4) VALUES (?, ?, ?, ?, ?, ?, ?)", (set, constants.potentialShape.index(shape), primary, secondaries[0], secondaries[1], secondaries[2], secondaries[3]))

    con.commit()
    con.close()
    
def addCharsAndModsToDB():
    con = sqlite3.connect(constants.dataBaseName)
    cur = con.cursor()

    with open(constants.tsvFileName,'r') as swgohtsv:
        characters = csv.DictReader(swgohtsv, delimiter="\t")
        # scroll through characters
        for character in characters: 
            cur.execute("INSERT INTO characters (Name, Relic) VALUES (?, ?)", (character['name'], character['relic']))
            # retrieve current character Id
            character_id = cur.lastrowid
            sets = character['sets'].split(",")
            primaries = character['primaries'].split(",")
            secondaries = character['secondaries'].split(",")
            done = character['done'].split(",")
            if (len(sets) == 2 or len(sets) == 3) and len(primaries) == 6 and len(secondaries) == 5:
                mods = tools.createModsFromLine(sets, primaries, secondaries, done)
                for mod in mods:
                    # we search for the mod in the database
                    cur.execute("SELECT Id FROM mods WHERE (Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4)=(?, ?, ?, ?, ?, ?, ?)", (mod[0], constants.potentialShape.index(mod[1]), mod[2], mod[3][0], mod[3][1], mod[3][2], mod[3][3]))
                    mod_id = cur.fetchall()
                    if mod_id != []:
                        # if we found it
                        mod_id = mod_id[0][0]
                        cur.execute("SELECT COUNT(*) FROM modForCharacter WHERE Character_id=" + str(character_id) + " AND Mod_id=" + str(mod_id))
                        exist = cur.fetchall()[0][0]
                        if exist != 0:
                            print("Duplicate entry in database")
                        else:
                            cur.execute("INSERT OR REPLACE INTO modForCharacter (Character_id, Mod_id, Done) VALUES (?, ?, ?)", (character_id, mod_id, mod[4]!='0'))
                    else:
                        print("Database isn't complete..")
    con.commit()
    con.close()

def update_DB(mod, charactersName):
    con = sqlite3.connect(constants.dataBaseName)
    cur = con.cursor()

    cur.execute("SELECT Id FROM mods WHERE (Sets, Shape, Primaries, Secondary1, Secondary2, Secondary3, Secondary4)=(?, ?, ?, ?, ?, ?, ?)", (mod.set, constants.potentialShape.index(mod.shape), mod.primary, mod.secondaries[0], mod.secondaries[1], mod.secondaries[2], mod.secondaries[3]))
    mod_id = cur.fetchall()
    cur.execute("SELECT Id FROM characters WHERE (Name)=(?)", (charactersName,))
    character_id = cur.fetchall()
    
    if mod_id != [] and character_id != []:
        mod_id = mod_id[0][0]
        character_id = character_id[0][0]
        cur.execute("UPDATE modForCharacter SET Done = 1 WHERE (Character_id, Mod_id)=(?, ?) RETURNING *", (character_id, 100000))
        res = cur.fetchall()
        print(charactersName)
    else:
        print("Impossible to find said character and mod..")
        input()

    con.commit()
    con.close()