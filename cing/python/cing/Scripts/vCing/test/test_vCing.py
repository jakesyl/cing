'''
Created on Oct 20, 2010

@author: jd

topos https://topos.grid.sara.nl/4.1

'''

from cing import cingDirTmp
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Libs.forkoff import Process
from cing.Scripts.vCing.vCing import Vcing
from unittest import TestCase
import unittest

vc = Vcing()
lockTimeOut = 6
sleepTimeSimulatingWork = 10
max_time_to_wait = 365 * 24 * 60 * 60 # a year in seconds
p = Process( max_time_to_wait_kill = max_time_to_wait)

class AllChecks(TestCase):
    # Test will fail if topos hasn't been properly initialized.
    # It is not intended to be run every time the other cing unit test are.
    def _testvCingMaster(self):
        # important to switch to temp space before starting to generate files for the project.
        cingDirTmpTest = os.path.join( cingDirTmp, 'test_vCing' )
        mkdirs( cingDirTmpTest )
        os.chdir(cingDirTmpTest)

        exitCode, token, tokenLock = vc.nextTokenWithLock(lockTimeOut)
        if exitCode:
            nTdebug("Failed to vc.nextTokenWithLock(). Was the token deleted?")
        nTdebug("Got exitCode, token, tokenLock: %s %s %s" % (exitCode, token, tokenLock))
#        vc.refreshLock(tokenLock, lockTimeOut)
        tokenContent = vc.getToken(token)
        nTdebug("Got tokenContent: %s" % tokenContent)
        # Just temporary.
        self.assertFalse(vc.deleteLock(tokenLock))
        exitCode, token, tokenLock = vc.nextTokenWithLock(lockTimeOut)

        pid = p.process_fork( vc.keepLockFresh, [tokenLock, lockTimeOut] )
        nTdebug("Create a background process [%s] keeping the lock" % pid)
        time.sleep(sleepTimeSimulatingWork)
        self.assertFalse(vc.deleteToken(token)) # this should end the background process pid

if __name__ == "__main__":
    cing.verbosity = verbosityDebug
    unittest.main()
