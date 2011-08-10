"""
Unit test execute as:
python $CINGROOT/python/cing/STAR/test/test_SaveFrame.py
"""
from cing import cingDirTmp
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.STAR.SaveFrame import SaveFrame
from cing.STAR.TagTable import TagTable
from unittest import TestCase
import unittest


class AllChecks(TestCase):
    cingDirTmpTest = os.path.join( cingDirTmp, 'test_SaveFrame' )
    mkdirs( cingDirTmpTest )
    os.chdir(cingDirTmpTest)


    sf = SaveFrame()
    tT = TagTable()
    tT.tagnames=['_File_characteristics.Sf_category']
    tT.tagvalues=[['file_characteristics']]
    sf.tagtables.append(tT)

    def test_check_integrity(self):
        self.assertFalse(self.sf.check_integrity())

    def test_STARrepresentation(self):
        # pylint: disable=C0301
        starTextExpected = """\nsave_general_sf_title\n   loop_\n      _File_characteristics.Sf_category\n\nfile_characteristics\n\n   stop_\n\nsave_\n"""
#        starTextExpected.replac(' \n', new)
        starText = self.sf.star_text()
        self.assertEqual(starText, starTextExpected)
        
    def test_getSaveFrameCategory(self):
        sfCategory = "file_characteristics"
        self.assertEqual(self.sf.getSaveFrameCategory(), sfCategory)


if __name__ == "__main__":
    unittest.main()
