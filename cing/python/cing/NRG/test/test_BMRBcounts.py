"""
Unit test execute as:
python $CINGROOT/python/cing/NRG/test/test_BMRBcounts.py
"""
from cing import cingDirData
from cing import cingDirTestsData
from cing import cingDirTmp
from cing.Libs.DBMS import DBMS
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.NRG.PDBEntryLists import getBmrbCsCounts
from cing.PluginCode.required.reqCcpn import CCPN_STR
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

    def _test_BMRBcounts(self):

        cingDirTmpTest = os.path.join( cingDirTmp, getCallerName() )
        mkdirs( cingDirTmpTest )
        self.failIf(os.chdir(cingDirTmpTest), msg =
            "Failed to change to test directory for files: " + cingDirTmpTest)

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
        bmrb_id = 4020
        self.assertEqual( getDeepByKeysOrAttributes( bmrbCountMap, bmrb_id, '1H' ), 183)
        self.assertEqual( getDeepByKeysOrAttributes( bmrbCountMap, bmrb_id, '13C' ), 73)
        self.assertEqual( getDeepByKeysOrAttributes( bmrbCountMap, bmrb_id, '15N' ), None)

    def test_BMRBcounts2(self):

        cingDirTmpTest = os.path.join( cingDirTmp, getCallerName() )
        mkdirs( cingDirTmpTest )
        self.failIf(os.chdir(cingDirTmpTest), msg =
            "Failed to change to test directory for files: " + cingDirTmpTest)

        entryId = '1brv'
        bmrbId = 4020
        inputArchiveDir = os.path.join(cingDirTestsData, "ccpn")
        ccpnFile = os.path.join(inputArchiveDir, entryId + ".tgz")
        project = Project.open(entryId, status = 'new')
        self.assertTrue(project.initCcpn(ccpnFolder = ccpnFile))
        assignmentCountMap = project.molecule.getAssignmentCountMap()
#        p_cs_count = assignmentCountMap['overall']
        p_cs1H_count = assignmentCountMap['1H']
        p_cs13C_count = assignmentCountMap['13C']
        p_cs15N_count = assignmentCountMap['15N']

        bmrbCountMap = getBmrbCsCounts()
        nTdebug("bmrbCountMap %r" % bmrbCountMap)
        entryMap = getDeepByKeysOrAttributes( bmrbCountMap, bmrbId )
        nTdebug("entryMap %r" % entryMap)
        d_cs1H_count = getDeepByKeysOrAttributes( entryMap, '1H' )
        d_cs13C_count = getDeepByKeysOrAttributes( entryMap, '13C' )
        d_cs15N_count = getDeepByKeysOrAttributes( entryMap, '15N' )

        nTdebug("db: %s project: %s" % ( d_cs1H_count, p_cs1H_count ) )
        nTdebug("db: %s project: %s" % ( d_cs13C_count, p_cs13C_count ) )
        nTdebug("db: %s project: %s" % ( d_cs15N_count, p_cs15N_count ) )

#        self.assertTrue( d_cs1H_count, p_cs1H_count) # was 183
#        self.assertTrue( d_cs13C_count, p_cs13C_count) # was 73
#        self.assertTrue( d_cs15N_count, p_cs15N_count)


if __name__ == "__main__":
    cing.verbosity = verbosityDebug
    unittest.main()