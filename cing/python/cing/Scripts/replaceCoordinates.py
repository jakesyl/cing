#!/usr/bin/env python

"""
Regular use: from recoord.

Execute like:
cd /Library/WebServer/Documents/RECOORD/data/br/1brv
python -u $C/python/cing/Scripts/replaceCoordinates.py 1brv 9 \
file:///Library/WebServer/Documents/NRG-CING/data \
       /Library/WebServer/Documents/RECOORD \
. . BY_CH23_BY_ENTRY CING 1 auto 0 0 1 \
/Library/WebServer/Documents/recoord_cns_w/web/%s_cns_w.pdb ARCHIVE_RECOORD XPLOR

"""

from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Libs.network import * #@UnusedWildImport
from cing.NRG import * #@UnusedWildImport
from cing.NRG.settings import * #@UnusedWildImport
from cing.Scripts.validateEntry import * #@UnusedWildImport
from cing.core.constants import * #@UnusedWildImport


def mainReplaceCoordinatesEntry(entryId, *extraArgList):
    """inputDir may be a directory or a url. A url needs to start with http://.
    """

    fastestTest = False # DEFAULT: False
    
    htmlOnly = False # DEFAULT:: False but enable it for faster runs without some actual data.
    doWhatif = True 
    doProcheck = True
    doWattos = True
    doQueeny = True
    doTalos = True

    if fastestTest:
        htmlOnly = True
        doWhatif = False
        doProcheck = False
        doWattos = False
        doQueeny = False
        doTalos = False
    force_redo = True
    force_retrieve_input = True


    nTmessage(header)
    nTmessage(getStartMessage())

    # Sync below code with nrgCing#createToposTokens
    expectedArgumentList = """
    verbosity         inputDir             outputDir
    pdbConvention     restraintsConvention archiveType         projectType
    storeCING2db      ranges               filterTopViolations filterVasco
    singleCoreOperation inPathTemplate     archive_id          convention
    """.split()
    expectedNumberOfArguments = len(expectedArgumentList)
    if len(extraArgList) != expectedNumberOfArguments:
        nTmessage("consider updating code to include all sequential parameters: %s" % str(expectedArgumentList))
        if len(extraArgList) > expectedNumberOfArguments:
            nTerror("Got arguments: " + repr(extraArgList))
            nTerror("Failed to get expected number of arguments: %d got %d" % (
                expectedNumberOfArguments, len(extraArgList)))
            nTerror("Expected arguments: %s" % expectedArgumentList)
            return True
        # end if
    # end if
    entryCodeChar2and3 = entryId[1:3]
    cing.verbosity = int( extraArgList[IDX_VERBOSITY] )
    inputDir = extraArgList[IDX_INPUT]
    outputDir = os.path.join(extraArgList[IDX_OUTPUT], DATA_STR, entryCodeChar2and3, entryId)
    pdbConvention = extraArgList[IDX_PDB] #@UnusedVariable
    restraintsConvention = extraArgList[IDX_RESTRAINTS]
    archiveType = extraArgList[IDX_ARCHIVE] # Only used for deriving the input location not the output.
    projectType = extraArgList[IDX_PROJECT_TYPE]
    storeCING2db = stringMeansBooleanTrue( getDeepByKeysOrAttributes(extraArgList, IDX_STORE_DB))
    ranges = getDeepByKeysOrAttributes(extraArgList, IDX_RANGES)
    filterTopViolations = getDeepByKeysOrAttributes(extraArgList, IDX_FILTER_TOP)
    if filterTopViolations:
        filterTopViolations = int(filterTopViolations) # change '0' to 0
    filterVasco = getDeepByKeysOrAttributes(extraArgList, IDX_FILTER_VASCO)
    if filterVasco:
        filterVasco = int(filterVasco)
    else:
        filterVasco = 1 # Default should be True
    singleCoreOperation = getDeepByKeysOrAttributes(extraArgList, IDX_SINGLE_CORE_OPERATION )
    inPathTemplate = getDeepByKeysOrAttributes(extraArgList, IDX_SINGLE_CORE_OPERATION + 1 )    
    archive_id = getDeepByKeysOrAttributes(extraArgList, IDX_SINGLE_CORE_OPERATION + 2 )    
    convention = getDeepByKeysOrAttributes(extraArgList, IDX_SINGLE_CORE_OPERATION + 3 )        
    
    if archiveType == ARCHIVE_TYPE_FLAT:
        pass # default
    elif archiveType == ARCHIVE_TYPE_BY_ENTRY:
        inputDir = os.path.join(inputDir, entryId)
    elif archiveType == ARCHIVE_TYPE_BY_CH23:
        inputDir = os.path.join(inputDir, entryCodeChar2and3)
    elif archiveType == ARCHIVE_TYPE_BY_CH23_BY_ENTRY:
        inputDir = os.path.join(inputDir, entryCodeChar2and3, entryId)

    isRemoteOutputDir = False
    if '@' in outputDir:
        isRemoteOutputDir = True
#    vc = vCing('.') # argument is a fake master_ssh_url not needed here.

    nTdebug("Using program arguments:")
    nTdebug("inputDir:             %s" % inputDir)
    nTdebug("outputDir:            %s" % outputDir)
    nTdebug("pdbConvention:        %s" % pdbConvention)
    nTdebug("restraintsConvention: %s" % restraintsConvention)
    nTdebug("archiveType:          %s" % archiveType)
    nTdebug("projectType:          %s" % projectType)
    nTdebug("storeCING2db:         %s" % storeCING2db)
    nTdebug("ranges:               %s" % ranges)
    nTdebug("filterTopViolations:  %s" % filterTopViolations)
    nTdebug("filterVasco:          %s" % filterVasco)
    nTdebug("singleCoreOperation:  %s" % singleCoreOperation)
    nTdebug("inPathTemplate:       %s" % inPathTemplate)
#    nTdebug("inPath:               %s" % inPath)
    nTdebug("")
    nTdebug("Using derived settings:")
    nTdebug("isRemoteOutputDir:    %s" % isRemoteOutputDir)
    
    # For NMR_REDO required as most efficient.
    if singleCoreOperation: 
        setToSingleCoreOperation()
    
    # presume the directory still needs to be created.
    cingEntryDir = entryId + ".cing"

    if os.path.isdir(cingEntryDir):
        if force_redo:
            nTmessage("Enforcing a redo")
            rmtree(cingEntryDir)
        else:
            mainIndexFile = os.path.join(cingEntryDir, "index.html")
            isDone = os.path.isfile(mainIndexFile)
            if isDone:
                nTmessage("SKIPPING ENTRY ALREADY DONE")
                return
            nTmessage("REDOING BECAUSE VALIDATION CONSIDERED NOT DONE.")
            rmtree(cingEntryDir)
        # end if.
    # end if.

    if isRemoteOutputDir:
        os.chdir(cingDirTmp)
    else:
        mkdirs(outputDir)
        os.chdir(outputDir)

    project = Project(entryId)
    if project.removeFromDisk():
        nTerror("Failed to remove existing project (if present)")
        return True
    # end if.

    formatFileName = '%s.tgz'
    if projectType == PROJECT_TYPE_CING:
        formatFileName = '%s.cing.tgz'
    elif projectType == PROJECT_TYPE_PDB:
        formatFileName = 'pdb%s.ent.gz'
    fileNameTgz = formatFileName % entryId

#    nTdebug("fileNameTgz: %s" % fileNameTgz)
    allowedInputProtocolList = 'http file ssh'.split()
    inputProtocal = string.split( inputDir, ':' )[0]
    if inputProtocal in allowedInputProtocolList:
        stillToRetrieve = False
        if os.path.exists(fileNameTgz):
            if force_retrieve_input:
                os.unlink(fileNameTgz)
                stillToRetrieve = True
            # end if
        else:
            stillToRetrieve = True
        # end if
        if stillToRetrieve:
            retrieveTgzFromUrl(entryId, inputDir, archiveType=archiveType, formatFileName=formatFileName)
        # end if
        if not os.path.exists(fileNameTgz):
            nTerror("Tgz should already have been present skipping entry")
            return
        # end if
    else:
        nTdebug("Entry not retrieved which might be normal in some situations.")
    # end if.

    if projectType == PROJECT_TYPE_CING:
        # Needs to be copied because the open method doesn't take a directory argument..
#        fullFileNameTgz = os.path.join(inputDir, fileNameTgz)
#        shutil.copy(fullFileNameTgz, '.')
        project = Project.open(entryId, status='old')
        if not project:
            nTerror("Failed to init old project")
            return True
    else:
        nTerror("Expected a CING project.")
        return True
        # end if
    # end if

####> MAIN UTILITY HERE    
    name = entryId + "_recoord"
    inPath = inPathTemplate % entryId    
    if project.molecule.replaceCoordinatesByPdb( inPath, name = name, convention=convention ):  
        nTerror("Failed replaceCoordinatesByPdb.")
        return True
    # end if          
    
    if ranges != None:
        project.molecule.setRanges(ranges)
    project.molecule.superpose(ranges=ranges)

    if 1: # DEFAULT 1?
        project.save()
    if project.validate(htmlOnly=htmlOnly, ranges=ranges, doProcheck=doProcheck, doWhatif=doWhatif,
            doWattos=doWattos, doQueeny = doQueeny, doTalos=doTalos, filterVasco = filterVasco ):
        nTerror("Failed to validate project read")
        return True
    # end if filterVasco

    project.save()
    
    if storeCING2db:
        try:
            if doStoreCING2db( entryId, archive_id, project=project):
                nTerror("Failed to store CING project's data to DB but continuing.")
        except:
            nTtracebackError()
            nTerror("Failed to store CING project's data due to above traceback error.")
    # end if

    
# end def

if __name__ == "__main__":
    cing.verbosity = verbosityDebug
#        sys.exit(1) # can't be used in forkoff api
    try:
        status = mainReplaceCoordinatesEntry(*sys.argv[1:])
    finally:
        nTmessage(getStopMessage(cing.starttime))
