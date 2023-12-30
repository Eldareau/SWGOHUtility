import os
import csv
import tools
import constants

potentialSecondariesDuplicate = ["defense%", "health%", "offense%", "protection%"]

"""
Check tsv file validity
"""
def checkTsv():
    print("Checking tsv file conformity..")
    nbErrors = 0
    eof = False
    while not eof:
        with open(constants.tsvFileName,'r') as swgohRead:
            reader = csv.DictReader(swgohRead, delimiter="\t")
            lineNumber = 0
            for row in reader:
                lineNumber += 1
                if row.values() is not None:
                    primaries = row['primaries'].split(",")
                    secondaries = row['secondaries'].split(",")
                    for i in range(len(primaries)):
                        # primary isn't speed and doesn't with % -> problem (speed is the only flat primary)
                        # we ignore blank values (character mods aren't filled yet)
                        if primaries[i] != "speed" and primaries[i] != "" and primaries[i] != "-" and primaries[i][-1] != "%":
                            nbErrors += 1
                            print("Primary error, line: " + str(lineNumber))
                    for i in range(len(secondaries)):
                        # only %only secondaries 
                        if secondaries[i] == "tenacity" or secondaries[i] == "potency" or secondaries[i] == "criticalchance":
                            nbErrors += 1
                            print("Secondaries error, line: " + str(lineNumber) + " on secondary number " + str(i))
                    # we ignore "-" for duplicates
                    secondariesDuplicate = tools.list_duplicates(secondaries, "-")
                    if len(secondariesDuplicate) > 0:
                        nbErrors += 1
                        print("Duplicate error, line: " + str(lineNumber) + " on " + str(secondariesDuplicate))
                else:
                    nbErrors = -1
                    print("Something's wrong with your file format, tabulation might be missing somewhere ..")
            eof = True
    if nbErrors == 0:
        print("tsv file OK.")
    else:
        print("tsv file KO.. (" +str(nbErrors) + " errros found)")
    return nbErrors

"""
Open the wanted tsv file and update the values to look like the expected ones 
"""
def refractorTsv(nbTSVErrors):
    tsvName = constants.tsvFileName
    dummyName = tsvName[1:]
    os.rename(tsvName, dummyName)
    eof = False

    # open tsv
    with open(dummyName,'r') as swgohRead, open(tsvName, 'w', newline='') as swgohWrite:
        reader = csv.DictReader(swgohRead, delimiter="\t")
        writer = csv.DictWriter(swgohWrite, reader.fieldnames, delimiter="\t")
        writer.writeheader()
        while nbTSVErrors > 0 and not eof:
            for row in reader:
                if row.values() is not None:
                    primaries = row['primaries'].split(",")
                    secondaries = row['secondaries'].split(",")
                    for i in range(len(primaries)):
                        if primaries[i] != "speed" and primaries[i] != "" and primaries[i] != "-" and primaries[i][-1] != "%":
                            primaries[i] += "%"
                            nbTSVErrors -= 1
                    for i in range(len(secondaries)):
                        if secondaries[i] == "tenacity" or secondaries[i] == "potency" or secondaries[i] == "criticalchance":
                            secondaries[i] += "%"
                            nbTSVErrors -= 1
                    sortedSecondariesDuplicate = sorted(tools.list_duplicates(secondaries))
                    for dup in sortedSecondariesDuplicate:
                        combined = "\t".join(potentialSecondariesDuplicate)
                        if dup[0] in combined:
                            if "%" in dup[0]:
                                secondaries[dup[1][1]] = secondaries[dup[1][1]][:-1]
                            else:
                                secondaries[dup[1][0]] += "%"
                                nbTSVErrors -= 1
                    row['primaries'] = ",".join(primaries)
                    row['secondaries'] = ",".join(secondaries)
                    writer.writerow(row)
                else:
                    print("Something's wrong with your file format, tabulation might be missing somewhere ..")
                    nbTSVErrors = -1
            eof = True
    os.remove(dummyName)
    if nbTSVErrors > 0:
        nbTSVErrors = -1
    return nbTSVErrors 