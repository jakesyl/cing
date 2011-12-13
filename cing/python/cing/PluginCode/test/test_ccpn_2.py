"""
Unit test execute as:
python $CINGROOT/python/cing/PluginCode/test/test_ccpn_2.py
"""

from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Libs.disk import isRootDirectory
from cing.PluginCode.required.reqCcpn import CCPN_STR
from nose.plugins.skip import SkipTest
from unittest import TestCase
import unittest

# Import using optional plugins.
try:
    from cing.PluginCode.Ccpn import Ccpn #@UnusedImport needed to throw a ImportWarning so that the test is handled properly.
    from cing.PluginCode.Ccpn import getProjectNameInFileName
    from cing.PluginCode.Ccpn import getRestraintBoundList
    from cing.PluginCode.Ccpn import modResDescriptorForTerminii
    from cing.PluginCode.Ccpn import patchCcpnResDescriptor
except ImportWarning, extraInfo: # Disable after done debugging; can't use nTdebug yet.
    print "Got ImportWarning %-10s Skipping unit check %s." % ( CCPN_STR, getCallerFileName() )
    raise SkipTest(CCPN_STR)
# end try

class AllChecks(TestCase):

    def testIsRootDirectory(self):
        self.assertTrue( isRootDirectory("linkNmrStarData/"))
        self.assertTrue( isRootDirectory("linkNmrStarData//"))
        self.assertFalse( isRootDirectory("linkNmrStarData/ccp/"))
        self.assertFalse( isRootDirectory("linkNmrStarData/ccp//"))
    # end def

    def _testRestraintsValuesRegular(self):
        _alsoSee = """See http://code.google.com/p/cing/issues/detail?id=121"""

        msgHoL = MsgHoL()
#        lower, upper, targetValue, error
        rList = [
                 (0.0, 3.0, 4.0, 1.0), # Should give a warning and just use lower/upper as is.
                 (0.0, 3.0, 4.0, None), # Same
                 (0.0, 5.5, 5.5, None), # failed for entry 2cka with original code.
                 (None, None, 5.5, None),
                 (None, None, 5.5, 1.0),
                 (None, None, None, None),
                 (None, 4.0, None, None), # upper bound only
                 (2.0, None, None, None), # lower only
                 (-2.0, 5.0, None, None), # should give reasonable error and unset distance lower bound

                 (-5.0, 5.0, None, None, Ccpn.RESTRAINT_IDX_DIHEDRAL), # Is a range of 10 degrees.
                 (5.0, - 5.0, None, None, Ccpn.RESTRAINT_IDX_DIHEDRAL), # Is a range of 350 degrees.
                 (None, None, - 10.0, 20.0, Ccpn.RESTRAINT_IDX_DIHEDRAL), # Is a range of 20 degrees.
                 (None, None, 350.0, 20.0, Ccpn.RESTRAINT_IDX_DIHEDRAL), # Same.
                 (None, None, 123.0, 200.0, Ccpn.RESTRAINT_IDX_DIHEDRAL), 
                 # Give a reasonable warning and sets to full circle by setting to (0,-SMALL_FLOAT_FOR_DIHEDRAL_ANGLES)
                   ]
        cingRlist = [
                     (0.0, 3.0),
                     (0.0, 3.0),
                     (0.0, 5.5),
                     (5.5, 5.5),
                     (4.5, 6.5),
                     None,
                     (None, 4.0),
                     (2.0, None),
                     (None, 5.0),

                     (-5.0, 5.0), # dihedrals
                     (5.0, - 5.0),
                     (-30.0, 10.0),
                     (-30.0, 10.0),
                     (0.0, - Ccpn.SMALL_FLOAT_FOR_DIHEDRAL_ANGLES),
                   ]

        for i in range(len(rList)):
            cc = rList[i]
            ccpnConstraint = NTdict()
            ccpnConstraint.lowerLimit = cc[0]
            ccpnConstraint.upperLimit = cc[1]
            ccpnConstraint.targetValue = cc[2]
            ccpnConstraint.error = cc[3]
            restraintTypeIdx = Ccpn.RESTRAINT_IDX_DISTANCE
            if len(cc) >= 5:
                restraintTypeIdx = cc[4]

            cie = cingRlist[i]
#               Output: floats (lower, upper)
            ci = getRestraintBoundList(ccpnConstraint, restraintTypeIdx, msgHoL)

            if not ci:
                self.assertFalse(cie)
            else:
                self.assertEquals(ci[0], cie[0])
                self.assertEquals(ci[1], cie[1])
            msgHoL.showMessage(999, 999, 999, 999)
    def _testPatchCcpnResDescriptor(self):
        rList = [ # result, description, ccpnMolType, linking,
                 ['neutral', 'prot:H3', Ccpn.CCPN_PROTEIN, Ccpn.CCPN_START],
                 ['prot:H3', 'prot:H3', Ccpn.CCPN_RNA, Ccpn.CCPN_START], # do not touch!
                 ['prot:HG1', "prot:HG1;deprot:H''", Ccpn.CCPN_PROTEIN, Ccpn.CCPN_END],
                 ['prot:HD1;prot:HE2', 'prot:HD1;prot:HE2', Ccpn.CCPN_PROTEIN, Ccpn.CCPN_MIDDLE],
                 [Ccpn.CCPN_DEPROT_HG, Ccpn.CCPN_DEPROT_HG, Ccpn.CCPN_PROTEIN, Ccpn.CCPN_MIDDLE], # not an issue anymore.
                   ]

        for i in range(len(rList)):
            d = rList[i]
            nTdebug("d: %s" % d)
            self.assertEquals(d[0], patchCcpnResDescriptor(d[1], d[2], d[3]))
    # end def

    def testModDescriptorForTerminii( self ):

        seqLength = 3
        # Note the list is the same as above; the assert has the first 2 argument switched.
        rList = [ # result, description, ccpnMolType, linking,
                 ['neutral', "deprot:H''", Ccpn.CCPN_PROTEIN, 2], # C-terminus
                 ['neutral', 'prot:H3', Ccpn.CCPN_PROTEIN, 0], # N-terminus
                 ['prot:H3', 'prot:H3', Ccpn.CCPN_RNA, 0], # do not touch!
                 ['prot:HG1', "prot:HG1;deprot:H''", Ccpn.CCPN_PROTEIN, 2],
                 ['prot:A,B;deprot:X,Y', "prot:A,B;deprot:H'',X,Y", Ccpn.CCPN_PROTEIN, 2],
                 ['prot:HD1,HE2', 'prot:HD1,HE2', Ccpn.CCPN_PROTEIN, 1],
                 [Ccpn.CCPN_DEPROT_HG, Ccpn.CCPN_DEPROT_HG, Ccpn.CCPN_PROTEIN, 1], # not an issue anymore.
                   ]

        for i in range(len(rList)):
            d = rList[i]
            nTdebug("d: %s" % d)
            self.assertEquals(d[1], modResDescriptorForTerminii( d[0], d[3], seqLength, d[2]))


    def _testCcpnProjectNameOfFn(self):
        inputList = ["BASP/memops/Implementation/BASP.xml",
                     "/X/Y/memops/Implementation/BASP.xml", # base not important.
                     "bla.xml",
                     "/X/Y/memops/Implementation/BA SP.xml"
                     ]
        expectedList = ['BASP',
                        'BASP',
                        None,
                        'BA SP'
                        ]
        for i, input in enumerate(inputList):
            result = getProjectNameInFileName(input)
            nTdebug( "i, input, result, expected: [%s] [%s] [%s] [%s]" % ( i, input, result, expectedList[i]))
            self.assertEquals(expectedList[i], result)


if __name__ == "__main__":
    cing.verbosity = verbosityDefault
    cing.verbosity = verbosityDebug
    unittest.main()
