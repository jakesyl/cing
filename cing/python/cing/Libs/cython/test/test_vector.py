"""
Unit test execute as:
python $CINGROOT/python/cing/Libs/cython/test/test_vector.py
"""
from cing.Libs.NTutils import * #@UnusedWildImport
try:
    import pyximport
    pyximport.install()
    import cing.Libs.cython.superpose as superpose
# GWV 20140501: changed calls
#    from cing.Libs.cython.superpose import NTcMatrix
#    from cing.Libs.cython.superpose import NTcVector
#    from cing.Libs.cython.superpose import calculateRMSD
#    from cing.Libs.cython.superpose import superposeVectors
#    from cing.Libs.cython.superpose import Rm6dist #@UnresolvedImport
except ImportError:
    pass
from cing.core.molecule import Coordinate #@UnusedImport
from cing.core.molecule import CoordinateOld #@UnusedImport
from cing.core.molecule import nTdihedralOpt
from unittest import TestCase
import profile #@UnusedImport
import pstats #@UnusedImport
import unittest #@UnusedImport

class AllChecks(TestCase):

    def testVector0(self):
        v = superpose.NTcVector(0.0,1.0,2.0)
        nTdebug("v: %r or %s" % (v,v) )

    def testVector(self):
        n = 10 * 1000
        cList = []
        for _j in range(4):
            # performance is 3.1 s per 10,000
#            c = CoordinateOld(random(),random(),random())
            # performance is 8.2 s per 10,000
            c = Coordinate(random(),random(),random())
            cList.append(c)
        for _i in range(n):
            _d = nTdihedralOpt(cList[0], cList[1], cList[2], cList[3])
#            nTdebug("d: %8.3f" % d )

    def testSuperposeChains(self):
        pass

if __name__ == "__main__":
#     cing.verbosity = verbosityDebug
#     profile.run('unittest.main()', 'fooprof')
#     p = pstats.Stats('fooprof')
#    p.sort_stats('time').print_stats(10)
#     p.sort_stats('cumulative').print_stats(20)
    unittest.main() # or just use this line to test without profiling.
