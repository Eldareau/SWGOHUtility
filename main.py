"""
The purpose of this file is to combine all of the elemente to create the perfect tool to manage mods in SWGOH
"""

# import PySimpleGUI as sg
import tools
import integrity
import dataBaseManagement
import csv
import os

def findMod():
    """ ask for the wanted mod """
    wantedMod = tools.askingForMod()

    """ retrieve all the mods """
    potentialMods = tools.openModsFile()

    """ compare with the list """
    resList = tools.comparePotentialWanted(potentialMods, wantedMod)

    """ display the result & ask for response"""
    tools.askForAction(resList)

def neededMods():
    # TODO
    return

def mostNeededModSet():
    # TODO
    return

"""
Open the wanted tsv file and update the values to look like the expected ones 
"""
def refractorTSV(name):
    dummy_name = name[1:]
    os.rename(name, dummy_name)

    # open tsv
    with open(dummy_name,'r') as swgohtsv:
        reader = csv.reader(swgohtsv, delimiter="\t")
        header = next(reader)
        with open(name, 'w', newline='') as swgoh:
            writer = csv.writer(swgoh, delimiter="\t")
            writer.writerow(header)
            for row in reader:
                primaries = row[3].split(",")
                secondaries = row[4].split(",")
                for i in range(len(primaries)):
                    if primaries[i] != "speed" and primaries[i] != "" and primaries[i][-1] != "%":
                        primaries[i] += "%"
                for i in range(len(secondaries)):
                    if secondaries[i] == "tenacity" or secondaries[i] == "potency" or secondaries[i] == "criticalchance":
                        secondaries[i] += "%"
                for dup in sorted(tools.list_duplicates(secondaries)):
                    secondaries[dup[1][0]] += "%"
                row[3] = ",".join(primaries)
                row[4] = ",".join(secondaries)
                writer.writerow(row)
    os.remove(dummy_name)
    return

dataBaseManagement.DBGenerator()
# findMod()
# refractorTSV('SWGOHCharacters.tsv')
print("Done.")