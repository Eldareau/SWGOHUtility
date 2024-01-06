import constants
import tools
import sqlite3
import csv
import os
import dbGenerator

def findMod():
    # ask for the wanted mod
    #wantedMod = askingForMod()
    wantedMod = tools.Mod("speed", "triangle", "protection%", ["speed", "protection", "tenacity%", "-"])

    # retrieve the list of character that want the wanted mod
    charactersNameList = searchForMod(wantedMod)

    # display the result & ask for response
    updateDatabase = askForAction(charactersNameList)

    if updateDatabase > 0:
        # update the tsv file and database depending on the wanted action
        update_tsv(wantedMod, charactersNameList[updateDatabase-1])
        dbGenerator.update_DB(wantedMod, charactersNameList[updateDatabase-1])
    elif updateDatabase == -1:
        print("Something went wrong ..")

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
        while tools.secondaryNotValid(secondaryAsked, primaryAsked, secondaries):
            print("You entered " + secondaryAsked + " but the secondary value must be one of those and unique : " + str(
                constants.potentialSecondary))
            secondaryAsked = input().lower()
        nbSecondaries += 1
        secondaries.append(secondaryAsked)

    return tools.Mod(setAsked, shapeAsked, primaryAsked, secondaries)

"""
Search the mod in database and return a list of character that might want it
"""
def searchForMod(wantedMod):
    char_name = []
    con = sqlite3.connect(constants.dataBaseName)
    cur = con.cursor()
    # sort secondaries for easier search in database
    wantedMod.secondaries = tools.sort_secondaries(wantedMod.secondaries)
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
        while tools.not_a_valid_number(answer, len(resList)):
            print("Please select a number between 0 and " + str(len(resList)))
            answer = input()
        answer = int(answer)
        if answer == 0:
            print("You chose 0 : nothing to do")
            res = 0
        else:
            print("You chose : " + str(resList[answer-1]) + ", we are updating the database")
            res = answer
    else:
        print("No one would want this Mod, you can sell it")
        res = 0
    return res

"""
Update the tsv file
"""
def update_tsv(mod, charactersName):
    # retrieve shape name from shape id
    modNb = constants.potentialShape.index(mod.shape)
    name = constants.tsvFileName
    print("This part is critical please do not leave until the end")
    temp_name = name[1:]

    # open tsv
    with open(name,'r') as swgohRead, open(temp_name, 'w', newline='') as swgohWrite:
        reader = csv.DictReader(swgohRead, delimiter="\t")
        writer = csv.DictWriter(swgohWrite, reader.fieldnames, delimiter="\t")
        writer.writeheader()
        for row in reader:
            if row['name'] == charactersName:
                done = row['done'].split(",")
                done[modNb-1] = mod.set
                row['done'] = ",".join(done)
            writer.writerow(row)

    os.remove(name)
    os.rename(temp_name, name)
    return 0