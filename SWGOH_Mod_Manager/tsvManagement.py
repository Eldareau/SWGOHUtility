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
            lineNumber = 1
            for row in reader:
                lineNumber += 1
                if row.values() is not None:
                    setErrors = 0
                    sets = row['sets'].split(",")
                    primaries = row['primaries'].split(",")
                    secondaries = row['secondaries'].split(",")
                    if len(sets) > 1 and len(primaries) > 1 and len(secondaries) > 1:
                        for i in range(len(sets)):
                            if sets[i] not in constants.potentialSet:
                                nbErrors += 1
                                setErrors += 1
                                print("Set error, line " + str(lineNumber) + " on " + sets[i] + ", set number " + str(i+1) + " must be one of those values : " + str(constants.potentialSet))
                        if setErrors == 0 and tools.computeSetValue(sets) != 6:
                            nbErrors += 1
                            print("Set error, line " + str(lineNumber) + " on " + sets[i] + ", you either put set too much sets or not enough " + str(sets))
                        for i in range(len(primaries)):
                            if primaries[i] not in constants.potentialPrimary[i]:
                                nbErrors += 1
                                print("Primary error, line " + str(lineNumber) + " on " + primaries[i] + ", primary number " + str(i+1) + " must be one of those values : " + str(constants.potentialPrimary[i]))
                            # primary isn't speed and doesn't with % -> problem (speed is the only flat primary)
                            # we ignore blank values (character mods aren't filled yet)
                            elif primaries[i] != "speed" and primaries[i] != "" and primaries[i] != "-" and not primaries[i].endswith("%"):
                                nbErrors += 1
                                print("Primary error, line " + str(lineNumber) + " on " + primaries[i] + " (% missing)")
                            elif primaries[i].endswith("%%"):
                                nbErrors += 1
                                print("Primary error, line " + str(lineNumber) + " on " + primaries[i] + " (double %%)")
                        for i in range(len(secondaries)):
                            if secondaries[i] not in constants.potentialSecondary:
                                nbErrors += 1
                                print("Secondaries error, line " + str(lineNumber) + " on " + secondaries[i] + ", secondary number " + str(i+1) + " must be one of those values : " + str(constants.potentialSecondary))
                            # only %only secondaries 
                            elif secondaries[i] == "tenacity" or secondaries[i] == "potency" or secondaries[i] == "criticalchance":
                                nbErrors += 1
                                print("Secondaries error, line " + str(lineNumber) + " on " + secondaries[i] + " (% missing)")
                            elif secondaries[i].endswith("%%"):
                                nbErrors += 1
                                print("Secondaries error, line " + str(lineNumber) + " on " + secondaries[i] + " (double %%)")
                        # we ignore "-" for duplicates
                        secondariesDuplicate = tools.list_duplicates(secondaries, "-")
                        if len(secondariesDuplicate) > 0:
                            nbErrors += 1
                            print("Duplicate error, line " + str(lineNumber) + " on " + str(secondariesDuplicate[0][0]) + ", secondary number " + str(secondariesDuplicate[0][1][0]) + " and " + str(secondariesDuplicate[0][1][1]) + " are duplicate.")
                    else:
                        print("Line " + str(lineNumber) + " (" + row['name'] + ") has been ignored (incomplete)")
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
        startingError = nbTSVErrors
        while nbTSVErrors > 0 and not eof:
            for row in reader:
                if row.values() is not None:
                    sets = row['sets'].split(",")
                    primaries = row['primaries'].split(",")
                    secondaries = row['secondaries'].split(",")
                    if len(sets) > 1 and len(primaries) > 1 and len(secondaries) > 1:
                        for i in range(len(primaries)):
                            if primaries[i] != "speed" and primaries[i] != "" and primaries[i] != "-" and primaries[i][-1] != "%":
                                primaries[i] += "%"
                                nbTSVErrors -= 1
                            if primaries[i].endswith("%%"):
                                primaries[i] = primaries[i][:-1]
                                nbTSVErrors -= 1
                        for i in range(len(secondaries)):
                            if secondaries[i] == "tenacity" or secondaries[i] == "potency" or secondaries[i] == "criticalchance":
                                secondaries[i] += "%"
                                nbTSVErrors -= 1
                            if secondaries[i].endswith("%%"):
                                secondaries[i] = secondaries[i][:-1]
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
    print(str(startingError - nbTSVErrors) + " errors has been fixed.")
    if nbTSVErrors > 0:
        nbTSVErrors = -1
    if nbTSVErrors == 0:
        print("TSV file has been fixed succesfully.")
    return nbTSVErrors 