"""
Constants definitions
"""

#__author__ = 'geerten'
__author__ = 'jurgen'


CING       = 'CING'
CING_STR   = CING


# 0.11+ is iPython version 2.
IPYTHON_VERSION_A = 'iPythonVersion_A'
IPYTHON_VERSION_B = 'iPythonVersion_B'


ERROR_ID = "ERROR"
WARNING_ID = "WARNING"
MESSAGE_ID = "MESSAGE"
DEBUG_ID = "DEBUG"
STEREO_ASSIGN_FILENAME_STR = 'stereo_assign.str'
PLEASE_ADD_EXECUTABLE_HERE = "PLEASE_ADD_EXECUTABLE_HERE" # Keep the below in sync with the one in setupCing.py


# Nomenclature systems
AQUA       = 'AQUA'         # AQUA nomenclature; not up-to-date with BMRB DG/G difference.
IUPAC      = 'IUPAC'        # IUPAC Nomenclature
SPARKY     =  IUPAC         # Sparky nomenclature, amounts to IUPAC
CYANA      = 'CYANA'        # CYANA 1.x nomenclature
XEASY      = CYANA          # Xeasy nomenclature; amounts to CYANA
DYANA      = CYANA          # DYANA nomenclature; amounts to CYANA
CYANA2     = 'CYANA2'       # CYANA 2.x nomenclature
XPLOR      = 'XPLOR'        # XPLOR nomenclature
CNS        =  XPLOR         # CNS nomenclature; amounts to XPLOR
PDB        = 'PDB'          # Old (PDB2) nomenclature
INTERNAL_0 = 'INTERNAL_0'   # INTERNAL_0 is the first convention used: was based upon DYANA/CYANA1.x convention (Gly has HA1/2)
INTERNAL_1 = 'INTERNAL_1'   # INTERNAL_1 is the second convention used: IUPAC for IUPAC defined atoms, CYANA2 for non-IUPAC atoms
INTERNAL   = INTERNAL_1     # Current internal nomenclature (INTERNAL_0 or INTERNAL_1)
LOOSE      = 'LOOSE'        # "free' format
CCPN       = 'CCPN'         # CCPN nomenclature
nomenClatureConventions = [INTERNAL_0, INTERNAL_1, AQUA, IUPAC, CYANA, CYANA2, XPLOR, PDB, CCPN]


# axes
X_AXIS = 0
Y_AXIS = 1
Z_AXIS = 2
A_AXIS = 3


NaNstring           = "."

CONSENSUS_STR = 'consensus'
MAX_TRIES_UNIQUE_NAME = 99999

# No shift value for Xeasy.
NOSHIFT         =  999.000
NULL_STRING_DOT ='.'
EMPTY_STRING =''
# ranges definitions. NB: a None value for ranges in function calls will cause CING to pick ranges up from molecule.ranges.
EMPTY_RANGES_STR = NULL_STRING_DOT
CV_RANGES_STR = 'cv'
AUTO_RANGES_STR = 'auto'
ALL_RANGES_STR = 'all'
LIMIT_RANGES = 0.7

# PLUGINS
IS_INSTALLED_STR = 'isInstalled'
PARSED_STR = 'parsed'
COMPLETED_STR = 'completed'
dots   = '-----------'               #: 11 dashes
dots20 = '--------------------'      #: 20 dashes inlined for efficiency?



SYMMETRY_C1_STR = 'SYMMETRY_C1' # No symmetry or undetermined. Use None for unknown.
SYMMETRY_C2_STR = 'SYMMETRY_C2' # Homodimer such as 1hue
SYMMETRY_C3_STR = 'SYMMETRY_C3' #
SYMMETRY_C5_STR = 'SYMMETRY_C5' # 2kyv all helical
SYMMETRY_D2_STR = 'SYMMETRY_D2' # 1olg  No symmetry

# In NMR the symmetry is not always enfoced so really these cutoffs have little use.
SYMMETRY_NCS_CUTOFF = 10.0 # angstrom. E.g. 1hue: 4.6                   1dum: 0.7. ONly bb used and no protons.
SYMMETRY_DR_CUTOFF  = 10.0 # angstrom. E.g. 1hue: 2.2 (not enforced)    1dum: 0.3 # averaged over all models.

MIN_DISTANCE_ANY_ATOM_PAIR = 1.8
# Needs to be one word for otherwise the restore failed.
THEORETICAL_RESTRAINT_LIST_STR = "theoreticalRestraintList"

FASTA_UNCOMMON_RESIDUE_STR = 'X'

CYANA_NON_RESIDUES = ['PL','LL2','link']

# Color labels for HTML/CSS output
COLOR_RED    = 'red'
COLOR_GREEN  = 'green'
COLOR_ORANGE = 'orange'

EPSILON_RESTRAINT_VALUE_FLOAT = 1.e-5

# For criteria implementation.
OPERATION_EQUALS                 = '=='
OPERATION_LESS_THAN_OR_EQUALS    = '<='
OPERATION_GREATER_THAN_OR_EQUALS = '>='
OPERATION_LESS_THAN              = '<'
OPERATION_GREATER_THAN           = '>'
OPERATION_IN                     = 'in'
OPERATION_OUT                    = 'out'

ATOM_LEVEL     = 'ATOM'
RES_LEVEL      = 'RESIDUE'
CHAIN_LEVEL    = 'CHAIN'
#MOLECULE_LEVEL = 'MOLECULE'
PROJECT_LEVEL  = 'PROJECT' # use project only.
CSL_LEVEL      = 'CSL'               # cingresonancelist
CSLPA_LEVEL    = 'CSL_PER_ATOMCLASS' # cingresonancelistperatomclass

ATOM_STR = 'atom'
ATOMS_STR = 'atoms'
RES_STR = 'res'
CHAIN_STR = 'chain'
MOLECULE_STR = 'molecule'
PROJECT_STR = 'project'
#ATOMS_STR = 'atoms'
COORDINATES_STR = 'coordinates'
DIHEDRAL_STR = 'dihedral'
DIHEDRALS_STR = 'dihedrals'

ANY_ENTITY_LEVEL = 'ANY_ENTITY'

DR_LEVEL       = 'DistanceRestraint'
DRL_LEVEL      = 'DistanceRestraintList'
DRL_STR      = 'DRL'
HBR_LEVEL = 'HBondRestraint' # Alternative for hydrogen bond restraints where in CCPN another name is used.
HBRL_LEVEL = 'HBondRestraintList'
AC_LEVEL = 'DihedralRestraint'
ACL_LEVEL = 'DihedralRestraintList'
ACL_STR      = 'ACL'
RDC_LEVEL = 'RDCRestraint'
RDCL_LEVEL = 'RDCRestraintList'
RDCL_STR      = 'RDCL'
RESONANCE_LEVEL = 'Resonance'
RESONANCEL_LEVEL = 'ResonanceList'
RESONANCEL_STR      = 'RESONANCEL'
COPLANAR_LEVEL = 'Coplanar'
COPLANARL_LEVEL = 'CoplanarList'
DIHEDRAL_BY_PROJECT_LEVEL = 'DihedralByProject'
DIHEDRALL_BY_PROJECT_LEVEL = 'DihedralByProjectList' # unused?
DIHEDRAL_BY_RESIDUE_STR = 'DihedralByResidue'

SUMMARY_STR = 'summary'

INPUT_STR = 'input' # To files like $D/NRG-CING/input/br/1brv.tgz
DATA_STR = 'data' # mostly for NRG.
DB_STR = 'db'
COMMON_NAME_STR = 'commonName'
TYPE_STR = 'type' # db atom type
SPINTYPE_STR = 'spinType'
C_ALI_STR = 'C_ALI' # aliphatic db atom type
CA_STR = 'CA'
C1Prime_STR = "C1'"

DR_STR = 'distanceRestraints' # used as in residue.distanceRestraints
AC_STR = 'dihedralRestraints' # used as in residue.dihedralRestraints
VIOL1_STR = 'violCount1'
VIOL3_STR = 'violCount3'
VIOL5_STR = 'violCount5'

RESONANCES_STR = 'resonances'
RESONANCE_LIST_IDX_ANY = -999 # will match assignment in any resonance list.
MERGED_STR = 'merged'
RESONANCE_SOURCES_STR = 'resonanceSources'
STEREO_ASSIGNMENT_CORRECTIONS_STAR_STR = 'stereoAssignmentCorrectionsStar'
DISTANCE_RESTRAINT_LIST_HIGH_VIOLATIONS_FILTERED_STR = 'distance_restraint_list_high_violations_filtered.txt'

# SQL stuff
NAME_STR        = 'name'
RES_NAME_STR    = 'resName'
RES_NUMB_STR    = 'resNum'
NUMBER_STR      = 'number'
NAMEDICT_STR    = 'nameDict'

ARCHIVE_ID_STR  = 'archive_id'
PDB_ID_STR      = 'pdb_id'
BMRB_ID_STR     = 'bmrb_id'
BMRB_ENTRY_LIST_STR = 'bmrbEntryList'
PDB_ENTRY_LIST_STR  = 'pdbEntryList'
ENTRY_ID_STR    = 'entry_id'
CHAIN_ID_STR    = 'chain_id'
RESIDUE_ID_STR  = 'residue_id'
ATOM_ID_STR     = 'atom_id'
RES_COUNT_STR   = 'res_count'
MODEL_COUNT_STR = 'model_count'
ROG_STR         = 'rog'

OMEGA_DEV_AV_ALL_STR    = 'omega_dev_av_all'
CV_BACKBONE_STR         = 'cv_backbone'
CV_SIDECHAIN_STR        = 'cv_sidechain'
CHK_RAMACH_STR          = 'chk_ramach'
CHK_JANIN_STR           = 'chk_janin'
CHK_D1D2_STR            = 'chk_d1d2'
PHI_AVG_STR             = 'phi_avg'
PSI_AVG_STR             = 'psi_avg'
CHI1_AVG_STR            = 'chi1_avg'
CHI2_AVG_STR            = 'chi2_avg'
PHI_CV_STR              = 'phi_cv'
PSI_CV_STR              = 'psi_cv'
CHI1_CV_STR             = 'chi1_cv'
CHI2_CV_STR             = 'chi2_cv'

DISTANCE_COUNT_STR    = 'distance_count'
DIHEDRAL_COUNT_STR    = 'dihedral_count'
RDC_COUNT_STR         = 'rdc_count'
PEAK_COUNT_STR        = 'peak_count'
CS_COUNT_STR          = 'cs_count'
CS1H_COUNT_STR        = 'cs1H_count'
CS13C_COUNT_STR       = 'cs13C_count'
CS15N_COUNT_STR       = 'cs15N_count'

POOR_PROP = 'POOR'
BAD_PROP  = 'BAD'

CHARS_PER_LINE_OF_PROGRESS = 100

#PROTEIN_STR = 'protein' # duplicate
PHI_STR = 'PHI'
PSI_STR = 'PSI'
CHI1_STR = 'CHI1'
CHI2_STR = 'CHI2'
OMEGA_STR = 'OMEGA'
CV_STR = 'cv'
CAV_STR = 'cav'
S2_STR = 'S2' # used in TalosPlus. For the talosPlus variable see reqNih.py


DIHEDRAL_NAME_Cb4N = 'Cb4N'
DIHEDRAL_NAME_Cb4C = 'Cb4C'
GLY_HA3_NAME_CING = 'HA2'
range0_360 = [0.,360.]

DIHEDRAL_60_STR = 'DIHEDRAL_60' # gauche + Leu chi2
DIHEDRAL_180_STR = 'DIHEDRAL_180' # trans
DIHEDRAL_300_STR = 'DIHEDRAL_300' # gauche -

VALUE_LIST_STR   = "valueList" # Originally in reqWhatif.py
# Used for keying of residue entity (and potentially others) with CING's own Z-score values.
CHK_STR = 'CHK'
RAMACHANDRAN_CHK_STR = 'RAMACHANDRAN_CHK'
CHI1CHI2_CHK_STR = 'CHI1CHI2_CHK'
D1D2_CHK_STR = 'D1D2_CHK'

AUTO_STR = 'auto'
#RMSD_STR = 'rmsd' #duplicate
RANGES_STR = 'ranges'
RESNUM_STR = 'resNum'
VALUE_STR = "value"
ERROR_STR = "error"
BACKBONE_AVERAGE_STR = 'backboneAverage'
HEAVY_ATOM_AVERAGE_STR = 'heavyAtomsAverage'
QSHIFT_STR = 'Qshift'
ALL_ATOMS_STR = 'allAtoms'
BACKBONE_STR = 'backbone'
HEAVY_ATOMS_STR = 'heavyAtoms'
PROTONS_STR = 'protons'

# for RDB only:
RMSD_BACKBONE_STR = 'rmsd_backbone'
RMSD_SIDECHAIN_STR = 'rmsd_sidechain'
SEL1_STR = 'sel_1'
SEL2_STR = 'sel_2'
SEL3_STR = 'sel_3'
SEL4_STR = 'sel_4'
SEL5_STR = 'sel_5'

DIS_MAX_ALL_STR = 'dis_max_all'
DIS_RMS_ALL_STR = 'dis_rms_all'
DIS_AV_ALL_STR  = 'dis_av_all'
DIS_AV_VIOL_STR = 'dis_av_viol'
DIS_C1_VIOL_STR = 'dis_c1_viol'
DIS_C3_VIOL_STR = 'dis_c3_viol'
DIS_C5_VIOL_STR = 'dis_c5_viol'

DIH_MAX_ALL_STR = 'dih_max_all'
DIH_RMS_ALL_STR = 'dih_rms_all'
DIH_AV_ALL_STR  = 'dih_av_all'
DIH_AV_VIOL_STR = 'dih_av_viol'
DIH_C1_VIOL_STR = 'dih_c1_viol'
DIH_C3_VIOL_STR = 'dih_c3_viol'
DIH_C5_VIOL_STR = 'dih_c5_viol'

# in CING
VIOLMAXALL_STR = 'violMaxAll'
RMSD_STR       = 'rmsd' # see above.
VIOLAV_STR     = 'violAv'
VIOLAVALL_STR  = 'violAvAll'
VIOLCOUNT1_STR = 'violCount1'
VIOLCOUNT3_STR = 'violCount3'
VIOLCOUNT5_STR = 'violCount5'

# DB
QCS_ALL_STR = 'qcs_all'
QCS_BB_STR = 'qcs_bb'
QCS_HVY_STR = 'qcs_hvy'
QCS_PRT_STR = 'qcs_prt'

SCALE_BY_MAX = 'SCALE_BY_MAX' # Ramachandran
SCALE_BY_SUM = 'SCALE_BY_SUM' # D1D2
SCALE_BY_Z = 'SCALE_BY_Z' # D1D2 new
SCALE_BY_ONE = 'SCALE_BY_ONE' # NO scaling that is.
SCALE_BY_DEFAULT = SCALE_BY_MAX

MIN_PERCENTAGE_RAMA = 2.0  # This is a percentage of the MAX
MAX_PERCENTAGE_RAMA = 20.0
MIN_PERCENTAGE_D1D2 = 0.08 # This is a percentage of the SUM
MAX_PERCENTAGE_D1D2 = 0.2
MIN_Z_D1D2 = -1.0 # This is an absolute value of number of sigma's from average. NB, this is not a percentage
MAX_Z_D1D2 = 0.0

QshiftMinValue = 0.0
QshiftMaxValue = 0.05
QshiftReverseColorScheme = False

DS_STORE_STR = ".DS_Store" # A mac OSX file that should be ignored by CING.

ALL_CHAINS_STR = 'ALL_CHAINS'
MAX_SIZE_XPLOR_RESTRAINT_LIST_NAME = 10
#maxlength = 20 - len('viol.noe.')

# 2 Gb fails on Ubuntu 11.4 but 1500 Mb works.
JVM_MAX_MEM     = '1499m' # passed to Java using the -Xmx option. For now this is tied to 32 bitness.
JVM_TYPE        = '-d32'
JVM_HEADNESS    = '-Djava.awt.headless=true'
#JVM_CMD_STD     = '/local/tmp/jdk1.6.0_41/bin/java -Xmx%s %s %s' % ( JVM_MAX_MEM, JVM_TYPE, JVM_HEADNESS )
JVM_CMD_STD     = '/usr/bin/java -Xmx%s %s %s' % ( JVM_MAX_MEM, JVM_TYPE, JVM_HEADNESS )
#JVM_CMD_STD     = 'echo helloJvm; which java; ' + JVM_CMD_STD # DEFAULT OFF

#: Don't report on the next atoms
#: Add these to CING lib later. For now, it's just clobbering the output to report on them.
ATOM_LIST_TO_IGNORE_REPORTING = []
hideMissingAtomsJfdKnowsAbout = True # default should be False
if hideMissingAtomsJfdKnowsAbout:
    ATOM_LIST_TO_IGNORE_REPORTING = "H1 H2 H3 OXT ZN O' HO3' HO5' HOP2 HOP3 OP3".split(' ')

# Mol types as per CCPN defs.
PROTEIN_STR = 'protein'
DNA_STR = 'DNA'
RNA_STR = 'RNA'
WATER_STR = 'water'
HOH_STR = 'HOH'
OTHER_STR = 'other'

molTypeList = [ PROTEIN_STR, DNA_STR, RNA_STR, WATER_STR, OTHER_STR ]
mapMoltypeToInt = {PROTEIN_STR: 0, DNA_STR : 1, RNA_STR : 2, WATER_STR : 3, OTHER_STR: 4}

WATER_ATOM_COUNT = 4 # Including QH.

#----------------------------------------------------------------------
#required items for reqShiftx plugin
#----------------------------------------------------------------------
#'required items for this plugin for CING setup'
SHIFTX_STR       = "shiftx"

#----------------------------------------------------------------------
#required items for CCPN plugin
#----------------------------------------------------------------------
CCPN_STR = "Ccpn"
CCPN_LOWERCASE_STR = 'ccpn'

#----------------------------------------------------------------------
# Talos, from reqNih
#----------------------------------------------------------------------
#DEPRECIATED
TALOSPLUS_STR = "talosPlus" # key to the entities (status, atoms, residues, etc)
                            # under which the results will be stored
#NIH_STR = "nih" # key to the plugin
TALOSPLUS_CLASS_STR = 'classification'
NUMBER_OF_SD_TALOS = 2

# Needs to be one word for otherwise the restore failed.
TALOSPLUS_LIST_STR = "talos_plus_predicted_dihedrals"

#----------------------------------------------------------------------
# queeny, from reqQueeny
#----------------------------------------------------------------------
#DEPRECIATED
QUEENY_STR       = "queeny" # key to the entities (atoms, residues, etc under which the results will be stored

QUEENY_UNCERTAINTY1_STR = 'uncertainty1'  # Key used for residue's and atom's uncertainty after topology triangulation
QUEENY_UNCERTAINTY2_STR = 'uncertainty2'  # Key used for residue's and atom's uncertainty after restraint triangulation
QUEENY_INFORMATION_STR  = 'information'   # Key used for residue's and atom's information, calculated from uncertainty1 and uncertainty2

# RDB requires a little bit more specific qualifier; GWV?
RDB_QUEENY_UNCERTAINTY1_STR = 'queen_uncertainty1'
RDB_QUEENY_UNCERTAINTY2_STR = 'queen_uncertainty2'
RDB_QUEENY_INFORMATION_STR = 'queen_information'

#----------------------------------------------------------------------
# Whatif, from reqWhatif
#----------------------------------------------------------------------
#DEPRECIATED
WHATIF_STR       = "Whatif" # key to the entities (atoms, residues, etc under which the results will be stored

#----------------------------------------------------------------------
# Procheck, from reqProcheck
#----------------------------------------------------------------------
#DEPRECIATED
PROCHECK_STR       = "procheck" # key to the entities (atoms, residues, etc under which the results will be stored

#----------------------------------------------------------------------
# v3 key definitions
#----------------------------------------------------------------------

# Projects; used in Project.open routine
PROJECT_OLD         = 'old'             # open existing cing project
PROJECT_NEW         = 'new'             # create new cing project; overwrite any existing one
PROJECT_CREATE      = 'create'          # open old project if it exists, new project otherwise
PROJECT_NEWFROMCCPN = 'newFromCcpn'     # use new CCPN file to initialise data
PROJECT_OLDFROMCCPN = 'oldFromCcpn'     # use the stored CCPN data for restoring


# keys of different ValidationResult types
OBJECT_KEY          = 'object' # ValidationResult key for pointing at object
CING_KEY            = 'cing'
TALOSPLUS_KEY       = 'talosPlus'
QUEENY_KEY          = 'queeny'
SHIFTX_KEY          = 'shiftx'
WHATIF_KEY          = 'whatif'
DSSP_KEY            = 'dssp'
PROCHECK_KEY        = 'procheck'
WATTOS_KEY          = 'wattos'
VASCO_KEY           = 'vasco'
X3DNA_KEY           = 'x3dna'

VALIDATION_KEYS = [TALOSPLUS_KEY, QUEENY_KEY, SHIFTX_KEY, WHATIF_KEY, DSSP_KEY, PROCHECK_KEY,
                   WATTOS_KEY, VASCO_KEY, X3DNA_KEY]
# OS related
OS_TYPE_MAC         = 'darwin'
OS_TYPE_LINUX       = 'linux'
OS_TYPE_WINDOWS     = 'windows' # unsupported.
OS_TYPE_UNKNOWN     = 'unknown'

#----------------------------------------------------------------------
# convenience imports
#----------------------------------------------------------------------
# verbosity
from cing.constants import verbosity
# system related
from cing.constants.definitions import systemDefinitions as system
# code related
from cing.constants.definitions import cingDefinitions as code
# path related
from cing.constants.definitions import cingPaths as paths
# validation related
from cing.constants.definitions import validationSettings




