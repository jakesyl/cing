"""
Author: Jurgen F. Doreleijers

python -u $CINGROOT/python/cing/NRG/PDBEntryLists.py
"""
#from ccp.format.nmrStar.projectIO import NmrStarProjectFile
from cing import cingDirData
from cing import cingPythonDir
from cing.Libs.DBMS import DBMS
from cing.Libs.DBMS import getRelationFromCsvFile
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.NRG.nrgCingRdb import getPdbIdList
from cing.NRG.settings import matchBmrbPdbDir
import urllib
import urllib2

urlDB2 = "http://restraintsgrid.bmrb.wisc.edu/servlet_data/viavia/mr_mysql_backup/"
#urlDB2 = "http://restraintsgrid.bmrb.wisc.edu/servlet_data/viavia/mr_mysql_backupAn_2009-08-03/"
#urlDB2 = "http://nmr.cmbi.ru.nl/~jd/viavia/mr_mysql_backup/"

#ocaUrl = "http://oca.ebi.ac.uk/oca-bin/ocaids"
ocaUrl = "http://www.ebi.ac.uk/msd-srv/oca/oca-bin/ocaids"
bmrbUrl ="http://www.bmrb.wisc.edu/ftp/pub/bmrb/relational_tables/nmr-star2.1/depsindb.csv.gz"

testingLocally = False
if testingLocally:
    urlDB2 = "http://localhost/servlet_data/viavia/mr_mysql_backup/" # For fastest develop.
    ocaUrl = "http://localhost/oca" # For fastest develop.

matchBmrbPdbDataDir = "data/NRG/bmrbPdbMatch" # wrt $CINGROOT
matchBmrbPdbTable = 'newMany2OneTable'

def getEntryListFromCsvFile(urlLocation):
    result = []
    ##108d
    ##149d
    r1 = urllib.urlopen(urlLocation)
    data = r1.read()
    r1.close()
    dataLines = data.split("\n")
    for dataLine in dataLines:
        if dataLine:
            (entryCode,) = dataLine.split()
            result.append(entryCode)
    return result

def getBmrbLinks():
    """ Returns None for failure
    Returns matches_many2one hash.
    """
    dbms = DBMS()
#    matchBmrbPdbDataDirLocal = os.path.join(cingRoot, matchBmrbPdbDataDir) # Needs to change to live resource as well.
    matchBmrbPdbDataDirLocal = matchBmrbPdbDir
    dbms.readCsvRelationList([ matchBmrbPdbTable ], matchBmrbPdbDataDirLocal)
    mTable = dbms.tables[matchBmrbPdbTable]
#    nTmessage("mTable:\n%s" % mTable.__str__(show_rows=False))
    matches_many2one = mTable.getHash(useSingleValueOfColumn=1) # hashes by first column to the next by default already.
#    nTmessage("Found %s matches from PDB to BMRB" % len(matches_many2one))
    return matches_many2one

def getBmrbNmrGridEntries():
    result = []
    urlLocation = urlDB2 + "/entry.txt"
    #  nTdebug("Loading from %s" % urlLocation)
    ##4583    \N    108d    \N    \N
    ##4584    \N    149d    \N    \N
    r1 = urllib.urlopen(urlLocation)
    data = r1.read()
    r1.close()
    dataLines = data.split("\n")
    for dataLine in dataLines:
        if dataLine:
            # b is for bogus/unused
            (_entryId, _bmrbId, pdbCode, _in_recoord, _in_dress) = dataLine.split()
            result.append(pdbCode)
    result.sort()
    return result

def getDOCRfREDDone():
    result = []
    urlLocation = urlDB2 + "/mrfile.txt"
    ##61458    7567    4-filtered-FRED    2gov    2006-05-11
    ##61459    7567    4-filtered-FRED    2gov    2006-05-11
    r1 = urllib.urlopen(urlLocation)
    data = r1.read()
    r1.close()
    dataLines = data.split("\n")
    for dataLine in dataLines:
        if dataLine:
            (_mrfile_id, _entry_id, stage, pdbCode, _date_modified) = dataLine.split()
            if stage == "4-filtered-FRED":
                if pdbCode not in result:
                    result.append(pdbCode)
    result.sort()
    return result

def getBmrbNmrGridEntriesDOCRDone():
    badDocrEntryList = '1lcc 1lcd'.split() # Disable this manual correction when NRG issssue 272 is fixed.
    # See CING issue 266
    #  badDocrEntryList = []
    result = []
    urlLocation = urlDB2 + "/mrfile.txt"
    ##61458    7567    4-filtered-FRED    2gov    2006-05-11
    ##61459    7567    4-filtered-FRED    2gov    2006-05-11
    r1 = urllib.urlopen(urlLocation)
    data = r1.read()
    r1.close()
    dataLines = data.split("\n")
    for dataLine in dataLines:
        if not dataLine:
            continue
        (_mrfile_id, _entry_id, stage, pdbCode, _date_modified) = dataLine.split()
        if stage == "3-converted-DOCR":
            if pdbCode in badDocrEntryList:
                continue
            if pdbCode in result:
                continue
            result.append(pdbCode)
        # end if
    # end for
    result.sort()
    return result

def writeEntryListToFile(fileName, entryList):
    "Returns True on failure"
    csvText = toCsv(entryList)
#    nTdebug("entryList: %s" % str(entryList))
    if not csvText:
        nTerror("Failed to get CSV for %s" % entryList)
        return True
    writeTextToFile(fileName, csvText)

def readEntryListFromFile(fileName, headerCount=0):
    """
    Throws exception on failure or None on error
    Will only use first column's values
    """
    txt = readTextFromFile(fileName)
    if not txt:
        nTerror("Failed to readLinesFromFile %s" % fileName)
        return None
    result = []
    for line in txt.split('\n'):
        val = line
        if line.count(','):
            val = line.split(',')[0]
        elif line.count(' '):
            val = line.split(' ')[0]
        result.append(val)
    if headerCount:
        result = result[headerCount:]
    return result
# end def

def getBmrbEntries():
    'Return None on error.'
    r1 = urllib.urlopen(bmrbUrl)
    data = r1.read()
    fileNameGz = getFileName(bmrbUrl)
    writeDataToFile(fileNameGz, data)
    fileName = fileNameGz[:-3] # remove .gz
    gunzip(fileNameGz, outputFileName=fileName, removeOriginal=True)
    bmrbDepRelation = getRelationFromCsvFile( fileName, containsHeaderRow=0 )
    if not bmrbDepRelation:
        nTerror('No relation read from CSV file: %s' % fileName )
        return None
    bmrbDateList = bmrbDepRelation.getColumnByIdx(0)
    bmrbIdList = [ int(bmrbData[5:]) for bmrbData in bmrbDateList ]
    nTmessage("Read %s BMRB entries from DB dump" % len(bmrbIdList))
    bmrbIdList.sort()
    return bmrbIdList
# end def

def getPdbEntries(onlyNmr=False, mustHaveExperimentalNmrData=False, onlySolidState=False):
    """Includes solution and solid state NMR if onlyNMR is chosen
    """
#    if True: # Default False; used for not bothering sites.
#        return ['1a4d', '2d6p', '2e7r', '3ejo']

    dir_name = os.path.join(cingPythonDir, 'cing', 'NRG', DATA_STR)
    if onlySolidState:
        inputFile = os.path.join(dir_name, 'RESTqueryPDB_NMR_solid.xml')
    elif onlyNmr:
        if mustHaveExperimentalNmrData:
            inputFile = os.path.join(dir_name, 'RESTqueryPDB_NMR_exp.xml')
        else:
            inputFile = os.path.join(dir_name, 'RESTqueryPDB_NMR.xml')
    else:
        if mustHaveExperimentalNmrData:
            inputFile = os.path.join(dir_name, 'RESTqueryPDB_exp.xml')
#            nTcodeerror("Can't query for onlyNmr = True AND mustHaveExperimentalNmrData = True")
#            return
        else:
            inputFile = os.path.join(dir_name, 'RESTqueryPDB.xml')

    rpcUrl = 'http://www.rcsb.org/pdb/rest/search'
    queryText = open(inputFile, 'r').read()
#    nTdebug("queryText:\n%s" % queryText)
#    nTdebug("querying...")
    req = urllib2.Request(url=rpcUrl, data=queryText)
    f = urllib2.urlopen(req)
    result = []
    for _i, record in enumerate(f.readlines()):
        entry_code = record.rstrip().lower()
        if not is_pdb_code(entry_code):
#            nTwarning("In %s found an invalid entry code: %s from record (%s) '%s'" % (getCallerName(), str(entry_code), i, record)) 
# Reported to Wolfgang on April 24, 2011.
            continue
        result.append( entry_code )
    if not result:
        nTerror("Failed to read file from server")
        return
#    nTdebug("Done successfully.")
    return result


def getPdbEntriesOca(onlyNmr=False):
    """Not really used anymore"""
    result = []
    urlLocation = ocaUrl + "?dat=dep&ex=any&m=du"
    if testingLocally:
        urlLocation = ocaUrl + "/ocaidsPDB"
    if onlyNmr:
        urlLocation = ocaUrl + "?dat=dep&ex=nmr&m=du"
        if testingLocally:
            urlLocation = ocaUrl + "/ocaidsPDB-NMR"

## OCA database search on: Wed Dec  3 10:18:07 2008
## Query: ex=any&m=du
## Hits: 55841 (search time 0 sec)
#100D     Crystal The Highly Distorted Chimeric Deca... Ban                1.90
#101D     Refinement Of Netropsin Bound To DNA: Bias... Goodsell           2.25
    r1 = urllib.urlopen(urlLocation)
    data = r1.read()
    r1.close()
    
    dataLines = data.split("\n")
    for dataLine in dataLines:
        if dataLine:
            if not dataLine[0].isdigit():
                # skipping html and header.
                continue
            items = dataLine.split()
            if items:
                pdbCode = items[0]
                pdbCode = pdbCode.lower()
                result.append(pdbCode)
            # end if
        # end if
    # end for
    result.sort()
    return result

def getBmrbCsCounts():
    dbms = DBMS()
    bmrbCountTableName = 'BMRB_CS_counts'
    dbms.readCsvRelationList([bmrbCountTableName], os.path.join(cingDirData, 'NRG'))
    bmrbCountTable = dbms.tables[ bmrbCountTableName ]
    bmrbCountTable.convertColumn(0) # default is integer data type converting the read strings
    bmrbCountTable.convertColumn(2)
    bmrbCountTableProper = bmrbCountTable.toTable()
#        nTdebug("Found table: %r" % bmrbCountTableProper)
    bmrbCountMap = NTdict()
#        idxColumnKeyList = [0, 1, 2]
    idxColumnKeyList = []
    bmrbCountMap.appendFromTableGeneric(bmrbCountTableProper, *idxColumnKeyList)

    return bmrbCountMap

def findMissingPdbjEntries():
    'Return True if entries are missing in pdbj wrt rcsb-pdb.'
    pdbRcsbEntryList = getPdbEntries()
    NTmessage("Found RCSB PDB entries count: %s" % len(pdbRcsbEntryList))
    host = 'localhost'
    if True: # DEFAULT True
        host = 'nmr.cmbi.ru.nl'
    pdbjEntryList = getPdbIdList(fromCing=False, host=host)
    if not pdbRcsbEntryList:
        NTerror("Failed to find any entry in RCSB-PDB")
        return True
    if not pdbjEntryList:
        NTerror("Failed to find any entry in pdbj's")
        return True
    NTmessage("Found PDBj entries count: %s" % len(pdbjEntryList))
    pdbRcsbEntryNtList = NTlist(*pdbRcsbEntryList)
    pdbjEntryNtList = NTlist(*pdbjEntryList)
    pdbjMissingEntryNtList = pdbRcsbEntryNtList.difference(pdbjEntryNtList)
    NTmessage("Found PDBj missing entries count: %s %s" % (len(pdbjMissingEntryNtList), pdbjMissingEntryNtList))
    pdbRcsbMissingEntryNtList = pdbjEntryNtList.difference(pdbRcsbEntryNtList)
    NTmessage("Found RCSB-PDB missing entries count: %s %s" % (len(pdbRcsbMissingEntryNtList), pdbRcsbMissingEntryNtList))
# end def
    
if __name__ == '__main__':
#    cing.verbosity = cing.verbosityDebug
    findMissingPdbjEntries()
