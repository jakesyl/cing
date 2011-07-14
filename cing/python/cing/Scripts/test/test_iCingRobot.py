"""
Unit test execute as:
python -u $CINGROOT/python/cing/Scripts/test/test_iCingRobot.py
"""
from cing import cingDirTestsData #@UnusedImport
from cing import cingDirTmp
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Scripts.iCingRobot import * #@UnusedWildImport
from unittest import TestCase
import unittest

class AllChecks(TestCase):

    def test_iCingRobot(self):
        cingDirTmpTest = os.path.join( cingDirTmp, getCallerName() )
        mkdirs( cingDirTmpTest )
        self.failIf(os.chdir(cingDirTmpTest), msg =
            "Failed to change to test directory for files: " + cingDirTmpTest)

        if not cing.isInternetConnected():
            nTdebug("Skipping %s because cing is not connected to the internet." % getCallerName())
            return
#        url = 'http://restraintsgrid.bmrb.wisc.edu/servlet_data/NRG_ccpn_tmp'
    #    nTwarning("Expect errors without a server up and running.")
        nTmessage("Firing up the iCing robot; aka example interface to CING")

        ## queries possible; do one at a time going down the list.
        ## After the run is started the status will let you know if the run is finished
        ## The log will show what the server is doing at any one time.
        doSave  = 0 # Upload to iCing and show derived urls
        doRun   = 0 # Start the run in Nijmegen
        doStatus= 1 # Find out if the run finished
        doLog   = 0 # Get the next piece of log file (may be empty)
        doPname = 0 # Get the project name back. This is the entryId below.
        doPurge = 0 # Remove data from server again.

        # User id should be a short id (<without any special chars.)
    #    user_id = os.getenv("USER", "UnknownUser")
        user_id = "iCingRobot"
        access_key = "123456"
#        access_key = getRandomKey() # Use a different one in a production setup.

        entryId = '1brv' # 68K, smallest for quick testing.
    #    entryId = 'gb1' # only included in xplor variant as single model.

        # Select one of the types by uncommenting it
        inputFileType = 'CCPN'
    #    inputFileType = 'PDB'
    #    inputFileType = 'XPLOR'

        ccpnFile = os.path.join(cingDirTestsData, "ccpn", entryId + ".tgz")
        pdbFile = os.path.join(cingDirTestsData, "pdb", entryId, 'pdb' + entryId + ".ent")
        xplorFile = os.path.join(cingDirTestsData, "xplor", entryId, entryId + ".pdb")

        inputFile = ccpnFile
        if inputFileType == 'PDB':
            inputFile = pdbFile
        elif inputFileType == 'XPLOR':
            inputFile = xplorFile


    #    rpcUrl=DEFAULT_URL+"icing/serv/iCingServlet"
        rpcUrl=DEFAULT_URL+DEFAULT_RPC_PORT+'/'+DEFAULT_URL_PATH+"/serv/iCingServlet"
        nTdebug("Using rpc at: %s" % rpcUrl )
        credentials = [(FORM_USER_ID, user_id), (FORM_ACCESS_KEY, access_key)]
        nTdebug("With credentials: %s" % credentials )

    ##############################################################################################################

        if doSave:
            data = credentials + [(FORM_ACTION,FORM_ACTION_SAVE),]
            nTdebug("Getting file contents from disk")
            fileObj = open(inputFile, 'rb')
            files = [( FORM_UPLOAD_FILE_BASE, inputFile, fileObj.read() ),]

            nTdebug("Sending contents to rpc")
            result = sendRequest(rpcUrl, data, files)
            if not result:
                nTerror("Failed to save file to server")
            else:
                print "result of save request: %s" % result
                urls = getResultUrls(credentials, entryId, DEFAULT_URL)
                print "Base URL", urls[0]
                print "Results URL:", urls[1]
                print "Log URL:", urls[2]
                print "Zip URL:", urls[3]


    ##############################################################################################################
        files = None

        if doRun:
            data = credentials + [(FORM_ACTION,FORM_ACTION_RUN),]
            nTmessage( str(sendRequest(rpcUrl, data, files) ))

        if doStatus:
            data = credentials + [(FORM_ACTION,FORM_ACTION_STATUS),]
            nTmessage( str(sendRequest(rpcUrl, data, files) ))

        if doLog:
            data = credentials + [(FORM_ACTION,FORM_ACTION_LOG),]
            nTmessage( str(sendRequest(rpcUrl, data, files) ))

        if doPname:
            data = credentials + [(FORM_ACTION,FORM_ACTION_PROJECT_NAME),]
            nTmessage( str(sendRequest(rpcUrl, data, files) ))

        if doPurge:
            data = credentials + [(FORM_ACTION,FORM_ACTION_PURGE),]
            nTmessage( str(sendRequest(rpcUrl, data, files) ))

if __name__ == "__main__":
    cing.verbosity = verbosityDebug
    unittest.main()
