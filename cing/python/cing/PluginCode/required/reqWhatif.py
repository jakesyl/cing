'required items for this plugin for CING setup'
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.core.constants import * #@UnusedWildImport

# Too long lines. pylint: disable=C0301

WHATIF_STR       = "Whatif" # key to the entities (atoms, residues, etc under which the results will be stored

CHECK_ID_STR     = "checkID"
LOC_ID_STR       = "locID"
LEVEL_STR        = "level"
TEXT_STR         = "text"
TYPE_STR         = "type"
#VALUE_LIST_STR   = "valueList" now in constants.py
QUAL_LIST_STR    = "qualList"

INOCHK_STR       = 'INOCHK'
BNDCHK_STR       = 'BNDCHK'
ANGCHK_STR       = 'ANGCHK'
OMECHK_STR       = 'OMECHK'
HNDCHK_STR       = 'HNDCHK'
INOCHK_STR       = 'INOCHK'

QUACHK_STR       = 'QUACHK'
RAMCHK_STR       = 'RAMCHK'
C12CHK_STR       = 'C12CHK'
BBCCHK_STR       = 'BBCCHK'
ROTCHK_STR       = 'ROTCHK'

NQACHK_STR       = 'NQACHK'
PLNCHK_STR       = 'PLNCHK'
PL2CHK_STR       = 'PL2CHK'
PL3CHK_STR       = 'PL3CHK'

CHICHK_STR       = 'CHICHK'
FLPCHK_STR       = 'FLPCHK'
ACCLST_STR       = 'ACCLST'
BMPCHK_STR       = 'BMPCHK'

BA2CHK_STR       = 'BA2CHK'
BH2CHK_STR       = 'BH2CHK'
CHICHK_STR       = 'CHICHK'
DUNCHK_STR       = 'DUNCHK'
HNDCHK_STR       = 'HNDCHK'
MISCHK_STR       = 'MISCHK'
MO2CHK_STR       = 'MO2CHK'
PL2CHK_STR       = 'PL2CHK'
WGTCHK_STR       = 'WGTCHK'
WSVACC_STR       = 'WSVACC'

#define some more user friendly names
# List of defs at:
# http://www.yasara.org/pdbfinder_file.py.txt
# http://swift.cmbi.ru.nl/whatif/html/chap23.html
# All are in text record of file to be parsed so they're kind of redundant.
# Second element is an alternative CING id
# Fourth element is optional short name suitable for labeling a y-axis.

#            WHATIF     CING
nameDefs =[
            (ATOM_LEVEL,'BA2CHK',  None,          'Hydrogen bond acceptors',                                   'Hydrogen bond acceptors'),
            (ATOM_LEVEL,'BH2CHK',  None,          'Hydrogen bond donors',                                      'Hydrogen bond donors'),
            (ATOM_LEVEL,'CHICHK', 'torsion',      'Torsion angle check',                                       'Torsion angle check'),
            (ATOM_LEVEL,'DUNCHK',  None,          'Duplicate atom names in ligands',                           'Duplicate atom names in ligands'),
            (ATOM_LEVEL,'HNDCHK', 'chiralities',  'Chirality',                                                 'Chirality'),
            (ATOM_LEVEL,'MISCHK',  None,          'Missing atoms',                                             'Missing atoms'),
            (ATOM_LEVEL,'MO2CHK',  None,          'Missing C-terminal oxygen atoms',                           'Missing C-terminal oxygen atoms'),
            (ATOM_LEVEL,'PL2CHK',  None,          'Connections to aromatic rings',                             'Plan. to aromatic'),
            (ATOM_LEVEL,'WGTCHK',  None,          'Atomic occupancy check',                                    'Atomic occupancy check'),

            (RES_LEVEL, 'AAINLI',  None,          'Unknown check',                                             'Unknown check'),
            (RES_LEVEL, 'ACCLST',  None,          'Relative accessibility',                                    'Rel. accessibility'),
            (RES_LEVEL, 'ALTATM',  None,          'Amino acids inside ligands check/Attached group check',     'Amino acids inside ligands check/Attached group check'),
            (RES_LEVEL, 'ANGCHK', 'angles',       'Angles',                                                    'Bond angle'),
            (RES_LEVEL, 'ATHYBO',  None,          'Unknown check',                                             'Unknown check'),
            (RES_LEVEL, 'BBAMIS',  None,          'Unknown check',                                             'Unknown check'),
            (RES_LEVEL, 'BBCCHK', 'bbNormality',  'Backbone normality Z-score',                                'Backbone normality' ),
            (RES_LEVEL, 'BMPCHK', 'bumps',        'Bumps',                                                     'Summed bumps'),
            (RES_LEVEL, 'BNDCHK', 'bondLengths',  'Bond lengths',                                              'Bond lengths'),
            (RES_LEVEL, 'BVALST',  None,          'B-Factors',                                                 'B-Factors'),
            (RES_LEVEL, 'C12CHK', 'janin',        'Janin',                                                     'Janin Z'),
            (RES_LEVEL, 'CCOCHK',  None,          'Inter-chain connection check',                              'Inter-chain connection check'),
            (RES_LEVEL, 'EXTO2',   None,          'Test for extra OXTs',                                       'Test for extra OXTs'),
            (RES_LEVEL, 'FATAL',   None,          'Fatal errors',                                              'Unknown check'), # new in Version  : 8.0 (20091126-0948)
            (RES_LEVEL, 'FLPCHK',  None,          'Peptide flip',                                              'Peptide flip'),
            (RES_LEVEL, 'H2OCHK',  None,          'Water check',                                               'Water check'),
            (RES_LEVEL, 'H2OHBO',  None,          'Water Hydrogen bond',                                       'Water Hydrogen bond'),
            (RES_LEVEL, 'HNQCHK',  None,          'Flip HIS GLN ASN hydrogen-bonds',                           'Flip HIS GLN ASN hydrogen-bonds'),
            (RES_LEVEL, 'Hand',    None,          '(Pro-)chirality or handness check',                         'Handness'),
            (RES_LEVEL, 'INOCHK', 'accessibilities','Accessibility',                                             'Accessibility Z.'),
            (RES_LEVEL, 'NAMCHK',  None,          'Atom names',                                                'Atom names'),
            (RES_LEVEL, 'NOCAAA',  None,          'Non-canonical residue',                                     'Non-canonical residue'),
            (RES_LEVEL, 'NQACHK', 'packingQuality2','2nd generation packing quality',                          'New quality'),
            (RES_LEVEL, 'NTCHK',   None,          'Acid group conformation check',                             'COOH check'),
            (RES_LEVEL, 'OMECHK', 'omegas',       'Omega angle restraints',                                    'Omega check'),
            (RES_LEVEL, 'PC2CHK',  None,          'Proline puckers',                                           'Proline puckers'),
            (RES_LEVEL, 'PDBLST',  None,          'List of residues',                                          'List of residues'),
            (RES_LEVEL, 'PL3CHK',  None,          'Side chain planarity with hydrogens attached',              'NA planarity'),
            (RES_LEVEL, 'PLNCHK', 'planarities',  'Protein side chain planarities',                            'Protein SC planarity'),
            (RES_LEVEL, 'PRECHK',  None,          'Missing backbone atoms.',                                   'Missing backbone atoms.'),
            (RES_LEVEL, 'PUCCHK',  None,          'Ring puckering in Prolines',                                'Ring puckering in Prolines'),
            (RES_LEVEL, 'QUACHK', 'packingQuality1','Directional Atomic Contact Analysis, aka 1st generation packing quality', 'Packing quality'),
            (RES_LEVEL, 'RAMCHK', 'ramachandran', 'Ramachandran Z-score',                                      'Ramachandr.' ),
            (RES_LEVEL, 'ROTCHK', 'rotamer',      'Rotamers',                                                  'Rotamer normality'),
            (RES_LEVEL, 'SCOLST',  None,          'List of symmetry contacts',                                 'List of symmetry contacts'),
            (RES_LEVEL, 'TO2CHK',  None,          'Missing C-terminal groups',                                 'Missing C-terminal groups'),
            (RES_LEVEL, 'TOPPOS',  None,          'Ligand without know topology',                              'Ligand without know topology'),
            (RES_LEVEL, 'TORCHK',  None,          'Unknown check',                                             'Unknown check'),
            (RES_LEVEL, 'WIOPAC',  None,          'Water packing',                                              'Water packing'),

            (PROJECT_LEVEL, 'BBCCHK', 'bbNormality',  'Backbone normality Z-score',                                'Backbone normality' ),
            (PROJECT_LEVEL, 'BNDCHK', 'bondLengths',  'Bond lengths',                                              'Bond lengths'),
#            (RES_LEVEL, 'BVALST',  None,          'B-Factors',                                                 'B-Factors'),
#            (RES_LEVEL, 'C12CHK', 'janin',        'Janin',                                                     'Janin Z'),
#            (RES_LEVEL, 'CCOCHK',  None,          'Inter-chain connection check',                              'Inter-chain connection check'),
#            (RES_LEVEL, 'EXTO2',   None,          'Test for extra OXTs',                                       'Test for extra OXTs'),
#            (RES_LEVEL, 'FATAL',   None,          'Fatal errors',                                              'Unknown check'), # new in Version  : 8.0 (20091126-0948)
#            (RES_LEVEL, 'FLPCHK',  None,          'Peptide flip',                                              'Peptide flip'),
#            (RES_LEVEL, 'H2OCHK',  None,          'Water check',                                               'Water check'),
#            (RES_LEVEL, 'H2OHBO',  None,          'Water Hydrogen bond',                                       'Water Hydrogen bond'),
#            (RES_LEVEL, 'HNQCHK',  None,          'Flip HIS GLN ASN hydrogen-bonds',                           'Flip HIS GLN ASN hydrogen-bonds'),
#            (RES_LEVEL, 'Hand',    None,          '(Pro-)chirality or handness check',                         'Handness'),
#            (RES_LEVEL, 'INOCHK', 'accessibilities','Accessibility',                                             'Accessibility Z.'),
#            (RES_LEVEL, 'NAMCHK',  None,          'Atom names',                                                'Atom names'),
#            (RES_LEVEL, 'NOCAAA',  None,          'Non-canonical residue',                                     'Non-canonical residue'),
#            (RES_LEVEL, 'NQACHK', 'packingQuality2','2nd generation packing quality',                          'New quality'),
#            (RES_LEVEL, 'NTCHK',   None,          'Acid group conformation check',                             'COOH check'),
#            (RES_LEVEL, 'OMECHK', 'omegas',       'Omega angle restraints',                                    'Omega check'),
#            (RES_LEVEL, 'PC2CHK',  None,          'Proline puckers',                                           'Proline puckers'),
#            (RES_LEVEL, 'PDBLST',  None,          'List of residues',                                          'List of residues'),
#            (RES_LEVEL, 'PL3CHK',  None,          'Side chain planarity with hydrogens attached',              'NA planarity'),
#            (RES_LEVEL, 'PLNCHK', 'planarities',  'Protein side chain planarities',                            'Protein SC planarity'),
#            (RES_LEVEL, 'PRECHK',  None,          'Missing backbone atoms.',                                   'Missing backbone atoms.'),
#            (RES_LEVEL, 'PUCCHK',  None,          'Ring puckering in Prolines',                                'Ring puckering in Prolines'),
#            (RES_LEVEL, 'QUACHK', 'packingQuality1','Directional Atomic Contact Analysis, aka 1st generation packing quality', 'Packing quality'),
#            (RES_LEVEL, 'RAMCHK', 'ramachandran', 'Ramachandran Z-score',                                      'Ramachandr.' ),
#            (RES_LEVEL, 'ROTCHK', 'rotamer',      'Rotamers',                                                  'Rotamer normality'),
#            (RES_LEVEL, 'SCOLST',  None,          'List of symmetry contacts',                                 'List of symmetry contacts'),
#            (RES_LEVEL, 'TO2CHK',  None,          'Missing C-terminal groups',                                 'Missing C-terminal groups'),
#            (RES_LEVEL, 'TOPPOS',  None,          'Ligand without know topology',                              'Ligand without know topology'),
#            (RES_LEVEL, 'TORCHK',  None,          'Unknown check',                                             'Unknown check'),
#            (RES_LEVEL, 'WIOPAC',  None,          'Water packing',                                              'Water packing')
]

cingNameDict  = NTdict( zip( nTzap(nameDefs,1), nTzap(nameDefs,2)) )
nameDict      = NTdict( zip( nTzap(nameDefs,1), nTzap(nameDefs,3)) )
shortNameDict = NTdict( zip( nTzap(nameDefs,1), nTzap(nameDefs,4)) )
cingNameDict.keysformat()
nameDict.keysformat()
shortNameDict.keysformat()

wiPlotList = []
# GV: moved to outer level to not always call createHtmlWhatif
wiPlotList.append( ('_01_backbone_chi','QUA/RAM/BBC/C12') )
wiPlotList.append( ('_02_bond_angle','BND/ANG/NQA/PLNCHK') )
wiPlotList.append( ('_03_steric_acc_flip','BMP/ACC/FLP/CHI') )


# Whatif id's for summary; will be keys in molecule[WHATIF_STR] dict
# Make them available to 'outside world through the Whatif class
summaryCheckIdList = [ QUACHK_STR, NQACHK_STR, RAMCHK_STR, C12CHK_STR, BBCCHK_STR, # First part
                       BNDCHK_STR, ANGCHK_STR, OMECHK_STR, PLNCHK_STR, HNDCHK_STR, INOCHK_STR  # second part.
                     ]


def cingCheckId( checkId ):
    """
    Static method to return a cingId if exists. Returns checkId otherwise.
    """
    if cingNameDict.has_key(checkId) and cingNameDict[checkId] != None:
        return cingNameDict[checkId]
    return checkId
#end def
#cingCheckId = staticmethod( cingCheckId )
