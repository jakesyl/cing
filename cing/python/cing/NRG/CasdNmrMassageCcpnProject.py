"""
With help from Wim Vranken.
For example:
    - changing the MS name from 2kkx to ET109AredOrg
    - swap checks/changes

# Execute like e.g.:
# python -u $CINGROOT/python/cing/NRG/CasdNmrMassageCcpnProject.py ET109AredOrg ET109AredUtrecht
if the input project is in cwd.

Most functionality is hard-coded here so be careful reading the actual code.
"""
from cing.Libs.DBMS import DBMS
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Libs.disk import copy
from cing.Libs.disk import globMultiplePatterns
from cing.NRG import CASD_NMR_BASE_NAME
from cing.NRG.PDBEntryLists import writeEntryListToFile
from cing.core.constants import * #@UnusedWildImport
from glob import glob1
import tarfile, json

__author__ = "Wim Vranken <wim@ebi.ac.uk> Jurgen Doreleijers <jurgenfd@gmail.com>"
#    inputDir = os.path.join(cingDirTestsData, "ccpn")
#try:
#    from cing.NRG.localConstants import baseDir #@UnresolvedImport # pylint: disable=E0611
#except:
    #baseDir = '/Users/jd/CASD-NMR-CING'
#    baseDir = '/Volumes/UserHome/geerten/Data/CASD-NMR-CING'

#dataOrgDir = os.path.join(baseDir, DATA_STR)
#dataDir = os.path.join(baseDir, DATA_STR)
#startDir = '/Library/WebServer/Documents/' + CASD_NMR_BASE_NAME


# NBNB TBD this file is partly fixed and probably broken.
# Anyway it is broken already because the haousekeepign fiel system ic changed
# the file lcoations ahve changed, etc.
# NBNB FIX OR PENSION OFF.
# See CasdScripts.py for alternatives

cingDataDir = os.environ.get('CINGDATAROOT')
dataDir = os.path.join(cingDataDir, CASD_NMR_BASE_NAME, DATA_STR)
inputDir = dataDir
calcDataFile = os.path.join(dataDir, 'calcData.json')
calcData = json.load(open(calcDataFile))

colorByLab = {
    'Cheshire': 'green',
    'Frankfurt': 'blue',
    'Lyon': 'red',
    'Paris': 'darkblue',
    'Piscataway': 'orange',
    'Seattle': 'gold',
    'Utrecht': 'darkgreen'
}
def convertToProgram(t):
    """check if there is an x for each and creates a string Hash by row and Hash by column"""

    # Assumes first column has the row labels. This is called a header column in Numbers.
    rowLabelList = t.getColumnByIdx(0)
    rowSize = t.sizeRows()
    result = {}
    for r in range(rowSize):
        rowLabel = rowLabelList[r]
        result[rowLabel] = {}
        resultRow = result[rowLabel]
        for c, columnLabel in enumerate(t.columnOrder):
            if c == 0:
                continue
            column = t.attr[columnLabel]
            value = column[r].lower()

            valueEnumerated = None
            if value == 'c':
                valueEnumerated = CYANA
            if value == 'x':
                valueEnumerated = XPLOR
            if value == 'p':
                valueEnumerated = PDB

            resultRow[columnLabel] = valueEnumerated
    return result


def getCASD_NMR_DBMS():
    csvFileDir = os.path.join(baseDir, 'Overview')
    relationNames = glob1(csvFileDir, "*.csv")
    relationNames = [ relationName[:-4] for relationName in relationNames]
    if not relationNames:
        nTerror('Failed to read any relation from %s' % baseDir)
    dbms = DBMS()
    dbms.readCsvRelationList(relationNames, csvFileDir)
    return dbms

def createLayOutArchive():
    #inputDir = '/Users/jd/CASD-NMR-CING/casdNmrDbDivided'
    os.chdir(inputDir)
    for entryCode in entryList[:]:
#    for entryCode in entryList[0:1]:
        ch23 = entryCode[1:3]
        for city in cityList:
            entryCodeNew = entryCode + city
            entryDir = os.path.join(ch23, entryCodeNew)
            mkdirs(entryDir)

def copyFromCasdNmr2CcpnArchive():
    #inputDir = '/Users/jd/CASD-NMR-CING/casdNmrDbDivided'
    programHoH = convertToProgram(participationTable)
    os.chdir(inputDir)
    for entryCode in entryList:
#    for entryCode in entryList[0:1]:
        ch23 = entryCode[1:3]
        for city in cityList:
#        for city in cityList[0:1]:
            entryCodeNew = entryCode + city
            programId = getDeepByKeys(programHoH, entryCode, city)
            if not (city == 'Test' or programId):
#                nTdebug("Skipping %s" % entryCodeNew)
                continue
#            else:
#                nTdebug("Looking at %s" % entryCodeNew)
#                continue # TODO disable premature stop.

            nTmessage("Working on: %s" % entryCodeNew)

            inputEntryDir = os.path.join(inputDir, ch23, entryCodeNew)
            outputEntryDir = os.path.join(dataDir, ch23, entryCodeNew)
            inputAuthorDir = os.path.join(outputEntryDir, 'Author')
            outputNijmegenDir = os.path.join(outputEntryDir, 'Nijmegen')

            if not os.path.exists(inputAuthorDir):
                mkdirs(inputAuthorDir)
            if not os.path.exists(outputNijmegenDir):
                mkdirs(outputNijmegenDir)
            # prevent junk
            patternList = "*.pdb *.upl *.aco *.tbl".split()
            fnList = globMultiplePatterns(inputEntryDir, patternList)
            for fn in fnList:
                orgFn = os.path.join(inputEntryDir, fn)
#                nTmessage("Copying from %s" % fn)
#                fnBaseName = os.path.basename(fn)
                dstFn = os.path.join(inputAuthorDir, fn)
                nTmessage("Copying from %s to %s" % (orgFn, dstFn))
                copy(orgFn, dstFn)


def redoLayOutArchiveWim():
    #inputDir = '/Users/jd/Downloads/casdNmrCcpn'
    os.chdir(inputDir)
    for entryCode in entryList[:]:
#    for entryCode in entryList[0:1]:
        ch23 = entryCode[1:3]
        entryCodeNew = entryCode + "Org"
        entryDir = os.path.join(dataDir, ch23, entryCodeNew)
        tarPath = os.path.join(entryDir, entryCodeNew + ".tgz")
#        nTmessage("Tarring from %s to %s" % (entryCodeNew,tarPath))
        nTmessage("Creating %s" % tarPath)
        if not os.path.exists(entryDir):
            mkdirs(entryDir)
        if not os.path.exists(entryCodeNew):
            os.rename(entryCode, entryCodeNew)
        myTar = tarfile.open(tarPath, mode='w:gz') # overwrites
        myTar.add(entryCodeNew)
        myTar.close()

def getMapEntryNew(entryList, cityList):
    result = {}
    for entry in entryList:
        for city in cityList:
            entryNew = entry + city
            result[entryNew] = (entry, city)
    return result

def createTodoList(entryList, cityList, programHoH):
    entryListFileName = os.path.join(baseDir, 'list', 'entry_list_todo.csv')
    newEntryList = []
    for entry in entryList:
        for city in cityList:
            entryNew = entry + city
            programId = getDeepByKeys(programHoH, entry, city)
            if programId:
                newEntryList.append(entryNew)
    writeEntryListToFile(entryListFileName, newEntryList)
# end def

def getRangesForTarget(target):
    if target not in entryList:
        nTerror("Failed to find entryOrg [%s] in entryList %s" % (target, repr(entryList)))
        return None
    index = entryList.index(target)
    return rangesPsvsList[index]

def getTargetForFullEntryName(fullEntryCode):
    """
    Split the full entry name on the last capital and return the
    part before.
    ET109AredOrg     ET109Ared
    AR3436AFrankfurt AR3436A
    """
    idxLastCapital = -1
    for idx,char in enumerate(fullEntryCode):
        if char.isupper():
            idxLastCapital = idx
    if idxLastCapital < 0:
        nTerror("Failed to find idxLastCapital in [%s]" % fullEntryCode)
        return None
    target = fullEntryCode[:idxLastCapital]
    return target

def getFullEntryNameListForTarget(target, programHoH):
    """
    Query the participation table for who all predicted the target.
    Does not include the Org.
    """
    targetList = programHoH.keys()
    targetList.sort()
    print targetList
    if target not in targetList:
        nTerror("Failed to find target %s in list %s" % (target, str(targetList)))
        return None

    mapByLab = programHoH[target]
    labList = mapByLab.keys()
    labList.sort()
    result = []
    for labId in labList:
        if not getDeepByKeysOrAttributes(mapByLab, labId ):
            continue
        result.append(target+labId)
    return result

def printCingUrls(programHoH):
    targetList = programHoH.keys()
    targetList.sort()
    print targetList
    for target in targetList:
        mapByLab = programHoH[target]
        labList = mapByLab.keys()
        labList += ['Org']
        labList.sort()
        for labId in labList:
            program = getDeepByKeysOrAttributes(mapByLab, labId )
            if labId != 'Org':
                if not program:
                    continue
            entryCode = target + labId
            ch23 = entryCode[1:3]
            print "http://nmr.cmbi.ru.nl/CASD-NMR-CING/data/%s/%s/%s.cing" % (
                    ch23, entryCode, entryCode                )


# NB TODO: reorganize this data into a class so it can be properly imported from the many other scripts.


# NBNB this code breaks whenever Geeretns home directoryis not accessible!!!
# NBNB should be replaced with functions off resultData.json
# NBNB commented out for now, but htis will break things elsewhere.
#
#NBNB TODO FIXME!!!
"""dbms = getCASD_NMR_DBMS()
sheetName = 'Overview1'
participantTable = dbms.tables['%s-Participant' % sheetName]
participationTable = dbms.tables['%s-Participation' % sheetName]
targetTable = dbms.tables['%s-Target' % sheetName]
labTable = dbms.tables['%s-LabAndCount' % sheetName]
labList = labTable.columnOrder[0]
cityList = participantTable.columnOrder[1:]
entryList = targetTable.getColumnByIdx(0)
rangesPsvsList = targetTable.getColumnByIdx(6)
programHoH = convertToProgram(participationTable)
mapEntrycodeNew2EntrycodeAndCity = getMapEntryNew(entryList, cityList)
nTdebug("Read dbms with tables: %s" % dbms.tables.keys())
"""
entryList = []
#print labList
#print programHoH
#print getRangesForTarget('ET109Ared')
#print getTargetForFullEntryName('ET109AredOrg')
#print getTargetForFullEntryName('AR3436AFrankfurt')

#printCingUrls(programHoH)

if __name__ == '__main__':
    cing.verbosity = cing.verbosityDebug
#    createTodoList(entryList, cityList,programHoH)
#    createLayOutArchive()
#    copyFromCasdNmr2CcpnArchive()
#    annotateLoop()
#    redoLayOutArchiveWim()
#    nTmessage("entryList: %s" % str(entryList))
    target = 'CGR26A'
    #result = getFullEntryNameListForTarget(target, programHoH)
    #nTmessage("result: %s" % str(result))

