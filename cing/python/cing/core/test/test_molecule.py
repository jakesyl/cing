"""
Unit test execute as:
python $CINGROOT/python/cing/core/test/test_molecule.py
"""
from cing import cingDirTmp
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.core.classes import Project
from cing.core.molecule import * #@UnusedWildImport
from unittest import TestCase
import profile
import pstats
import unittest #@UnusedImport Too difficult for code analyzer.

class AllChecks(TestCase):

    cingDirTmpTest = os.path.join( cingDirTmp, 'test_molecule' )
    mkdirs( cingDirTmpTest )
    os.chdir(cingDirTmpTest)


    def test_NTdihedral(self):
        # 1brv phi
        #ATOM      3  C   VAL A 171       2.427   1.356   3.559  1.00  0.00           C
        #ATOM     16  N   PRO A 172       1.878   0.162   3.927  1.00  0.00           N
        #ATOM     17  CA  PRO A 172       0.906  -0.611   3.099  1.00  0.00           C
        #ATOM     18  C   PRO A 172      -0.287   0.182   2.484  1.00  0.00           C
        cc1 = Coordinate( 2.427,   1.356,   3.559 )
        cc2 = Coordinate( 1.878,   0.162,   3.927 )
        cc3 = Coordinate( 0.906,  -0.611,   3.099 )
        cc4 = Coordinate(-0.287,   0.182,   2.484 )
        for _i in range(1 * 100):
            _angle = nTdihedralOpt( cc1, cc2, cc3, cc4 )
        self.assertAlmostEqual( nTdihedralOpt( cc1, cc2, cc3, cc4 ), -47.1, 1)
        self.assertAlmostEqual( nTangleOpt(    cc1, cc2, cc3      ), 124.4, 1)
        self.assertAlmostEqual( nTdistanceOpt( cc1, cc2           ),   1.4, 1)

    def test_CoordinateOperations(self):
        cc1 = Coordinate( 2.427,   1.356,   3.559 )
        cc2 = Coordinate( 1.878,   0.162,   3.927 )
        cc3 = Coordinate( 0.906,  -0.611,   3.099 )
        cc4 = Coordinate(-0.287,   0.182,   2.484 )
        coordinateList = [cc1, cc2, cc3, cc4]
        model = Model('model', 0)
        model.coordinates.append(*coordinateList)
        ccExpected = Coordinate(1.878,   0.162,   3.559 )
        ccFound = cc1.copy()
        ccFound.setToMin(cc2)
        self.assertTrue( ccFound == ccExpected )

        ccExpected = Coordinate(2.427,   1.356,   3.927 )
        ccFound = cc1.copy()
        ccFound.setToMax(cc2)
        self.assertTrue( ccFound == ccExpected )

    # end def

    def test_EnsureValidChainId(self):
        self.assertEquals( ensureValidChainId('A'), 'A')
        self.assertEquals( ensureValidChainId('a'), 'a')
        v = cing.verbosity
        cing.verbosity = cing.verbosityNothing # temp disable error msg.
        self.assertEquals( ensureValidChainId('ABCD'), 'A')
        self.assertEquals( ensureValidChainId('BCDE'), 'B')
        cing.verbosity = v
        self.assertEquals( ensureValidChainId('1'), '1')
        self.assertEquals( ensureValidChainId('$'), Chain.defaultChainId)
        self.assertEquals( ensureValidChainId('-'), Chain.defaultChainId)
        self.assertEquals( ensureValidChainId('A'), Chain.defaultChainId) # They are the same.
        self.assertEquals( ensureValidChainId(None), Chain.defaultChainId)

    def test_GetNextAvailableChainId(self):
        entryId = 'test'
        project = Project(entryId)
        self.failIf(project.removeFromDisk())
        project = Project.open(entryId, status='new')
        molecule = Molecule(name='moleculeName')
        project.appendMolecule(molecule) # Needed for html.
        chainId = molecule.getNextAvailableChainId()
        self.assertEquals( chainId, Chain.defaultChainId)
        n = 26 * 2 + 10 + 1 # alpha numeric including an extra and lower cased.
        for _c in range(n):
            chainId = molecule.getNextAvailableChainId()
            self.assertTrue( molecule.addChain(chainId))
        nTdebug("Added %d chains to: %s" % (n, molecule.format()))
        self.assertEqual( len(molecule.allChains()), n)

    def test_AddResidue_Standard(self):
        entryId = 'test'
        project = Project(entryId)
        self.failIf(project.removeFromDisk())
        project = Project.open(entryId, status='new')

        mol = Molecule('test')
        project.appendMolecule(mol)
        c = mol.addChain('A')
        r1 = c.addResidue('ALA', 1, Nterminal = True)
        if r1:
            r1.addAllAtoms()
        r2 = c.addResidue('VAL', 2)
        if r2:
            r2.addAllAtoms()
        r2 = c.addResidue('PHE', 3)
        if r2:
            r2.addAllAtoms()
        r2 = c.addResidue('ARG', 4)
        if r2:
            r2.addAllAtoms()
        r3 = c.addResidue('GLU', 5, Cterminal = True)
        if r3:
            r3.addAllAtoms()

        mol.updateAll()

        nTmessage( mol.format() )

    def test_GetMolTypeCountList(self):
        cing.verbosity = verbosityDebug
        entryId = 'test'
        project = Project(entryId)
        self.failIf(project.removeFromDisk())
        project = Project.open(entryId, status='new')

        mol = Molecule('test')
        project.appendMolecule(mol)
        c = mol.addChain('A')
        c.addResidue('ALA', 1, Nterminal = True)
        c.addResidue('VAL', 2)
        c.addResidue('PHE', 3)
        c.addResidue('ARG', 4)
        c.addResidue('GLU', 5, Cterminal = True)
        c = mol.addChain('B')
        c.addResidue('DG', 1, Nterminal = True)
        c.addResidue('DA', 2)
        c.addResidue('DT', 3)
        c.addResidue('DC', 4, Cterminal = True)
        c = mol.addChain('C')

        c.addResidue('RGUA', 1, convention=INTERNAL_0, Nterminal = True)
        c.addResidue('RADE', 2, convention=INTERNAL_0, )
        c.addResidue('URA', 3, convention=INTERNAL_0, ) # not RTHY normally of course.
        c.addResidue('RTHY', 4, convention=INTERNAL_0, )
        c.addResidue('RCYT',  5, convention=INTERNAL_0, Cterminal = True)
        c = mol.addChain('D')
        for i in range(1,11):
            c.addResidue('HOH', i )
        # end for
        c = mol.addChain('E') # Unknown residue to CING
        c.addResidue('ACE', 1 )
        c = mol.addChain('F') # Ions are also other
        c.addResidue('CA2P', 1 )
        for residue in mol.allResidues():
            residue.addAllAtoms()
        # end for
        mol.updateAll()
        nTmessage( mol.format() )
        for c in mol.allChains():
            nTmessage( c.format() )
            nTmessage( "idxMolType: %s" % (c.getIdxMolType()))
        # end for

        nTmessage("Count the molecule types")
        molTypeCountList = mol.getMolTypeCountList()
        p_protein_count = molTypeCountList[ mapMoltypeToInt[PROTEIN_STR] ]
        p_dna_count     = molTypeCountList[ mapMoltypeToInt[DNA_STR] ]
        p_rna_count     = molTypeCountList[ mapMoltypeToInt[RNA_STR] ]
        p_water_count   = molTypeCountList[ mapMoltypeToInt[WATER_STR] ]
        p_other_count   = molTypeCountList[ mapMoltypeToInt[OTHER_STR] ]
        self.assertEqual(1, p_protein_count)
        self.assertEqual(1, p_dna_count  )
        self.assertEqual(1, p_rna_count  )
        self.assertEqual(1, p_water_count)
        self.assertEqual(2, p_other_count)

        nTmessage("Count the residue types")
        molTypeResidueCountList = mol.getMolTypeResidueCountList()
        p_res_protein_count = molTypeResidueCountList[ mapMoltypeToInt[PROTEIN_STR] ]
        p_res_dna_count     = molTypeResidueCountList[ mapMoltypeToInt[DNA_STR] ]
        p_res_rna_count     = molTypeResidueCountList[ mapMoltypeToInt[RNA_STR] ]
        p_res_water_count   = molTypeResidueCountList[ mapMoltypeToInt[WATER_STR] ]
        p_res_other_count   = molTypeResidueCountList[ mapMoltypeToInt[OTHER_STR] ]
        self.assertEqual(5, p_res_protein_count)
        self.assertEqual(4, p_res_dna_count  )
        self.assertEqual(5, p_res_rna_count  )
        self.assertEqual(10, p_res_water_count)
        self.assertEqual(2, p_res_other_count)

        nTmessage("Select a list of residues.")
        inputResList = (('A', 5),('B', 2),('A', 6),('X', 1)) # The last 2 are non-existing residues
        # should give two warnings for a non-existing residue
        resList = project.decodeResidueList( inputResList )
        self.assertEqual(2, len(resList) )
    # end def

    def test_RangeSelection(self):
        cing.verbosity = verbosityDebug
        entryId = 'testEntry'
        project = Project(entryId)
        self.failIf(project.removeFromDisk())
        project = Project.open(entryId, status='new')
        mol = Molecule('testMol')
        project.appendMolecule(mol)
        offset1 = -10
        # homo dimer
        chainList = ( 'A', 'B' )
        sequence = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        seqL = len(sequence)
        lastResidueI = seqL - 1
        for cId in chainList:
            c = mol.addChain(cId)
            for i, rName in enumerate(sequence):
                rNumber = i+offset1
                Nterminal = False # pylint: disable=C0103
                Cterminal = False # pylint: disable=C0103
                if i == 0:
                    Nterminal = True # pylint: disable=C0103
                if i == lastResidueI:
                    Cterminal = True # pylint: disable=C0103
                r = c.addResidue(rName, rNumber, Nterminal = Nterminal, Cterminal = Cterminal)
                if r:
#                    nTdebug("Adding atoms to residue: %s" % r)
                    r.addAllAtoms()
                    for atom in r.allAtoms():
                        atom.addCoordinate(0.0, 1.0, 2.0, 40.0)
#                else:
#                    nTdebug("Skipping atoms for residue: %s" % r)
                # end if
            # end for
        # end for chain

        # another homo dimer with renumbering.
        chainList = ( 'C', 'D' )
        offset2 = 100
        for cId in chainList:
            c = mol.addChain(cId)
            for i, rName in enumerate(sequence):
                rNumber = i+offset2
                Nterminal = False # pylint: disable=C0103
                Cterminal = False # pylint: disable=C0103
                if i == 0:
                    Nterminal = True # pylint: disable=C0103
                if i == lastResidueI:
                    Cterminal = True # pylint: disable=C0103
                r = c.addResidue(rName, rNumber, Nterminal = Nterminal, Cterminal = Cterminal)
                if r:
#                    nTdebug("Adding atoms to residue: %s" % r)
                    r.addAllAtoms()
#                else:
#                    nTdebug("Skipping atoms for residue: %s" % r)
                # end if
            # end for
        # end for chain
        nTdebug("Done creating simple fake molecule")
        self.assertFalse( mol.updateAll() )
        nTmessage( mol.format() )

        # Nada
        selectedResidueList = mol.ranges2list('')
        self.assertEquals( len(selectedResidueList), 2*len(chainList)*seqL)

        # Single residue
        selectedResidueList = mol.ranges2list('A.'+str(offset1))
        self.assertEquals( len(selectedResidueList), 1)
        nTdebug("Selected residues: %s" % str(selectedResidueList))

        # Two residues
        selectedResidueList = mol.ranges2list(str(offset1))
        self.assertEquals( len(selectedResidueList), 2)
        nTdebug("Selected residues: %s" % str(selectedResidueList))

        # Four residues in ranges
        selectedResidueList = mol.ranges2list('1-2')
        self.assertEquals( len(selectedResidueList), 4)
        nTdebug("Selected residues: %s" % str(selectedResidueList))

        # Eight residues in negative crossing ranges
        selectedResidueList = mol.ranges2list('-1-2')
        self.assertEquals( len(selectedResidueList), 8)
        nTdebug("Selected residues: %s" % str(selectedResidueList))


        selectedResidueList = mol.ranges2list('A.-5--2')
        self.assertEquals( len(selectedResidueList), 4)
        nTdebug("Selected residues: %s" % str(selectedResidueList))

        selectedResidueList = mol.ranges2list('-999-999')
        nTdebug("Selected residues: %s" % str(selectedResidueList))
        self.assertEquals( len(selectedResidueList), 2*len(chainList)*seqL)

        residueList2StartStopList = mol.ranges2StartStopList('-999-999')
        nTdebug('residueList2StartStopList: %s' % str(residueList2StartStopList))
        self.assertEquals( len(residueList2StartStopList), 8 )

#        """
#        Possible 5 situations:
#        a      # 1 # positive int
#        -a     # 2 # single int
#        -a-b   # 3 #
#        -a--b  # 4 #
#        a-b    # 5 # most common
#        """
        inputList = """
                      A.1
                      A.1-3
                      A.-2--1
                      A.-2-1
                      A.-3
                    """.split()
        for i, ranges in enumerate(inputList):
            nTdebug("test_RangeSelection: %d %s" % (i, ranges))
            residueList = mol.setResiduesFromRanges(ranges)
#            nTdebug('residueList: [%s]' % residueList)
            rangesRecycled = mol.residueList2Ranges(residueList)
#            nTdebug('rangesRecycled: [%s]' % rangesRecycled)
            self.assertEquals( ranges, rangesRecycled )

        res1, res2 = mol.ranges2list('A.1,A.3')
        self.assertEquals( 2, residueNumberDifference(res1, res2))
        res3, res4 = mol.ranges2list('A.5,A.8')
        self.assertEquals( 3, residueNumberDifference(res3, res4))
        res5, res6 = mol.ranges2list('B.9,B.10')
        self.assertEquals( 1, residueNumberDifference(res5, res6))

        ranges = mol.startStopList2ranges([res1, res2])
        self.assertEquals( 'A.1-3', ranges)
        ranges = mol.startStopList2ranges([res1, res2, res3, res4])
        self.assertEquals( 'A.1-3,A.5-8', ranges)
        ranges = mol.startStopList2ranges([res1, res2, res5, res6])
        self.assertEquals( 'A.1-3,B.9-10', ranges)

        # Check other routine
        chain0 = mol.allChains()[0]
        chain1 = mol.allChains()[1]
        atomList = chain0.getRepresentingAtomListsPerResidue(chain1)
        nTdebug("atomList: %s" % str(atomList))
        self.assertEquals( len(atomList[0]), 5)
    # end def

    def test_RangeSelectionStatic(self):
        inputList = """
            A.1
            A.1-3
            A.-2--1
            A.-2-1
            A.-3
            A.3-52,B.3-52
            2-40,41
            1-96,102-177
            """.split()
        expectedList = [
            [ ['A', 1,  1],                    ],
            [ ['A', 1,  3],                    ],
            [ ['A',-2, -1],                    ],
            [ ['A',-2,  1],                    ],
            [ ['A',-3, -3],                    ],
            [ ['A', 3, 52],     ['B', 3, 52]   ],
            [ ['A', 2, 40],     ['A', 41, 41]  ],
            [ ['A', 1, 96],     ['A', 102, 177]]
        ]
        cing.verbosity = verbosityDebug

        for i, ranges in enumerate(inputList):
            nTdebug("\ntest_RangeSelectionStatic: %d %s" % (i, ranges))
            startStopList = Molecule.ranges2StartStopLoLStatic(ranges)
            nTdebug('startStopList: [%s]' % startStopList)
            self.assertEqual( startStopList, expectedList[i] )
        # end for
    # end def

if __name__ == "__main__":
    cing.verbosity = verbosityDebug
    cingDirTmpTest = os.path.join( cingDirTmp, 'test_molecule' )
    mkdirs( cingDirTmpTest )
    os.chdir(cingDirTmpTest)
    # Commented out because profiling isn't part of unit testing.
    if False:
        fn = 'fooprof'
        profile.run('unittest.main()', fn)
        p = pstats.Stats(fn)
    #     enable a line or two below for useful profiling info
        p.sort_stats('time').print_stats(10)
        p.sort_stats('cumulative').print_stats(2)
    else:
        unittest.main()
