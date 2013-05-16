'''
Unit test execute as:
python -u $CINGROOT/python/cing/Libs/test/test_NoeCompleteness.py

Created on May 30, 2011

@author: jd
'''
from cing import cingDirTestsData
from cing import cingDirTmp
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Libs.NoeCompleteness import * #@UnusedWildImport
from unittest import TestCase
import unittest


class AllChecks(TestCase):
    'Test case'
    cingDirTmpTest = os.path.join( cingDirTmp, 'test_NoeCompleteness' )
    mkdirs( cingDirTmpTest )
    os.chdir(cingDirTmpTest)

#    def _test_NoeCompletenessLib(self):
##        cing.verbosity = cing.verbosityDebug
#        ncl = NoeCompletenessAtomLib()
#        self.assertTrue(ncl)
#        
        
    def test_ArtificialRestraints(self):
        'test artificialRestraints'
#        cing.verbosity = cing.verbosityDebug
        doCompletenessCheck         = True  # DEFAULT True
        doTheoreticalDihedralCheck  = True  # DEFAULT True
        doHydrogenBondCheck         = True  # DEFAULT True
        entryId = "1brv" # DEFAULT Testing entry with just 2 models.
#        entryId = "1nk4" # Interest of Winston
#        entryId = "1jve" # Interest of Winston
#        entryId = "1NK4_DNA" # Interest of Winston
#        entryId = "complexfit_6_0627_DNA" # Interest of Winston
#        entryId = "polxbinary" # Interest of Winston
#        entryId = "cluster1_1_130311" # Interest of Winston
#        entryId = "cluster1_3_07072012" # Interest of Winston
        convention = IUPAC # DEFAULT e.g. for 1brv?
#        convention = CNS # e.g. for cluster1_3_07072012
        max_dist_expectedOverall = 4.0 # DEFAULT
#        max_dist_expectedOverall = 2.0 # Fast check.
#        max_dist_expectedOverall = 6.0 # Winston's
#        ob_file_name = None
        ob_file_name = os.path.join( cingDirLibs, NoeCompletenessAtomLib.STR_FILE_DIR, 'ob_custom_2.str')
#        ranges = 'A.173-178'
        ranges = None

        pdbDirectory = os.path.join(cingDirTestsData,"pdb", entryId)
        pdbFileName = "pdb"+entryId+".ent"
        pdbFilePath = os.path.join( pdbDirectory, pdbFileName)

        project = Project( entryId )
        self.failIf( project.removeFromDisk())
        project = Project.open( entryId, status='new' )
        project.initPDB( pdbFile=pdbFilePath, convention = convention )

        m = project.molecule
        nTdebug("m: %s" % m)
        resList = m.ranges2list(ranges)
        nTdebug("resList: %s" % resList)
        self.assertTrue(resList)
        
        if doCompletenessCheck:
            resultCompleteness = doCompleteness( project,
                 max_dist_expectedOverall = max_dist_expectedOverall,
                 use_intra = True,
                 ob_file_name = ob_file_name, # Defaults to ob_standard.str
#                 ob_file_name = os.path.join( cingDirLibs, NoeCompletenessAtomLib.STR_FILE_DIR, ''ob_heavy.str'.str')
                 summaryFileNameCompleteness = "%s_compl_sum" % entryId,
                 write_dc_lists = True,
                 file_name_base_dc  = "%s_compl" % entryId,
                 resList = resList
            )
            self.assertTrue(resultCompleteness)

        if doTheoreticalDihedralCheck:        
            resultTheoreticalDihedral = doTheoreticalDihedral( project,
                 variance = 10, 
#                 ob_file_name = None, # defaults to dih_standard.str
#                 ob_file_name = os.path.join( cingDirLibs, NoeCompletenessAtomLib.STR_FILE_DIR, 'dih_backbone.str'),
                 write_ac_lists = True,
                 file_name_base_ac  = "%s_dihedral" % entryId,
                 resList = resList
            )
            self.assertTrue(resultTheoreticalDihedral)

        if doHydrogenBondCheck:
            resultHydrogenBondCheck = doCompleteness( project,
                 max_dist_expectedOverall = 2.7, # you might want this tighter. In Wattos I use:
# Float   hbHADistance Hydrogen bond distance between proton and acceptor cutoff (2.7 Angstroms suggested)
# Float   hbDADistance Hydrogen bond distance between donor and acceptor cutoff (3.35 Angstroms suggested)
                 
                 use_intra = True,
                 ob_file_name = os.path.join( cingDirLibs, NoeCompletenessAtomLib.STR_FILE_DIR, 'ob_hydrogen_bond.str'),
                 write_dc_lists = True,
                 file_name_base_dc  = "%s_hb" % entryId,
                 hbOnly = True,
                 resList = resList
            )
            self.assertTrue(resultHydrogenBondCheck)
    # end def
# end class        
        
if __name__ == "__main__":    
    cing.verbosity = cing.verbosityDebug
    unittest.main()
