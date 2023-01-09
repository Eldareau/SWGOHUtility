import PySimpleGUI as sg
import tools

def findMod():
    """ ask for the wanted mod """
    wantedMod = tools.askingForMod()

    """ retrieve all the mods """
    potentialMods = tools.openModsFile()

    """ compare with the list """
    resList = tools.comparePotentialWanted()

    """ display the result & ask for response"""
    tools.askForAction()

def neededMods():
    # TODO
    return

def mostNeededModSet():
    # TODO
    return

findMod()