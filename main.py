"""
The purpose of this file is to combine all of the elemente to create the perfect tool to manage mods in SWGOH
"""

# import PySimpleGUI as sg
import tools
import integrity

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

findMod()