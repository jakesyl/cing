"""
Unit test execute as:
python -u $CINGROOT/python/cing/STAR/test/test_File.py
"""
from cing import cingDirTmp
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.STAR import Utils
from cing.STAR.File import File
from unittest import TestCase
import unittest
import urllib
import zipfile



class AllChecks(TestCase):
    strf = File()
    cingDirTmpTest = os.path.join( cingDirTmp, 'test_File' )
    mkdirs( cingDirTmpTest )
    os.chdir(cingDirTmpTest)

    def test_Parse(self):
        text = """data_no_comments_here

save_comment
   _Saveframe_category  comment
   loop_
        _comment
        _every_flag
        _category

'#It has very upfield-shifted H5', H5" @ 3.935,4.012 ppm'
;
#######################
#  BOGUS              #
#######################

;

    BOGUS_CATEGORY

     stop_
save_
"""
        self.assertFalse(self.strf.parse(text = text))
        st = self.strf.star_text()
#            print "unparsed text:[" +st+ "]"

        exp = """data_no_comments_here
save_comment   _Saveframe_category  comment   loop_
        _comment
        _every_flag
        _category
;
#It has very upfield-shifted H5', H5" @ 3.935,4.012 ppm
;
;
#######################
#  BOGUS              #
#######################

;    BOGUS_CATEGORY     stop_ save_
"""
        self.assertTrue(Utils.equalIgnoringWhiteSpace(exp, st))

    def test_ReadFile(self):
        testEntry('1edp')

def testEntry(entry):
    """
    Extra Test Routine going over some entries in the NMR Restraints Grid
    """
    # Put a check in for internet availability.
    nTmessage("Testing Entry")
    strf = File()
    # Freely available on the web so not included in package.
    stage = "2-parsed"
#    stage = "3-converted-DOCR"
    urlLocation = ("http://www.bmrb.wisc.edu/NRG/MRGridServlet?" +
    "block_text_type=%s&file_detail=%s&pdb_id=%s" +
    "&program=STAR&request_type=archive&subtype=full&type=entry") % (stage, stage, entry)
    fnamezip = entry + ".zip"
#    print "DEBUG: downloading url:", urlLocation
    # TODO: wrap this in a try so the test is less invulnerable to network outages.
    try:
        urllib.urlretrieve(urlLocation, fnamezip)
    except:
        # not a real error since there might not be a network connection.
        nTwarning("Failed to get; " + urlLocation)
        return
#    print "DEBUG: opening local zip file:", fnamezip
    zfobj = zipfile.ZipFile(fnamezip)
    fname = None
    for name in zfobj.namelist():
        if name.endswith('.str'):
            fname = name
    orgWattosWrittenFile = entry + "_org.str"
    pystarlibWrittenFile = entry + "_pystar.str"
    wattosWrittenFile = entry + "_wattos.str"
    diffOrgPystarFile = entry + "_diff_org_pystar.str"
    diffPystarWattosFile = entry + "_diff_pystar_wattos.str"
    diffOrgWattosWattosFile = entry + "_diff_org_wattos_wattos.str"

    outfile = open(orgWattosWrittenFile, 'w')
    outfile.write(zfobj.read(fname))
    outfile.close()
    zfobj.close()
    strf.filename = orgWattosWrittenFile

    strf.read()
    strf.filename = pystarlibWrittenFile
    strf.write()

    nTmessage("Most likely the below diff will fail because it depends on diff being installed")
    cmd = "diff --ignore-all-space --ignore-blank-lines %s %s > %s" % (orgWattosWrittenFile, pystarlibWrittenFile, diffOrgPystarFile)
    os.system(cmd)
    if not os.path.exists(diffOrgPystarFile):
        nTwarning("failed to diff files: " + orgWattosWrittenFile + ", " + pystarlibWrittenFile)

    nTdebug("Most likely the below check will fail because it depends on Wattos being installed")
    nTdebug("rewrite to Java formating for comparison")
    cmd = "%s Wattos.Star.STARFilter %s %s ." % (JVM_CMD_STD, pystarlibWrittenFile, wattosWrittenFile)
    logFileName = "wattos_STARFilter.log"
    wattosProgram = ExecuteProgram(cmd, redirectOutputToFile = logFileName)
    wattosExitCode = wattosProgram()
    if wattosExitCode:
        nTwarning("failed to execute Wattos")
        return

    if not os.path.exists(wattosWrittenFile):
        nTerror("failed to rewrite file: " + pystarlibWrittenFile)
        return

    cmd = "diff --ignore-all-space --ignore-blank-lines %s %s > %s" % (pystarlibWrittenFile, wattosWrittenFile, diffPystarWattosFile)
    os.system(cmd)
    if not os.path.exists(diffPystarWattosFile):
        nTwarning("failed to diff file: " + pystarlibWrittenFile + ", " + wattosWrittenFile)
    cmd = "diff --ignore-all-space --ignore-blank-lines %s %s > %s" % (orgWattosWrittenFile, wattosWrittenFile, diffOrgWattosWattosFile)
    os.system(cmd)
    if not os.path.exists(diffOrgWattosWattosFile):
        nTwarning("failed to diff file: ", orgWattosWrittenFile + ", " + wattosWrittenFile)

    if 1:
        try:
            os.unlink(entry + ".zip")
            os.unlink(orgWattosWrittenFile)
            os.unlink(pystarlibWrittenFile)
        except:
            pass
        # end try
    # end if

def testSingleFile(filename):
    """
    Extra Test Routine going over some entries in the NMR Restraints Grid
    """
    strf = File()
    strf.filename = filename
    nTdebug("reading file ", strf.filename)
    strf.read()
    strf.filename = strf.filename + "_new.str"
    nTdebug("writing file ", strf.filename)
    strf.write()


if __name__ == "__main__":
    cing.verbosity = verbosityDetail
    cing.verbosity = verbosityOutput
    cing.verbosity = verbosityDebug
    unittest.main()
