<SML> 0.24

#=======================================================================
#             	name     convention
<ResidueDef>  	G        INTERNAL_1
#=======================================================================
	commonName = 'RGUA'
	shortName  = 'g'
	comment    = 'guanine'
	nameDict   = {'CCPN': 'RNA G prot:H1;deprot:H7', 'INTERNAL_0': 'RGUA', 'CYANA': 'RGUA', 'CYANA2': 'RGUA', 'INTERNAL_1': 'G', 'IUPAC': 'G', 'AQUA': 'G', 'BMRBd': 'RGUA', 'XPLOR': 'RGUA', 'PDB': 'RGUA'}
	properties = ['nucleic', 'RNA']

	dihedrals  = <NTlist>
	#---------------------------------------------------------------
	<DihedralDef> ALPHA   
	#---------------------------------------------------------------
		atoms    = [(-1, "O3'"), (0, 'P'), (0, "O5'"), (0, "C5'")]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> BETA    
	#---------------------------------------------------------------
		atoms    = [(0, 'P'), (0, "O5'"), (0, "C5'"), (0, "C4'")]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> GAMMA   
	#---------------------------------------------------------------
		atoms    = [(0, "O5'"), (0, "C5'"), (0, "C4'"), (0, "C3'")]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> DELTA   
	#---------------------------------------------------------------
		atoms    = [(0, "C5'"), (0, "C4'"), (0, "C3'"), (0, "O3'")]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> EPSILON 
	#---------------------------------------------------------------
		atoms    = [(0, "C4'"), (0, "C3'"), (0, "O3'"), (1, 'P')]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> ZETA    
	#---------------------------------------------------------------
		atoms    = [(0, "C3'"), (0, "O3'"), (1, 'P'), (1, "O5'")]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> NU0     
	#---------------------------------------------------------------
		atoms    = [(0, "C4'"), (0, "O4'"), (0, "C1'"), (0, "C2'")]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> NU1     
	#---------------------------------------------------------------
		atoms    = [(0, "O4'"), (0, "C1'"), (0, "C2'"), (0, "C3'")]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> NU2     
	#---------------------------------------------------------------
		atoms    = [(0, "C1'"), (0, "C2'"), (0, "C3'"), (0, "C4'")]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> NU3     
	#---------------------------------------------------------------
		atoms    = [(0, "C2'"), (0, "C3'"), (0, "C4'"), (0, "O4'")]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> NU4     
	#---------------------------------------------------------------
		atoms    = [(0, "C3'"), (0, "C4'"), (0, "O4'"), (0, "C1'")]
		karplus  = None
	</DihedralDef>
	#---------------------------------------------------------------
	<DihedralDef> CHI     
	#---------------------------------------------------------------
		atoms    = [(0, "O4'"), (0, "C1'"), (0, 'N9'), (0, 'C4')]
		karplus  = None
	</DihedralDef>
	</NTlist>

	atoms      = <NTlist>
	#---------------------------------------------------------------
	<AtomDef> P       
	#---------------------------------------------------------------
		topology   = [(-1, "O3'"), (0, 'OP1'), (0, 'OP2'), (0, "O5'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'P', 'INTERNAL_0': 'P', 'CYANA': 'P', 'CYANA2': 'P', 'INTERNAL_1': 'P', 'IUPAC': 'P', 'AQUA': 'P', 'BMRBd': None, 'XPLOR': 'P', 'PDB': None}
		aliases    = []
		type       = 'P_ALI'
		spinType   = '31P'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isBackbone', 'backbone', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> OP1     
	#---------------------------------------------------------------
		topology   = [(0, 'P')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'OP1', 'INTERNAL_0': 'OP1', 'CYANA': 'OP1', 'CYANA2': 'OP1', 'INTERNAL_1': 'OP1', 'IUPAC': 'OP1', 'AQUA': 'OP1', 'BMRBd': None, 'XPLOR': 'O1P', 'PDB': None}
		aliases    = []
		type       = 'O_BYL'
		spinType   = '16O'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> OP2     
	#---------------------------------------------------------------
		topology   = [(0, 'P')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'OP2', 'INTERNAL_0': 'OP2', 'CYANA': 'OP2', 'CYANA2': 'OP2', 'INTERNAL_1': 'OP2', 'IUPAC': 'OP2', 'AQUA': 'OP2', 'BMRBd': None, 'XPLOR': 'O2P', 'PDB': None}
		aliases    = []
		type       = 'O_BYL'
		spinType   = '16O'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> O5'     
	#---------------------------------------------------------------
		topology   = [(0, 'P'), (0, "C5'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "O5'", 'INTERNAL_0': "O5'", 'CYANA': "O5'", 'CYANA2': "O5'", 'INTERNAL_1': "O5'", 'IUPAC': "O5'", 'AQUA': "O5'", 'BMRBd': None, 'XPLOR': "O5'", 'PDB': None}
		aliases    = []
		type       = 'O_EST'
		spinType   = '16O'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isBackbone', 'backbone', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> C5'     
	#---------------------------------------------------------------
		topology   = [(0, "O5'"), (0, "H5'"), (0, "H5''"), (0, "C4'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "C5'", 'INTERNAL_0': "C5'", 'CYANA': "C5'", 'CYANA2': "C5'", 'INTERNAL_1': "C5'", 'IUPAC': "C5'", 'AQUA': "C5'", 'BMRBd': None, 'XPLOR': "C5'", 'PDB': None}
		aliases    = []
		type       = 'C_ALI'
		spinType   = '13C'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isCarbon', 'carbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isBackbone', 'backbone', 'isMethylene', 'methylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> H5'     
	#---------------------------------------------------------------
		topology   = [(0, "C5'")]
		real       = []
		pseudo     = "Q5'"
		nameDict   = {'CCPN': "H5'", 'INTERNAL_0': "H5'", 'CYANA': "H5'", 'CYANA2': "H5'", 'INTERNAL_1': "H5'", 'IUPAC': "H5'", 'AQUA': "H5'", 'BMRBd': None, 'XPLOR': "H5'", 'PDB': None}
		aliases    = []
		type       = 'H_ALI'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasPseudoAtom', 'haspseudoatom', 'isMethylene', 'methylene', 'isMethyleneProton', 'methyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> H5''    
	#---------------------------------------------------------------
		topology   = [(0, "C5'")]
		real       = []
		pseudo     = "Q5'"
		nameDict   = {'CCPN': "H5''", 'INTERNAL_0': 'H5"', 'CYANA': 'H5"', 'CYANA2': 'H5"', 'INTERNAL_1': "H5''", 'IUPAC': "H5''", 'AQUA': "H5''", 'BMRBd': None, 'XPLOR': "H5''", 'PDB': None}
		aliases    = ["H5''", 'H5"']
		type       = 'H_ALI'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasPseudoAtom', 'haspseudoatom', 'isMethylene', 'methylene', 'isMethyleneProton', 'methyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> Q5'     
	#---------------------------------------------------------------
		topology   = []
		real       = ["H5'", "H5''"]
		pseudo     = None
		nameDict   = {'CCPN': "H5'*", 'INTERNAL_0': "Q5'", 'CYANA': "Q5'", 'CYANA2': "Q5'", 'INTERNAL_1': "Q5'", 'IUPAC': "Q5'", 'AQUA': "Q5'", 'BMRBd': None, 'XPLOR': "Q5'", 'PDB': None}
		aliases    = []
		type       = 'PSEUD'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isPseudoAtom', 'pseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> C4'     
	#---------------------------------------------------------------
		topology   = [(0, "C5'"), (0, "H4'"), (0, "C3'"), (0, "O4'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "C4'", 'INTERNAL_0': "C4'", 'CYANA': "C4'", 'CYANA2': "C4'", 'INTERNAL_1': "C4'", 'IUPAC': "C4'", 'AQUA': "C4'", 'BMRBd': None, 'XPLOR': "C4'", 'PDB': None}
		aliases    = []
		type       = 'C_ALI'
		spinType   = '13C'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isCarbon', 'carbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isBackbone', 'backbone', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> H4'     
	#---------------------------------------------------------------
		topology   = [(0, "C4'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "H4'", 'INTERNAL_0': "H4'", 'CYANA': "H4'", 'CYANA2': "H4'", 'INTERNAL_1': "H4'", 'IUPAC': "H4'", 'AQUA': "H4'", 'BMRBd': None, 'XPLOR': "H4'", 'PDB': None}
		aliases    = []
		type       = 'H_ALI'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> C3'     
	#---------------------------------------------------------------
		topology   = [(0, "C4'"), (0, "H3'"), (0, "C2'"), (0, "O3'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "C3'", 'INTERNAL_0': "C3'", 'CYANA': "C3'", 'CYANA2': "C3'", 'INTERNAL_1': "C3'", 'IUPAC': "C3'", 'AQUA': "C3'", 'BMRBd': None, 'XPLOR': "C3'", 'PDB': None}
		aliases    = []
		type       = 'C_ALI'
		spinType   = '13C'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isCarbon', 'carbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isBackbone', 'backbone', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> H3'     
	#---------------------------------------------------------------
		topology   = [(0, "C3'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "H3'", 'INTERNAL_0': "H3'", 'CYANA': "H3'", 'CYANA2': "H3'", 'INTERNAL_1': "H3'", 'IUPAC': "H3'", 'AQUA': "H3'", 'BMRBd': None, 'XPLOR': "H3'", 'PDB': None}
		aliases    = []
		type       = 'H_ALI'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> C2'     
	#---------------------------------------------------------------
		topology   = [(0, "C3'"), (0, "H2'"), (0, "O2'"), (0, "C1'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "C2'", 'INTERNAL_0': "C2'", 'CYANA': "C2'", 'CYANA2': "C2'", 'INTERNAL_1': "C2'", 'IUPAC': "C2'", 'AQUA': "C2'", 'BMRBd': None, 'XPLOR': "C2'", 'PDB': None}
		aliases    = []
		type       = 'C_ALI'
		spinType   = '13C'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isCarbon', 'carbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> H2'     
	#---------------------------------------------------------------
		topology   = [(0, "C2'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "H2'", 'INTERNAL_0': "H2'", 'CYANA': "H2'", 'CYANA2': "H2'", 'INTERNAL_1': "H2'", 'IUPAC': "H2'", 'AQUA': "H2'", 'BMRBd': None, 'XPLOR': "H2'", 'PDB': None}
		aliases    = []
		type       = 'H_ALI'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> O2'     
	#---------------------------------------------------------------
		topology   = [(0, "C2'"), (0, "HO2'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "O2'", 'INTERNAL_0': "O2'", 'CYANA': "O2'", 'CYANA2': "O2'", 'INTERNAL_1': "O2'", 'IUPAC': "O2'", 'AQUA': "O2'", 'BMRBd': None, 'XPLOR': "O2'", 'PDB': None}
		aliases    = []
		type       = 'O_HYD'
		spinType   = '16O'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> HO2'    
	#---------------------------------------------------------------
		topology   = [(0, "O2'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "HO2'", 'INTERNAL_0': "HO2'", 'CYANA': "HO2'", 'CYANA2': "HO2'", 'INTERNAL_1': "HO2'", 'IUPAC': "HO2'", 'AQUA': "HO2'", 'BMRBd': None, 'XPLOR': "HO2'", 'PDB': None}
		aliases    = []
		type       = 'H_OXY'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> C1'     
	#---------------------------------------------------------------
		topology   = [(0, "C2'"), (0, "H1'"), (0, "O4'"), (0, 'N9')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "C1'", 'INTERNAL_0': "C1'", 'CYANA': "C1'", 'CYANA2': "C1'", 'INTERNAL_1': "C1'", 'IUPAC': "C1'", 'AQUA': "C1'", 'BMRBd': None, 'XPLOR': "C1'", 'PDB': None}
		aliases    = []
		type       = 'C_ALI'
		spinType   = '13C'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isCarbon', 'carbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> H1'     
	#---------------------------------------------------------------
		topology   = [(0, "C1'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "H1'", 'INTERNAL_0': "H1'", 'CYANA': "H1'", 'CYANA2': "H1'", 'INTERNAL_1': "H1'", 'IUPAC': "H1'", 'AQUA': "H1'", 'BMRBd': None, 'XPLOR': "H1'", 'PDB': None}
		aliases    = []
		type       = 'H_ALI'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> O4'     
	#---------------------------------------------------------------
		topology   = [(0, "C4'"), (0, "C1'")]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "O4'", 'INTERNAL_0': "O4'", 'CYANA': "O4'", 'CYANA2': "O4'", 'INTERNAL_1': "O4'", 'IUPAC': "O4'", 'AQUA': "O4'", 'BMRBd': None, 'XPLOR': "O4'", 'PDB': None}
		aliases    = []
		type       = 'O_EST'
		spinType   = '16O'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> N9      
	#---------------------------------------------------------------
		topology   = [(0, "C1'"), (0, 'C4'), (0, 'C8')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'N9', 'INTERNAL_0': 'N9', 'CYANA': 'N9', 'CYANA2': 'N9', 'INTERNAL_1': 'N9', 'IUPAC': 'N9', 'AQUA': 'N9', 'BMRBd': None, 'XPLOR': 'N9', 'PDB': None}
		aliases    = []
		type       = 'N_AMI'
		spinType   = '15N'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNitrogen', 'nitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> C4      
	#---------------------------------------------------------------
		topology   = [(0, 'N9'), (0, 'N3'), (0, 'C5')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'C4', 'INTERNAL_0': 'C4', 'CYANA': 'C4', 'CYANA2': 'C4', 'INTERNAL_1': 'C4', 'IUPAC': 'C4', 'AQUA': 'C4', 'BMRBd': None, 'XPLOR': 'C4', 'PDB': None}
		aliases    = []
		type       = 'C_ARO'
		spinType   = '13C'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isCarbon', 'carbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> N3      
	#---------------------------------------------------------------
		topology   = [(0, 'C4'), (0, 'C2')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'N3', 'INTERNAL_0': 'N3', 'CYANA': 'N3', 'CYANA2': 'N3', 'INTERNAL_1': 'N3', 'IUPAC': 'N3', 'AQUA': 'N3', 'BMRBd': None, 'XPLOR': 'N3', 'PDB': None}
		aliases    = []
		type       = 'N_AMI'
		spinType   = '15N'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNitrogen', 'nitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> C2      
	#---------------------------------------------------------------
		topology   = [(0, 'N3'), (0, 'N2'), (0, 'N1')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'C2', 'INTERNAL_0': 'C2', 'CYANA': 'C2', 'CYANA2': 'C2', 'INTERNAL_1': 'C2', 'IUPAC': 'C2', 'AQUA': 'C2', 'BMRBd': None, 'XPLOR': 'C2', 'PDB': None}
		aliases    = []
		type       = 'C_ARO'
		spinType   = '13C'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isCarbon', 'carbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> N2      
	#---------------------------------------------------------------
		topology   = [(0, 'C2'), (0, 'H21'), (0, 'H22')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'N2', 'INTERNAL_0': 'N2', 'CYANA': 'N2', 'CYANA2': 'N2', 'INTERNAL_1': 'N2', 'IUPAC': 'N2', 'AQUA': 'N2', 'BMRBd': None, 'XPLOR': 'N2', 'PDB': None}
		aliases    = []
		type       = 'N_AMI'
		spinType   = '15N'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNitrogen', 'nitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> H21     
	#---------------------------------------------------------------
		topology   = [(0, 'N2')]
		real       = []
		pseudo     = 'Q2'
		nameDict   = {'CCPN': 'H21', 'INTERNAL_0': 'H21', 'CYANA': 'H21', 'CYANA2': 'H21', 'INTERNAL_1': 'H21', 'IUPAC': 'H21', 'AQUA': 'H21', 'BMRBd': None, 'XPLOR': 'H21', 'PDB': None}
		aliases    = []
		type       = 'H_AMI'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasPseudoAtom', 'haspseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> H22     
	#---------------------------------------------------------------
		topology   = [(0, 'N2')]
		real       = []
		pseudo     = 'Q2'
		nameDict   = {'CCPN': 'H22', 'INTERNAL_0': 'H22', 'CYANA': 'H22', 'CYANA2': 'H22', 'INTERNAL_1': 'H22', 'IUPAC': 'H22', 'AQUA': 'H22', 'BMRBd': None, 'XPLOR': 'H22', 'PDB': None}
		aliases    = []
		type       = 'H_AMI'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasPseudoAtom', 'haspseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> Q2      
	#---------------------------------------------------------------
		topology   = []
		real       = ['H21', 'H22']
		pseudo     = None
		nameDict   = {'CCPN': 'H2*', 'INTERNAL_0': 'Q2', 'CYANA': 'Q2', 'CYANA2': 'Q2', 'INTERNAL_1': 'Q2', 'IUPAC': 'Q2', 'AQUA': 'Q2', 'BMRBd': None, 'XPLOR': 'Q2', 'PDB': None}
		aliases    = []
		type       = 'PSEUD'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isPseudoAtom', 'pseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> N1      
	#---------------------------------------------------------------
		topology   = [(0, 'C2'), (0, 'H1'), (0, 'C6')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'N1', 'INTERNAL_0': 'N1', 'CYANA': 'N1', 'CYANA2': 'N1', 'INTERNAL_1': 'N1', 'IUPAC': 'N1', 'AQUA': 'N1', 'BMRBd': None, 'XPLOR': 'N1', 'PDB': None}
		aliases    = []
		type       = 'N_AMI'
		spinType   = '15N'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNitrogen', 'nitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> H1      
	#---------------------------------------------------------------
		topology   = [(0, 'N1')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'H1', 'INTERNAL_0': 'H1', 'CYANA': 'H1', 'CYANA2': 'H1', 'INTERNAL_1': 'H1', 'IUPAC': 'H1', 'AQUA': 'H1', 'BMRBd': None, 'XPLOR': 'H1', 'PDB': None}
		aliases    = []
		type       = 'H_AMI'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> C6      
	#---------------------------------------------------------------
		topology   = [(0, 'N1'), (0, 'O6'), (0, 'C5')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'C6', 'INTERNAL_0': 'C6', 'CYANA': 'C6', 'CYANA2': 'C6', 'INTERNAL_1': 'C6', 'IUPAC': 'C6', 'AQUA': 'C6', 'BMRBd': None, 'XPLOR': 'C6', 'PDB': None}
		aliases    = []
		type       = 'C_ARO'
		spinType   = '13C'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isCarbon', 'carbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> O6      
	#---------------------------------------------------------------
		topology   = [(0, 'C6')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'O6', 'INTERNAL_0': 'O6', 'CYANA': 'O6', 'CYANA2': 'O6', 'INTERNAL_1': 'O6', 'IUPAC': 'O6', 'AQUA': 'O6', 'BMRBd': None, 'XPLOR': 'O6', 'PDB': None}
		aliases    = []
		type       = 'O_BYL'
		spinType   = '16O'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> C5      
	#---------------------------------------------------------------
		topology   = [(0, 'C4'), (0, 'C6'), (0, 'N7')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'C5', 'INTERNAL_0': 'C5', 'CYANA': 'C5', 'CYANA2': 'C5', 'INTERNAL_1': 'C5', 'IUPAC': 'C5', 'AQUA': 'C5', 'BMRBd': None, 'XPLOR': 'C5', 'PDB': None}
		aliases    = []
		type       = 'C_ARO'
		spinType   = '13C'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isCarbon', 'carbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> N7      
	#---------------------------------------------------------------
		topology   = [(0, 'C5'), (0, 'C8')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'N7', 'INTERNAL_0': 'N7', 'CYANA': 'N7', 'CYANA2': 'N7', 'INTERNAL_1': 'N7', 'IUPAC': 'N7', 'AQUA': 'N7', 'BMRBd': None, 'XPLOR': 'N7', 'PDB': None}
		aliases    = []
		type       = 'N_AMI'
		spinType   = '15N'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNitrogen', 'nitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> C8      
	#---------------------------------------------------------------
		topology   = [(0, 'N9'), (0, 'N7'), (0, 'H8')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'C8', 'INTERNAL_0': 'C8', 'CYANA': 'C8', 'CYANA2': 'C8', 'INTERNAL_1': 'C8', 'IUPAC': 'C8', 'AQUA': 'C8', 'BMRBd': None, 'XPLOR': 'C8', 'PDB': None}
		aliases    = []
		type       = 'C_ARO'
		spinType   = '13C'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isCarbon', 'carbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> H8      
	#---------------------------------------------------------------
		topology   = [(0, 'C8')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': 'H8', 'INTERNAL_0': 'H8', 'CYANA': 'H8', 'CYANA2': 'H8', 'INTERNAL_1': 'H8', 'IUPAC': 'H8', 'AQUA': 'H8', 'BMRBd': None, 'XPLOR': 'H8', 'PDB': None}
		aliases    = []
		type       = 'H_ARO'
		spinType   = '1H'
		shift      = None
		hetatm     = False
		properties = ['isProton', 'proton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	#---------------------------------------------------------------
	<AtomDef> O3'     
	#---------------------------------------------------------------
		topology   = [(0, 'C8'), (1, 'P')]
		real       = []
		pseudo     = None
		nameDict   = {'CCPN': "O3'", 'INTERNAL_0': "O3'", 'CYANA': "O3'", 'CYANA2': "O3'", 'INTERNAL_1': "O3'", 'IUPAC': "O3'", 'AQUA': "O3'", 'BMRBd': None, 'XPLOR': "O3'", 'PDB': None}
		aliases    = []
		type       = 'O_EST'
		spinType   = '16O'
		shift      = None
		hetatm     = False
		properties = ['isNotProton', 'notproton', 'isNotCarbon', 'notcarbon', 'isNotNitrogen', 'notnitrogen', 'isNotSulfur', 'isNotSulphur', 'notsulfur', 'notsulphur', 'isSidechain', 'sidechain', 'isNotAromatic', 'notaromatic', 'isNotMethyl', 'notmethyl', 'isNotMethylProton', 'notmethylproton', 'isNotPseudoAtom', 'notpseudoatom', 'hasNoPseudoAtom', 'hasnopseudoatom', 'isBackbone', 'backbone', 'isNotMethylene', 'notmethylene', 'isNotMethyleneProton', 'notmethyleneproton']
	</AtomDef>
	</NTlist>
</ResidueDef>
#=======================================================================
</SML>
