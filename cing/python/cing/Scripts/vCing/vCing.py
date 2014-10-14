#!/usr/bin/env python
"""
This is file: $C/python/cing/Scripts/vCing/vCing.py
Script for running CING on a bunch (8?) of cores.
Do NOT run from $CINGROOT/scripts/vcing/startVC.csh
Use:
$CINGROOT/python/cing/Scripts/vCing/vCing.py runSlaveThread
$CINGROOT/python/cing/Scripts/vCing/vCing.py runSlave
$CINGROOT/python/cing/Scripts/vCing/vCing.py addTokenListToTopos $D/NRG-CING/token_list_todo.txt
For killing use the shootall script. 
Author: Jurgen F. Doreleijers
Thu Oct 14 23:56:36 CEST 2010
"""
from cing import cingDirScripts
from cing import cingDirTmp
from cing import cingPythonDir
from cing import cingRoot
from cing import header
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Libs.forkoff import * #@UnusedWildImport
from cing.Libs.network import * #@UnusedWildImport
from cing.NRG import * #@UnusedWildImport
from cing.Scripts.vCing.Utils import prepareMaster
from cing.main import getStartMessage
from cing.main import getStopMessage
from datetime import datetime

# Will be overridden by local settings.
master_ssh_url_local    = 'i@nmr'
master_d_local          = '/Volumes/joe/D'
pool_postfix_local      = 'joe'
try:
    from cing.Scripts.vCing.localConstants import * #@UnusedWildImport # pylint: disable=E0611
except:
    pass
#    NTtracebackError() # codes below are nonsense.
#    pool_postfix = 'invalidPostFix'
#    master_ssh_url = 'i@vc'

cingDirNRG = os.path.join(cingPythonDir, 'cing', 'NRG')
cingDirVC = os.path.join(cingDirScripts, 'vCing')

VALIDATE_ENTRY_NRG_STR = 'validateEntryNrg'
REFINE_ENTRY_STR       = 'refineEntryNrg'
TEST_CING_STR          = 'testCing'

# Possible targets are keyed from token to provide some security and brevity.
cmdDict = {
#           VALIDATE_ENTRY_NRG_STR: os.path.join(cingDirNRG, 'validateEntryForNrgByVC.py'),
           VALIDATE_ENTRY_NRG_STR: os.path.join(cingDirScripts, 'validateEntry.py'),
           REFINE_ENTRY_STR:       os.path.join(cingDirScripts, 'refineEntry.py'),
           TEST_CING_STR:          os.path.join(cingDirVC, 'test', 'cingByVCtest.py'),
            }

class Vcing(Lister):
    BAD_COMMAND_TOKEN_STR = 'bad_command_token'
    COMMAND_FAILED_STR = 'command_failed'
    COMMAND_FINISHED_STR = 'command_finished'
    NO_TOKEN_CONTENT_STR = 'None'

    LEVEL_ERROR_STR = 'ERROR'
    LEVEL_MSG_STR = 'MSG'
    LEVEL_WARNING_STR = 'WARNING'

    MASTER_TARGET_LOG = 'log' # Payload log
    MASTER_TARGET_LOG2 = 'log2' # For slave's log (just a one or two lines
    MASTER_TARGET_UNF = 'unfinished'
    MASTER_TARGET_RESULT = 'result' # Payload result

    def __init__(self, master_ssh_url=None, master_d=None, cmdDict='', toposPool = None, max_time_to_wait_per_job = 60 * 60 * 6):
        Lister.__init__(self)
        self.toposDir = os.path.join(cingRoot, "scripts", "vcing", "topos")
        self.toposRealm = 'https://topos.grid.sara.nl/4.1/'
        self.toposPool = 'vCing' + pool_postfix_local
        if toposPool:
            self.toposPool = toposPool
        # end if
# Interface found at NBIC's https://gforge.nbic.nl/plugins/scmsvn/viewcvs.php/clients/trunk/python/?root=topos
#        self.toposCmd = toposcmd(realm=self.toposRealm, pool=self.toposPool)
        self.toposProg = os.path.join(self.toposDir, "topos")
        self.toposProgCreateTokens = os.path.join(self.toposDir, "createTokens")

        self.master_ssh_url = master_ssh_url_local
        if master_ssh_url:
            self.master_ssh_url = master_ssh_url
        # end if
        self.master_d = master_d_local
        if master_d:
            self.master_d = master_d
        # end if
        # Don't change the below without modifying the settings in:
        #  $C/python/cing/Scripts/vCing/localConstants.py
        #  $C/scripts/vcing/localConstants.csh
        self.master_target_dir = self.master_d + '/tmp/vCingSlave/' + self.toposPool
        self.master_target_url = self.master_ssh_url + ':' + self.master_target_dir
#        self.MASTER_SOURCE_SDIR = self.MASTER_D_URL + '/tmp/vCingSlave/' + self.toposPool
        self.max_time_to_wait = 365 * 24 * 60 * 60                    # a year in seconds
#        self.max_time_to_wait_per_job = max_time_to_wait_per_job      # 2p80 took the longest: 5.2 hours.
        self.max_time_to_wait_per_job = 86400*2 # two days
        self.time_sleep_when_no_token = 5 * 60                        # 5 minutes
        self.lockTimeOut = 5 * 60                                     # 5 minutes
    # end def

    def cleanMaster(self):
        return self.prepareMaster(doClean=True)
    # end def

    def prepareMaster(self, doClean=False):
        """
        Return True on error.
        Moved out of this setup so it can be run with a very limited CING install on gb-ui-kun.els.sara.nl
        """
        return prepareMaster(master_target_dir=self.master_target_dir, doClean=doClean)
    # end def


    def addTokenListToTopos(self, fileName):
        cmdTopos = ' '.join([self.toposProg, 'createTokensFromLinesInFile', self.toposPool, fileName])
        nTdebug("In addTokenListToTopos doing [%s]" % cmdTopos)
        status, result = commands.getstatusoutput(cmdTopos)
        nTdebug("In addTokenListToTopos got status: %s and result (if any) [%s]" % (status, result))
        return status
    # end def

    def refreshLock(self, lockname, lockTimeOut):
        cmdTopos = ' '.join([self.toposProg, 'refreshLock', self.toposPool, lockname, repr(lockTimeOut)])
        nTdebug("In refreshLock doing [%s]" % cmdTopos)
        status, result = commands.getstatusoutput(cmdTopos)
        nTdebug("In refreshLock got status: %s and result (if any) [%s]" % (status, result))
        return status
    # end def

    def keepLockFresh(self, lockname, lockTimeOut):
        maxSleapingTime = self.max_time_to_wait_per_job + 100 
        # process will be killed outside first so we give it some extra time here for it to be reaped.
        sleepTime = lockTimeOut / 2 + 1
        sleptTime = 0
        while True:
            nTdebug("refreshLock will now sleep for: %s" % sleepTime)
            time.sleep(sleepTime)
            sleptTime += sleepTime
            nTdebug("keepLockFresh doing a refreshLock")
            #nTdebug("Time is %s" % str(datetime.now()))
            status = self.refreshLock(lockname, lockTimeOut)
#            nTdebug("In keepLockFresh got status: %s and result (if any) [%s]" % (status, result))
            if status:
                nTmessage("In keepLockFresh got status: %s. This indicates that the token process finished." % status)
                nTdebug("Time is %s" % str(datetime.now()))
                break
            # end if
            if sleptTime > maxSleapingTime:
                nTerror("refreshLock should have exited by itself but apparently not after: %s" % sleptTime)
                nTdebug("Time is %s" % str(datetime.now()))
                break
            # end if
        # end while
    # end def

    def nextTokenWithLock(self, lockTimeOut):
        "Returns status 1 for on error"
        cmdTopos = ' '.join([self.toposProg, 'nextTokenWithLock', self.toposPool, repr(lockTimeOut)])
        nTdebug("In nextTokenWithLock doing [%s]" % cmdTopos)
        status, tokeninfo = commands.getstatusoutput(cmdTopos)
        if status:
            return [status, None, None]
        # end if
        resultList = tokeninfo.split()
        if len(resultList) != 2:
            nTerror("Failed to find tokeninfo as expected with 2 parts from: %s" % tokeninfo)
            return None
        # end if        
        return [status] + resultList
    # end def

    def getToken(self, token):
        """"
        Returns None for on error and tokenContent on success.
        I don't understand why the topos getToken call fails every now and then but when retried it seems to work fine.
        """
        cmdTopos = ' '.join([self.toposProg, 'getToken', self.toposPool, token])
        ntries = 3
        sleepTime = 10

        i = 0
        while i < ntries:
            i += 1
            nTdebug("In getToken doing [%s]" % cmdTopos)
            status, tokenContent = commands.getstatusoutput(cmdTopos)
            if not status:
                nTdebug("Got token content on try: %d: [%s]" % (i, tokenContent))
                return tokenContent
            # end if
            nTwarning("Failed to get token on try: %d with output message: [%s]" % (i, tokenContent))
            # end if
            nTdebug("In getToken sleeping %s" % sleepTime)
            time.sleep(sleepTime)
        # end while
        nTerror("Giving up trying to get token after %d tries" % ntries)
        return None
    # end def

    def deleteToken(self, token):
        "Returns status 1 for on error"
        cmdTopos = ' '.join([self.toposProg, 'deleteToken', self.toposPool, token])
        nTdebug("In deleteToken doing [%s]" % cmdTopos)
        status, result = commands.getstatusoutput(cmdTopos)
        if status:
            nTerror("Failed to deleteToken status: %s with result %s" % (status, result))
        # end if
        return status
    # end def

    def deleteLock(self, lock):
        "Returns status 1 for on error"
        cmdTopos = ' '.join([self.toposProg, 'deleteLock', self.toposPool, lock])
        nTdebug("In deleteLock doing [%s]" % cmdTopos)
        status, result = commands.getstatusoutput(cmdTopos)
        if status:
            nTerror("Failed to deleteLock status: %s with result %s" % (status, result))
        # end if
        return status
    # end def

    def getLogFileName(self, token, tokenContent):
        tokenContentList = tokenContent.split()
        if len(tokenContentList) > 2:
            tokenContentList = tokenContentList[:2]
        # end if
        logFile = '_'.join([token] + tokenContentList + [getRandomKey()]) + '.log'
        return logFile
    # end def

    def getPrefixForLevel(self, level_id):
        prefix = ''
        if level_id == self.LEVEL_ERROR_STR:
            prefix = prefixError
        elif level_id == self.LEVEL_WARNING_STR:
            prefix = prefixWarning
        # end if
        return prefix
    # end def

    def slaveEndAndLog(self, level_id, token, tokenContent, msg):
        "Returns True for on error"
        time.sleep(2)
        nTdebug("Ending with slave %s for token: %s containing %s with message: %s" % (level_id, token, tokenContent, msg))
        status = self.deleteToken(token)
        if status:
            nTerror("Failed in slaveEndAndLog to deleteToken with status: %s" % status)
        # end if
        logFile = self.getLogFileName(token, tokenContent)

        prefix = self.getPrefixForLevel(level_id)

        writeTextToFile(logFile, prefix + msg)
        targetUrl = '/'.join([self.master_target_url, self.MASTER_TARGET_LOG2])
        if putFileBySsh(logFile, targetUrl):
            nTerror("Failed to putFileBySsh with status: %s" % status)
            return True
        # end if
    # end def

    def runSlaveThread(self):
        """
        Slave thread code should always send a log file (to log2) to the master back if trying a
        token. See getLogFileName for encoding of it.
        """
        nTmessage("Now starting runSlaveThread")
        if False:
            time.sleep(self.max_time_to_wait)
        # end if
        p = Process(max_time_to_wait_kill=self.max_time_to_wait)

        os.chdir(cingDirTmp)

        maxTokenToTry = 999*999*999*999 # default
#        maxTokenToTry = 1
        iterationsTried = 0
        tokensTried = 0
        tokensFinished = 0
        while tokensTried < maxTokenToTry: # for debug limit to certain number of tries.
            iterationsTried += 1
            time.sleep(2)
            exitCode, token, tokenLock = self.nextTokenWithLock(self.lockTimeOut)
            if exitCode:
                nTmessage("Nothing returned by self.nextTokenWithLock(). Sleeping for 5 minutes and trying again.")
                #nTdebug("Time is %s" % str(datetime.now()))
                time.sleep(self.time_sleep_when_no_token)
                continue
            # end if            
            time.sleep(2)
            pid = p.process_fork(self.keepLockFresh, [tokenLock, self.lockTimeOut])
            nTdebug("Created a background process [%s] keeping the lock" % pid)
            nTdebug("Time is %s" % str(datetime.now()))
            time.sleep(2)
            tokenContent = self.getToken(token)
            if tokenContent == None:
                tokenContent = self.NO_TOKEN_CONTENT_STR
                msg = "Failed to get token content. Deleting token."
                nTerror(msg)
                nTdebug("Time is %s" % str(datetime.now()))
                self.slaveEndAndLog(self.LEVEL_ERROR_STR, token, tokenContent, msg)
                continue
            # end if
            tokensTried += 1
            nTmessage("In %d/%d/%d (finished/total/iterations) got token %s with lock: %s" % (tokensFinished, 
                        tokensTried, iterationsTried, token, tokenLock))

            # The script needs itself to send the results all included.
            nTmessage("Found tokenContent: %s" % tokenContent)
            nTdebug("Time is %s" % str(datetime.now()))  
            tokenPartList = tokenContent.split()
            cmdToken = tokenPartList[0]
            parTokenListStr = ' '.join(tokenPartList[1:])
            if not cmdDict.has_key(cmdToken):
                self.slaveEndAndLog(self.LEVEL_ERROR_STR, token, tokenContent, self.BAD_COMMAND_TOKEN_STR)
                continue
            # end if
            cmdReal = cmdDict[cmdToken]
            log_file_name = self.getLogFileName(token, tokenContent)
#            cmdProgram = ExecuteProgram(cmdReal, rootPath=cingDirTmp, redirectOutputToFile=log_file_name)
            cmdProgram = 'cd %s; %s %s > %s 2>&1' % (cingDirTmp, cmdReal, parTokenListStr, log_file_name)
            nTmessage("Running payload %s" % cmdProgram)
            nTdebug("Time is %s" % str(datetime.now()))
            job = (do_cmd, (cmdProgram,))
            job_list = [ job ]
            f = ForkOff(max_time_to_wait=self.max_time_to_wait_per_job)
            done_entry_list = f.forkoff_start(job_list, delay_between_submitting_jobs=1)
            cmdExitCode = 1
            if done_entry_list: # length will be jobs done successfully.
                cmdExitCode = 0
            # end if
            fs = os.path.getsize(log_file_name)
            nTmessage("Payload returned with status: %s and log file size %s" % (cmdExitCode, fs))
            nTdebug("Time is %s" % str(datetime.now()))
            targetUrl = '/'.join([self.master_target_url, self.MASTER_TARGET_LOG])
            if putFileBySsh(log_file_name, targetUrl):
                nTerror("In runSlaveThread failed putFileBySsh")
                nTdebug("Time is %s" % str(datetime.now()))
            # end if
            if cmdExitCode:
                nTerror("Failed payload")
                nTdebug("Time is %s" % str(datetime.now()))
                if self.deleteLock(tokenLock):
                    nTerror("Failed to delete lock %s" % tokenLock)
                    nTdebug("Time is %s" % str(datetime.now()))
                # end if
                self.slaveEndAndLog(self.LEVEL_ERROR_STR, token, tokenContent, self.COMMAND_FAILED_STR)
                continue
            # end if
            self.slaveEndAndLog(self.LEVEL_MSG_STR, token, tokenContent, self.COMMAND_FINISHED_STR)
            # Check if unfinished cing tgz file exists
            unfTgzFileName = tokenPartList[1] + ".cing.unf.tgz"
            if(os.path.exists(unfTgzFileName)):
                targetUrl = '/'.join([self.master_target_url, self.MASTER_TARGET_UNF])
                # Send it to the master
                if putFileBySsh(unfTgzFileName, targetUrl):
                    nTerror("In runSlaveThread failed putFileBySsh for unfinished cing tgz")
                    nTdebug("Time is %s" % str(datetime.now()))
                # end if
                # Remove the unfinished cing tgz file from the slave
                nTmessage("Removing tgz result: %s" % unfTgzFileName)
                os.remove(unfTgzFileName)
            # end if
            tokensFinished += 1
            nTdebug("Time is %s, finished token" % str(datetime.now()))
        # end while
    #  if [ "$?" != "0" ]; then
    #    $TOPOS deleteLock $POOL ${tokeninfo[1]}
    #    echo "Wrong!"
    #    continue
    #  fi
        nTdebug("Should never get here.")
        nTerror("Code runSlaveThread should never stop in vCingSlave except when interrupted by user.")
    # end def

    def runSlave(self):
        """
        Returns True on error
        Intended to run forever: kill by:
        -1- shutting down the VM running it
        -2- killall Python (pretty drastic)
        -3- Twice a 2 (INT) signal to master, it will then kill each 'thread'.
            E.g. set pid = 4237 && kill -2 $pid && sleep 10 && kill -2 $pid
        """

        if os.chdir(cingDirTmp):
            nTerror("Failed to change to directory for temporary test files: %s" % cingDirTmp)
            return True
        # end if
        _status, date_string = commands.getstatusoutput('date "+%Y-%m-%d_%H-%M-%S"') # gives only seconds.
        _status, epoch_string = commands.getstatusoutput('java Wattos.Utils.Programs.GetEpochTime')
        time_string = '%s_%s' % (date_string, epoch_string)
        nTmessage("In runSlave time is: %s" % time_string)


        job_list = []
        ncpus = cing.ncpus
        if False: # DEFAULT: False
            ncpus = 1
        # end if
        for i in range(ncpus):
            date_stamp = getDateTimeStampForFileName()
            base_name = nTpath(__file__)[1]
            # Might be important to run in real separate process.
            cmd = '%s runSlaveThread > %s_%s_%s.log 2>&1 ' % (
                __file__, base_name, date_stamp, i)
            job = (do_cmd, (cmd,))
            job_list.append(job)
        # end for
        delay_between_submitting_jobs = 60
        f = ForkOff(processes_max=ncpus, max_time_to_wait=self.max_time_to_wait)
        done_entry_list = f.forkoff_start(job_list, delay_between_submitting_jobs)
        nTdebug("In runSlave Should never get here in runSlave.")
        done_entry_list.sort()
        not_done_entry_list = range(len(job_list))
        for id in done_entry_list:
            idx = not_done_entry_list.index(id)
            if idx >= 0:
                del(not_done_entry_list[idx])
            # end if
        # end for
        nTmessage("In runSlave Finished list  : %s" % done_entry_list)
        nTmessage("In runSlave Unfinished list: %s" % not_done_entry_list)
        for id in not_done_entry_list:
            job = job_list[id]
            _do_cmd, cmdTuple = job
            cmd = cmdTuple[0]
            nTerror("In runSlave Failed forked: %s" % cmd)
        # end for
    # end def
# end class

if __name__ == "__main__":
    cing.verbosity = verbosityDebug

    nTmessage(header)
    nTmessage(getStartMessage())

    vc = Vcing(cmdDict=cmdDict)
    nTmessage("Starting with %r" % vc)

    destination = sys.argv[1]
    startArgListOther = 2
    argListOther = []
    if len(sys.argv) > startArgListOther:
        argListOther = sys.argv[startArgListOther:]
    # end if
    nTmessage('\nGoing to destination: %s with(out) arguments %s' % (destination, str(argListOther)))
    try:
        if destination == 'runSlaveThread':
            if vc.runSlaveThread():
                nTerror("Failed to runSlaveThread")
            # end if
        elif destination == 'runSlave':
            if vc.runSlave():
                nTerror("Failed to vCingSlave")
            # end if
        elif destination == 'prepareMaster':
            if vc.prepareMaster():
                nTerror("Failed to prepareMaster")
            # end if
        elif destination == 'cleanMaster':
            if vc.cleanMaster():
                nTerror("Failed to cleanMaster")
            # end if
        elif destination == 'addTokenListToTopos':
            # Tokens already created by nrgCing.py
            if vc.addTokenListToTopos(argListOther[0]):
                nTerror("Failed to addTokenListToTopos")
            # end if
        else:
            nTerror("Unknown destination: %s" % destination)
        # end if
    finally:
        nTmessage(getStopMessage(cing.starttime))
    # end try
# end if main
    
