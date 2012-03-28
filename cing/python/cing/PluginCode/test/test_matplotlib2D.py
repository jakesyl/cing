"""
Unit test execute as:
python $CINGROOT/python/cing/PluginCode/test/test_matplotlib2D.py
"""
from cing import cingDirTestsData
from cing import cingDirTmp
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Libs.numpyInterpolation import interp2_linear
from cing.Libs.numpyInterpolation import interpn_linear
from cing.Libs.numpyInterpolation import interpn_nearest
from cing.PluginCode.matplib import NTplotSet
from cing.PluginCode.matplib import gray_inv
from cing.PluginCode.matplib import makeDihedralHistogramPlot
from cing.PluginCode.required.reqCcpn import CCPN_STR
from cing.core.classes import Project
from matplotlib.pylab import * #@UnusedWildImport
from nose.plugins.skip import SkipTest
from numpy import * #@UnusedWildImport
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

    def test_matplotlib2D(self):

        # important to switch to temp space before starting to generate files for the project.
        cingDirTmpTest = os.path.join( cingDirTmp, getCallerName() )
        mkdirs( cingDirTmpTest )
        self.failIf(os.chdir(cingDirTmpTest), msg =
            "Failed to change to test directory for files: " + cingDirTmpTest)

        # Trying to plot without GUI backend.
#        use('Agg') Already present in NTplot.py

        plot( [1,2,3] , 'go' )

        savefig('backendPlot.png')
        savefig('backendPlot.pdf')
        close()

    def _testNumpyInterpolation(self):
        x,y = ogrid[ -1:1:10j, -1:1:10j ]
        z = sin( x**2 + y**2 )
        vmin = -1.
        vmax =  1.
        binx = (x,y)
        tx = ogrid[ -1:1:10j, -1:1:10j ]

        subplot(221)
        title('original')
        imshow(z, vmin=vmin, vmax=vmax)
        subplot(223)
        title('interpn_nearest')
        imshow( interpn_nearest( z, tx, binx ), vmin=vmin, vmax=vmax )
        subplot(222)
        title('interpn_linear')
        imshow( interpn_linear( z, tx, binx ), vmin=vmin, vmax=vmax )
        subplot(224)
        title('interp2_linear')
        imshow( interp2_linear( z, tx[0],tx[1], x.ravel(),y.ravel() ), vmin=vmin, vmax=vmax )
        show()

    def testMatplotlibColorSegmented(self):
        palette  = gray_inv # from white to black
        # Testing defaults should be the same when set or not set.
        for doSet in ( False, True):
            nTdebug("doSet: %s" % doSet)
            if doSet:
                palette.set_under(color = 'w', alpha = 1.0 )
                palette.set_over(color = 'k', alpha = 1.0 )
                palette.set_bad(color = 'k', alpha = 0.0 )
            nTdebug("under: %s"   % str(palette._rgba_under))
            nTdebug("over : %s"   % str(palette._rgba_over))
            nTdebug("bad  : %s\n" % str(palette._rgba_bad))
            self.assertEqual(palette(0.0)[0],1.0) # low end is white with alpha 1
            self.assertEqual(palette(0.0)[3],1.0)
            self.assertEqual(palette(1.0)[0],0.0) # hi end is white with alpha 1
            self.assertEqual(palette(1.0)[3],1.0) #
            # under should be white with alpha 0 should actually be true, alpha needs to be zero for under.
            self.assertEqual(      palette(-1.0  )[0],1.0)   
            self.assertEqual(      palette(-1.0  )[3],1.0)
            # over should be black with alpha 1 should actually be true, alpha needs to be zero for under.
            self.assertEqual(      palette( 9.0  )[0],0.0)   
            self.assertEqual(      palette( 9.0  )[3],1.0)

    def testMatplotlibColorSegmented3(self):
        palette  = gray_inv
        palette.set_under(color = 'w', alpha = 0.0 )
        # See issue 214
        paletteStr = str( palette([-1,     # under: red but with alpha zero.
                       0.,      # black with alpha 1
                       1,      # white with alpha 1
                       ],
        #               alpha=0)
        ))
        nTdebug( paletteStr )
        
    def test_makeDihedralHistogramPlot(self):
        '''
        See test_NTplot2 for simpler test
        '''
        cing.verbosity = verbosityDebug        
        cingDirTmpTest = os.path.join( cingDirTmp, getCallerName() )
        mkdirs( cingDirTmpTest )
        self.failIf(os.chdir(cingDirTmpTest), msg =
            "Failed to change to test directory for files: " + cingDirTmpTest)        
#        entryId = "1brv_cs_pk_2mdl"        
        entryId = "2kq3"        
        project = Project.open(entryId, status = 'new')
        inputArchiveDir = os.path.join(cingDirTestsData, "ccpn")
        ccpnFile = os.path.join(inputArchiveDir, entryId + ".tgz")
        self.assertTrue(project.initCcpn(ccpnFolder = ccpnFile ))
        self.assertFalse( project.validateDihedrals() )
#        residue = project.molecule.A.PRO172
        residue = project.molecule.A.ASP19
        # Dihedral plots
        for dihed in residue.db.dihedrals.zap('name'):
            if dihed in residue and residue[dihed]:
#                d = residue[dihed] # List of values with outliers etc attached.
#                nTdebug("Residue %s: generating dihedral %s plot", residue, dihed )
                ps = makeDihedralHistogramPlot( project, residue, dihed )
                tmpPath = os.path.join( dihed + '.png')
                if ps and isinstance(ps, NTplotSet):
                    ps.hardcopy( fileName = tmpPath )
                #end if
            #end if
        #end for
    # end def

if __name__ == "__main__":
    cing.verbosity = verbosityDebug
    unittest.main()
