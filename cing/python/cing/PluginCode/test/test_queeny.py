"""
Unit test execute as:
python $CINGROOT/python/cing/PluginCode/test/test_queeny.py
"""
from cing import cingDirTestsData
from cing import cingDirTmp
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.NRG import * #@UnusedWildImport
from cing.NRG.storeCING2db import doStoreCING2db
from cing.PluginCode.required.reqCcpn import CCPN_STR
from cing.PluginCode.required.reqQueeny import * #@UnusedWildImport
from cing.core.classes import Project
from nose.plugins.skip import SkipTest
from unittest import TestCase
import unittest

# Import using optional plugins.
try:
    from cing.PluginCode.Ccpn import Ccpn #@UnusedImport needed to throw a ImportWarning so that the test is handled properly.
except ImportWarning, extraInfo: # Disable after done debugging; can't use nTdebug yet.
    print "Got ImportWarning %-10s Skipping unit check %s." % ( CCPN_STR, getCallerFileName() )
    raise SkipTest(CCPN_STR)
# end try

class AllChecks(TestCase):
    def test_queeny(self):

        runQueeny = 1           # DEFAULT: 1
        doStoreCheck = False    # DEFAULT: False Requires sqlAlchemy
        doValueCheck = 1        # DEFAULT: 1 Requires 1brv
        entryList = "1brv_cs_pk_2mdl".split() # DEFAULT because it contains many data types and is small/fast to run.
#        entryList = "1a24 1a4d 1afp 1ai0 1b4y 1brv 1brv 1bus 1cjg 1hue 1ieh 1iv6 1kr8 2cka 2hgh 2jzn 2k0e 8psh".split()

        expectedInfoList = [
(158, 0.0     ),
(159, 0.0     ),
(160, 0.0     ),
(161, 0.0     ),
(162, 0.0     ),
(163, 0.0     ),
(164, 0.0     ),
(165, 0.000141),
(166, 0.006669),
(167, 0.047112),
(168, 0.159379),
(169, 0.309577),
(170, 0.578983),
(171, 0.838257), # First residue with restraints. Previously none zero elements are due to window averaging JFD assumes.
(172, 1.029047),
(173, 1.063531),
(174, 0.969195),
(175, 1.027744),
(176, 0.954469),
(177, 0.794625),
(178, 0.822723),
(179, 0.845598),
(180, 0.828139),
(181, 0.971881),
(182, 1.141096),
(183, 1.063613),
(184, 0.974891),
(185, 1.116405),
(186, 1.113886),
(187, 0.945552),
(188, 0.731124),
(189, 0.411986),
        ]

        cingDirTmpTest = os.path.join( cingDirTmp, getCallerName() )
        mkdirs( cingDirTmpTest )
        self.failIf(os.chdir(cingDirTmpTest), msg =
            "Failed to change to test directory for files: " + cingDirTmpTest)

        for entryId in entryList:
            project = Project.open(entryId, status = 'new')
            self.assertTrue(project, 'Failed opening project: ' + entryId)

            inputArchiveDir = os.path.join(cingDirTestsData, "ccpn")

            ccpnFile = os.path.join(inputArchiveDir, entryId + ".tgz")
            if not os.path.exists(ccpnFile):
                ccpnFile = os.path.join(inputArchiveDir, entryId + ".tar.gz")
                if not os.path.exists(ccpnFile):
                    self.fail("Neither %s or the .tgz exist" % ccpnFile)
            self.assertTrue(project.initCcpn(ccpnFolder = ccpnFile, modelCount=1))
            if runQueeny:
                self.assertFalse(project.runQueeny())
                if doValueCheck:
                    for i,res in enumerate( project.molecule.allResidues()):
                        expected = expectedInfoList[i][1]
                        information = getDeepByKeysOrAttributes(res, QUEENY_INFORMATION_STR )
                        uncertainty1 = getDeepByKeysOrAttributes(res, QUEENY_UNCERTAINTY1_STR )
                        uncertainty2 = getDeepByKeysOrAttributes(res, QUEENY_UNCERTAINTY2_STR )
                        nTdebug("Comparing expected versus inf/unc1/unc2 for %20s with %8.3f %8.3f %8.3f %8.3f" % (
                                    res, expected, information, uncertainty1, uncertainty2))
#                        self.assertAlmostEqual(expected,information,3)
            if doStoreCheck:
#                # Does require:
                try:
                    from cing.PluginCode.sqlAlchemy import CsqlAlchemy #@UnusedImport # pylint: disable=W0612,W0404
                    pdbEntryId = entryId[0:4]
                    if doStoreCING2db( pdbEntryId, ARCHIVE_DEV_NRG_ID, project=project):
                        nTerror("Failed to store CING project's data to DB but continuing.")
                except:
                    nTwarning("Failed to doStoreCING2db from test_queeny.py")
        # end for
    # end def test

if __name__ == "__main__":
    cing.verbosity = verbosityDebug
    unittest.main()