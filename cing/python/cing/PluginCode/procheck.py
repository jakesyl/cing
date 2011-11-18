"""
Adds procheck methods
----------------  Methods  ----------------


procheck( ranges=None   )


----------------  Attributes generated  ----------------


Molecule:
    procheck: <Procheck> object

Residue
    procheck: NTdict instance with procheck values for this residue
"""

from cing import cingPythonCingDir
from cing.Libs import disk
from cing.Libs.AwkLike import AwkLike
from cing.Libs.AwkLike import AwkLikeS
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Libs.disk import copy
from cing.PluginCode.required.reqProcheck import * #@UnusedWildImport
from cing.core.constants import * #@UnusedWildImport
from cing.core.parameters import PLEASE_ADD_EXECUTABLE_HERE
from cing.core.parameters import cingPaths
from glob import glob


if True: # block
    useModule = True
    if not cingPaths.aqpc:
#        nTdebug("Missing aqpc which is a dep for procheck")
        useModule = False
    elif not cingPaths.procheck_nmr:
#        nTdebug("Missing procheck_nmr which is a dep for procheck")
        useModule = False
    if not useModule:
        raise ImportWarning('procheck')
#    nTmessage('Using procheck')

#Trying to accommodate at least
#2k0e with 160 models of with each 148 residues, 2611 atoms
#1ai0
## Adjusted to reflect original procheck_nmr settings:
#
#C MXATOM - Maximum number of atoms allowed for the structure (1 model)
#was 50,000 in rmsdev, set to 100,000
#
#C MXCONS - Maximum number of NMR constraints that can be stored
#was  10,000 in mplot.inc, set to 100,000
#
#C MXRES  - Maximum number of residues allowed for the protein structure
#C          being plotted
#was 20,000 in tplot.inc, set to 200,000
#5,000 to 50,000 in mplot.inc etc.
#
#C MAXARR - Maximum size of constraints array
#was 120,000 in mplot.inc set to 1,200,000
#
#C MXRCON - Maximum number of distance restraints per residue
#was 500 left so.
#
#C MXFILE - Maximum number of .rin files allowed in the ensemble
#was 60, left because there are also other deps in .f code that hardcode a 60 dep.
#this limits cing/pc to 60
#
#MXONE 'Maximum number of residues per protein exceeded:',
#left at 10,000
#

def procheckString2float(string):
    """Convert a string to float, return None in case of value of 999.90"""
    result = float(string)
    if result > 999.8 and result < 999.99:
        return None
    return result

class ProcheckSummaryResult( NTdict ):
    """
    Class to store procheck results as obtained from the summary file

    keys:
        text:       unparsed text
        molecule:   Molecule instance
        ranges:     Ranges used
        core:       Percentage core residues
        allowed:    Percentage allowed residues
        generous:   Percentage generous residues
        disallowed: Percentage disallowed residues

    TODO: get a complete .sum file (bug in procheck compile) and parse it too (partially done).

    """
    def __init__(self, text, molecule, ranges=None):
        NTdict.__init__(self,
                        __CLASS__  = 'ProcheckSummaryResult',
                        molecule   = molecule,
                        ranges     = ranges,
                        text       = text,
                        __FORMAT__ = """
molecule:     %(molecule)s
ranges:       %(ranges)s
ramachandran
  core:       %(core)4.1f%%
  allowed:    %(allowed)4.1f%%
  generous:   %(generous)4.1f%%
  disallowed: %(disallowed)4.1f%%"""
                       )
        self.core      = None
        self.allowed   = None
        self.generous  = None
        self.disallowed= None

        self._parseText()
    #end def

    def _parseText(self):
        for line in AwkLikeS(self.text):
            if line.NF >= 2 and line.dollar[2] == 'Ramachandran':
                self.core      = float(line.dollar[4][:-1])
                self.allowed   = float(line.dollar[6][:-1])
                self.generous  = float(line.dollar[8][:-1])
                self.disallowed = float(line.dollar[10][:-1])
                break
            #end if
        #end for
        if self.core == None or self.allowed == None or self.generous == None or self.disallowed == None:
            nTerror("IN ProcheckSummaryResult Failed to parse Text as expected for self.text:\n%s" % self.text)
    #end def
#end class

class ProcheckResidueResult( NTdict ):
    """
    Class to store procheck per-residue results

    keys:
        gf:        G-factor
        gfCHI1:    G-factor CHI1
        gfCHI12:   G-factor CHI12
        gfPHIPSI:  G-factor PHI-PSI
        secStruct: NTlist instance with secondary structure indication per model
        consensus: consensus secondary structure derived from secStruct
    """
    def __init__(self, residue):
        NTdict.__init__(self,
                        __CLASS__  = 'ProcheckResidueResult',
                        residue    = residue,
                        gf         = None,
                        gfCHI1     = None,
                        gfCHI12    = None,
                        gfPHIPSI   = None,
                        secStruct  = NTlist(),
                        consensus  = None,
                        __FORMAT__ = \
dots + " procheck result %(residue)s " + dots + """
gf:                  %(gf)s
gfCHI1:              %(gfCHI1)s
gfCHI12:             %(gfCHI12)s
gfPHIPSI:            %(gfPHIPSI)s
secStruct:           %(secStruct)s
consensus:           %(consensus)s"""
                       )
#end class

class Procheck( NTdict ):
    """
    From Jurgen:

    Column id
    ^ Fortran variable
    ^ ^        Explanation
    ##############################
    ###################################################
    1 NXRES    residue number in procheck
    2 AA3      residue name
    3 BRKSYM   chain id as in PDB file
    4 SEQBCD   resdiue id as in PDB file??
    5 SUMMPL   secondary structure classification (DSSP?)
    6 MCANGS 1 phi
    7 MCANGS 2 psi
    8 MCANGS 3 omega
    9 SCANGS 1 chi 1
    0 SCANGS 2 chi 2
    1 SCANGS 3 chi 3
    2 SCANGS 4 chi 4
    3 HBONDE   Hydrogen bond energy
    4 DSDSTS ? statistics?
    5 MCANGS ?
    6 BVALUE   Crystallographic B factor
    7 MCBVAL   Mainchain B value
    8 SCBVAL   Sidechain B value
    9 OOIS 1 ?
    0 OOIS 2 ?
    1 MCBSTD Main chain bond standard deviation?
    2 SCBSTD Side chain bond standard deviation?


    #0000000000000000000000000000000000000000000000000000000000000000000000
                    phi   psi    omega  chi1   chi2   chi3   chi4   hb     dsdsts mcang
      55GLY A  62 T-147.73 -20.13-166.50 999.90 999.90 999.90 999.90  -0.87   0.00 999.90   0.00  0.000  0.000 11 38  0.000  0.000
      56ASP A  63 e -78.77 161.06-173.97 -56.24 -71.93 999.90 999.90  -0.76   0.00  34.42   0.00  0.000  0.000 13 50  0.000  0.000
      57ARG A  64 E-104.07 124.65 166.81 177.50-170.21 179.43-172.18  -2.12   0.00  37.30   0.00  0.000  0.000 12 56  0.000  0.000
      58VAL A  65 E -87.26 117.24 175.76-157.64 999.90 999.90 999.90  -3.33   0.00  33.46   0.00  0.000  0.000 14 67  0.000  0.000
      59LEU A  66 E -99.01 -36.19-179.02  50.71 149.42 999.90 999.90  -2.74   0.00  31.00   0.00  0.000  0.000 13 50  0.000  0.000
      95PRO!A 102   -69.35 999.90 999.90 -24.86 999.90 999.90 999.90   0.00   0.00  37.72   0.00  0.000  0.000  4 13  0.000  0.000
      96TYR!B 205   999.90 -55.02-171.34-143.34 -89.71 999.90 999.90   0.00   0.00  34.80   0.00  0.000  0.000  2  5  0.000  0.000
      97LEU B 206    61.37 179.80 171.30-145.66  66.98 999.90 999.90   0.00   0.00  31.07   0.00  0.000  0.000  3  5  0.000  0.000
        # 2hgh
      10GLY A 113    74.45  15.22 178.99 999.90 999.90 999.90 999.90  -0.95   0.00 999.90   0.00  0.000  0.000  9 20  0.000  0.000
      11LYS A 114 e -71.09 143.35-173.40-153.49 165.04 174.07  65.99   0.00   0.00  34.73   0.00  0.000  0.000  7 25  0.000  0.000
      12ALA A 115 E-123.24 137.51-174.84 999.90 999.90 999.90 999.90   0.00   0.00  34.69   0.00  0.000  0.000  9 22  0.000  0.000
      13PHE A 116 E-126.20 154.68 179.89 -49.13  80.54 999.90 999.90  -3.08   0.00  35.22   0.00  0.000  0.000 10 21  0.000  0.000
      14LYS A 117 S -66.93 -37.97-173.87-164.02 169.28-166.01  51.19   0.00   0.00  34.94   0.00  0.000  0.000  7 16  0.000  0.000
      15LYS A 118 h-135.63 148.98-170.06 -51.60 -73.02 152.83  37.49   0.00   0.00  34.76   0.00  0.000  0.000  8 19  0.000  0.000
      16HIS A 119 H -66.31 -28.97 177.00  52.90  58.00 999.90 999.90   0.00   0.00  34.07   0.00  0.000  0.000  8 24  0.000  0.000
      17ASN A 120 H -64.88 -30.42 173.13  18.31  58.33 999.90 999.90   0.00   0.00  33.97   0.00  0.000  0.000  7 30  0.000  0.000
      18GLN A 121 H -73.16 -37.55 175.47 -46.40-178.69 -71.05 999.90  -0.83   0.00  34.45   0.00  0.000  0.000  9 30  0.000  0.000
      19LEU A 122 H -61.95 -47.13 175.48 169.01  56.82 999.90 999.90  -1.43   0.00  34.90   0.00  0.000  0.000 13 31  0.000  0.000
      20LYS A 123 H -60.27 -39.32 175.72 -80.80-175.12 167.71 178.94  -2.93   0.00  34.60   0.00  0.000  0.000  9 36  0.000  0.000


    .edt file The contents of the .edt file are:

           FORMAT(A1,A5,A3,6(1X,F7.3),2(1X,F7.3),4(1X,F6.2))
           A1  -  Chain-id
           A5  -  Residue number
           A3  -  Residue name
         6F7.3 -  The 6 circular variance values for the phi, psi, chi1,
                  chi2, phi-psi and chi1-chi2 distributions.
         2F7.3 -  Main-chain and side-chain deviations of this residue
                  from the overall mean value
         4F6.2 -  The G-factors for the phi-psi, chi1-chi2, chi1 only,
                  and the overall average.
01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789
0    -    1         2         3         4         5         6         7    -    8         9         1
A 185 ALA   0.000   0.000 999.900 999.900   0.000 999.900   0.500   0.499   0.80 999.90 999.90   0.80
A 186 GLU   0.000   0.002   0.363   0.504   0.001   0.429   0.489   2.949  -0.66   0.75 999.90   0.04
A 187 CYS   0.002   0.000   0.000 999.900   0.001 999.900   0.591   0.585  -0.41 999.90   0.13  -0.14
A 188 HIS   0.001   0.041   0.001   0.000   0.020   0.001   0.836   0.494  -1.69   1.22 999.90  -0.24
A 189 GLN   0.243   0.071   0.164   0.660   0.153   0.362   1.840   6.256  -0.73  -1.05 999.90  -0.89
A 190 ASP   0.001 999.900   0.000   0.001 999.900   0.000   5.329   8.952 999.90  -1.14 999.90  -1.14
B   2 G   999.900 999.900 999.900 999.900 999.900 999.900   0.000   1.574 999.90 999.90 999.90   0.00
B   3 G   999.900 999.900 999.900 999.900 999.900 999.900   0.000   1.306 999.90 999.90 999.90   0.00
B   4 C   999.900 999.900 999.900 999.900 999.900 999.900   0.000   1.076 999.90 999.90 999.90   0.00
B   5 C   999.900 999.900 999.900 999.900 999.900 999.900   0.000   1.002 999.90 999.90 999.90   0.00
B   6 A   999.900 999.900 999.900 999.900 999.900 999.900   0.000   1.149 999.90 999.90 999.90   0.00
B   7 U   999.900 999.900 999.900 999.900 999.900 999.900   0.000   1.932 999.90 999.90 999.90   0.00


    """
    procheckEnsembleDefs = NTdict(
                          # Keep rucksack from filling up over the years.
    #   field       (startChar, endChar, conversionFunction, store)
#        line      = (  0,  4, int, False ), # unique residue id over all models in NMR ensemble. No need to capture.
        chain     = (0, 1, str, False),
        resNum    = (1, 5, int, False),
        resName   = (6, 9, str, False),
        # ignore 6 cv values and 2 deviation values.
        gfPHIPSI  = (74, 80,  procheckString2float, True),
        gfCHI12   = (81, 87,  procheckString2float, True),
        gfCHI1    = (88, 94,  procheckString2float, True),
        gf        = (95, 101, procheckString2float, True) # note it's zero for nucleic acids.
    )
    procheckDefs = NTdict(
                          # Keep rucksack from filling up over the years.
    #   field       (startChar, endChar, conversionFunction, store)
#        line      = (  0,  4, int, False ), # unique residue id over all models in NMR ensemble. No need to capture.
        resName   = (4, 7, str, False),
        chain     = (8, 9, str, False),
        resNum    = (9, 13, int, False), # 4 digits!
        secStruct = (14, 15, str, True),
        PHI       = (15, 22, procheckString2float, False), # Already calculated internally.
        PSI       = (22, 29, procheckString2float, False),
        OMEGA     = (29, 36, procheckString2float, False),
        CHI1      = (36, 43, procheckString2float, False),
        CHI2      = (43, 50, procheckString2float, False),
        CHI3      = (50, 57, procheckString2float, False),
        CHI4      = (57, 64, procheckString2float, False)
    )

    rangesFileName = 'ranges.txt'
    procheckScript = 'procheck_nmr.scr'

    def __init__(self, project, **kwds):
        NTdict.__init__( self, __CLASS__ = PROCHECK_STR, **kwds )
#        Procheck class allows running procheck_nmr and parsing of results
        self.project      = project
        self.molecule     = project.molecule
        self.rootPath     = project.mkdir(project.molecule.name, project.moleculeDirectories.procheck)

        #generate the script

        self.redirectOutput = True
#        if cing.verbosity >= verbosityDebug: # Done debugging.
#            self.redirectOutput=False
#        nTdebug("Will redirect procheck output: " + repr(self.redirectOutput))
        self.procheck  = ExecuteProgram('./' + self.procheckScript,
                                        rootPath = self.rootPath,
                                        redirectOutput= self.redirectOutput
                                        )
        self.aqpc      = ExecuteProgram(cingPaths.aqpc,
                                        rootPath = self.rootPath,
                                        redirectOutput= self.redirectOutput
                                       )
        self.ranges    = None
    #end def

    def rangesForPlugin(self, ranges):
        '''
        Translate the ranges into plugin formatted string.
        Return empty string for empty selection.
        Return None on error.
        Return string otherwise.

        See Molecule#residueList2Ranges
        '''
        result = ''
        startStopList = self.molecule.ranges2StartStopList(ranges)
#        nTdebug( 'In pc startStopList (just the inclusive boundaries): %s' % startStopList)
        if startStopList == None:
            nTerror( 'In pc failed to get startStopList for ranges: %s' % ranges)
            return
        for i in range(0, len(startStopList), 2):
            result += 'RESIDUES'
            for r in ( startStopList[i], startStopList[i+1]):
                result += ' %3d %2s' % (r.resNum, r.chain.name)
            result += '\n'
#        nTdebug( ">ranges:\n" + result)
        return result
    # end def

    def getMaxModelCount(self):
        max_models = min( self.molecule.modelCount, MAX_PROCHECK_NMR_MODELS)
        resCount = len( self.molecule.allResidues() )
        resCountTotal = max_models * resCount
        if resCountTotal >= MAX_PROCHECK_TOTAL_RESIDUES:
            max_models_org = max_models
            max_models =  MAX_PROCHECK_TOTAL_RESIDUES / resCount
            nTdebug("Reducing number of models from %s to %s to limit residue count to less than %s" % (max_models_org, max_models, 
                MAX_PROCHECK_TOTAL_RESIDUES))
        if max_models < 1:
            nTerror("Molecule is to large for procheck to even run on a single model")
            return True
        if max_models > self.molecule.modelCount:
            nTcodeerror("Was trying to run more models than available; reseting to just a one.")
            max_models = 1
        return max_models
    # end def

    def run(self, ranges=None, export = True, createPlots=True, runAqua=True):
        """
        Run procheck analysis.

        Ranges: GWV 25 Sep 2008: does work ok, using modified script to only implement for tplot call

        Return True on error (None on success; Python default)
        """
        #

        if self.molecule.modelCount == 0:
            nTwarning('Procheck run: no models for "%s"', self.molecule)
            return

        # It's actually important not to write any to Procheck then because
        # there might be more than 200 stretches which upsets PC.
        nTmessage('==> Running procheck_nmr')

        useRanges = self.molecule.useRanges(ranges)
        if useRanges:
            self.ranges = ranges
#            nTdebug("pc.ranges: %s" % self.ranges)
            # Convert the ranges and translate into procheck format
            selectedResidues = self.molecule.setResiduesFromRanges(ranges)
            if selectedResidues == None:
                nTerror( 'In procheck.run selectedResidues None for ranges: %s' % ranges)
                return True
            rangesTxtPlugin = self.rangesForPlugin(ranges)
            if rangesTxtPlugin == None:
                nTerror('Procheck.run: Failed to get rangesTxtPlugin for ranges: [%s]' % ranges)
                return True
            writeTextToFile(os.path.join(self.rootPath, self.rangesFileName), rangesTxtPlugin)
        #end if

        #copy script
        source = os.path.join(cingPythonCingDir, 'PluginCode', DATA_STR, self.procheckScript)
        destination = os.path.join(self.rootPath, self.procheckScript)
        try:
            copy(source, destination)
        except:
            nTerror('Procheck.run: Failed to copy (by exception) "%s"', source)
            return True

        # Copy parameter file
        pcNmrParameterFileOrg = 'procheck_nmr.prm'
        if not createPlots:
            pcNmrParameterFileOrg = 'procheck_nmr_nada.prm'

        pcNmrParameterFile = os.path.join(cingPythonCingDir, 'PluginCode', DATA_STR, pcNmrParameterFileOrg)
        pcNmrParameterFileDestination = os.path.join(self.rootPath, 'procheck_nmr.prm')
        if os.path.exists(pcNmrParameterFileDestination):
#            nTdebug("Removing existing pcNmrParameterFileDestination:"+ pcNmrParameterFileDestination)
            os.unlink(pcNmrParameterFileDestination)
#        nTdebug("Copying "+pcNmrParameterFile+" to: " + pcNmrParameterFileDestination)

        try: # Don't allow this to mess up CING.1
            if copy(pcNmrParameterFile, pcNmrParameterFileDestination):
    #        if os.link(pcNmrParameterFile, pcNmrParameterFileDestination): # don't use link in python for this.
                nTerror("Procheck.run: Failed to copy from " +pcNmrParameterFile+" to: " + pcNmrParameterFileDestination)
                return True
        except:
            nTerror("Procheck.run: Failed to copy (by exception) from " +pcNmrParameterFile+" to: " + pcNmrParameterFileDestination)
            return True

        max_models = self.getMaxModelCount()

        path = os.path.join(self.rootPath, self.molecule.name + '.pdb')
        if export:
            self.molecule.toPDB(path, convention=AQUA, max_models = max_models)
#            self.molecule.toPDBfile(path, convention=AQUA) #GV removed because not implemented in toPDBfile; 12 Jan 09 Try-again
            # Can't use IUPAC here because aqua doesn't understand difference between
            # G and DG.(oxy/deoxy).

        canAqpc = True

        if cingPaths.aqpc == None or cingPaths.aqpc == PLEASE_ADD_EXECUTABLE_HERE:
            nTmessage("No aqpc installed so skipping this step")
            canAqpc = False

        if canAqpc:
            # Save restraints for Aqua
            if self.project.export2aqua():
                canAqpc = False
                nTwarning("Failed to export restraints to Aqua; will run pc without restraints")
            else:
                hasRestraints = False
                for extensionRestraintFile in [ "noe", "tor" ]:
                    srcDir = os.path.join(self.project.rootPath(self.project.name)[0], self.project.directories.aqua )
                    if not os.path.exists(srcDir):
                        nTcodeerror("Aqua export dir is absent")
                        return True
                    fileName = self.project.name +'.' + extensionRestraintFile
                    path = os.path.join(srcDir, fileName )
                    if not os.path.exists(path):
#                        nTdebug("No "+ path+" file found (in Aqua export dir)")
                        pass
                    else:
                        # Map from Aqua per project file to Cing per molecule file.
                        dstFileName = self.molecule.name + '.' + extensionRestraintFile
                        dstPath = os.path.join( self.rootPath, dstFileName )
                        if os.path.exists(dstPath):
#                            nTdebug("Removing existing copy: " + dstPath)
                            os.unlink(dstPath)
#                        nTdebug("Trying to copy from: " + path+" to: "+dstPath)
#                        if os.link(path, dstPath):# don't use link in python for this.
                        if disk.copy(path, dstPath):# don't use link in python for this.
                            nTcodeerror("Failed to copy from: " + path+" to: "+self.rootPath)
                            return True
                        hasRestraints = True
                # run aqpc
                if not canAqpc:
                    nTwarning("Skipping aqpc because failed to convert restraints to Aqua")
                elif not hasRestraints:
                    pass
#                    nTdebug("Skipping aqpc because no Aqua restraints were copied for Aqua")
                else:
#                    nTdebug("Trying aqpc")
                    if self.aqpc( '-r6sum 1 ' + self.molecule.name + '.pdb'):
                        nTcodeerror("Failed to run aqpc; please consult the log file aqpc.log etc. in the molecules procheck directory.")
                        return True
                    else:
                        nTmessage("==> Finished aqpc successfully")

#        nTdebug("Trying procheck_nmr")
        cmd = self.molecule.name +'.pdb'
        if useRanges:
            cmd += ' ' + self.rangesFileName
        if self.procheck(cmd):
            nTerror('Failed to run procheck_nmr successfully; please consult the log file (.log, .out0 etc). in the "%s" directory.',
                    self.rootPath)
            return True
        if self.parseResult():
            nTerror('Failed to procheck_nmr parseResult.')
            return False
        # Remove temp files in case the run was successful and parsed ok.
        removeTempFiles(self.rootPath)

        # Store in project file that we ran procheck successfully
        self.project.procheckStatus.completed = True
        if useRanges:
            self.project.procheckStatus.ranges = ranges
        else:
            self.project.procheckStatus.ranges = None
        nTmessage("==> Finished procheck_nmr successfully")

        return True
    #end def


    def _parseProcheckLine(self, line, defs):
        """
        Internal routine to parse a single line
        Return result, which is a dict type or None
        on error (i.e. too short line)
 e.g.   field       (startChar, endChar, conversionFunction)
        resName   = (  4,  7, str ),
        """
        result = {}
        if len(line) < 65:
            return None
        for field, fieldDef in defs.iteritems():
            c1, c2, func, dummyStore = fieldDef
            result[ field ] = func(line[c1:c2])
        return result
    #end def


    def parseResult(self):
        """
        Parse procheck .rin and .edt files and store result in procheck NTdict
        of each residue of molecule.

        Return True on error.

        """
#        nTdebug("Starting pc parseResult")
#        modelCount = self.molecule.modelCount
        modelCount = self.getMaxModelCount()

#        nTdebug("==> Parsing procheck results")

#        if modelCount > MAX_PROCHECK_NMR_MODELS:
#            nTwarning("Limiting number of models analyzed from %d to %d" % (modelCount, MAX_PROCHECK_NMR_MODELS))
#            modelCount = MAX_PROCHECK_NMR_MODELS

        # reset the procheck dictionary of each residue
        for res in self.molecule.allResidues():
            if res.has_key(PROCHECK_STR):
                del(res[PROCHECK_STR])
            res.procheck = ProcheckResidueResult(res)
        #end for

        for i in range(1, modelCount+1):
            modelCountStr = "%03d" % i

            # special case in procheck_nmr
            if modelCount == 1:
                # special case for different versions Alan vs Jurgen...
                # JFD adds; this fails with my pc. Adding enabling code to handle both.
                modelCountStr = "000"
                path = os.path.join(self.rootPath, '%s_%s.rin' % (self.molecule.name, modelCountStr))
                if not os.path.exists(path):
#                    nTdebug('Procheck.parseResult: file "%s" not found assuming it was pc -server- version. ', path)
                    modelCountStr = "***"

            path = os.path.join(self.rootPath, '%s_%s.rin' % (self.molecule.name, modelCountStr))
            if not os.path.exists(path):
                nTerror('Procheck.parseResult: file "%s" not found', path)
                return True


            for line in AwkLike(path, minLength = 64, commentString = "#"):
#                nTdebug("working on line: %s" % line.dollar[0])
                result = self._parseProcheckLine(line.dollar[0], self.procheckDefs)
                if not result:
                    nTerror("Failed to parse procheck rin file the below line; giving up.")
                    nTerror(line.dollar[0])
                    return True
                chain   = result['chain']
                resNum  = result['resNum']
                residue = self.molecule.decodeNameTuple((None, chain, resNum, None))
                if not residue:
                    nTerror('in Procheck.parseResult: residue not found (%s,%d); giving up.' % (chain, resNum))
                    return True

#                nTdebug("working on residue %s" % residue)
                for field, value in result.iteritems():
                    if not self.procheckDefs[field][3]: # Checking store parameter.
                        continue
                    # Insert for key: "field" if missing an empty  NTlist.
                    residue.procheck.setdefault(field, NTlist())
#                    nTdebug( "For residue %s field %s found value %s" % ( residue, field, value ) )
                    residue.procheck[field].append(value)
#                    nTdebug("field %s has values: %s" % ( field, residue.procheck[field]))
                #end for result
            #end for line
        #end for

        path = os.path.join(self.rootPath, '%s.edt' % self.molecule.name)
        if not os.path.exists(path):
            nTerror('Procheck.parseResult: file "%s" not found', path)
            return True
#        nTdebug( '> parsing edt >'+ path)

        for line in AwkLike(path, minLength = 64, commentString = "#"):
            result = self._parseProcheckLine(line.dollar[0], self.procheckEnsembleDefs)
            if not result:
                nTerror("Failed to parse procheck edt file the below line; giving up.")
                nTerror(line.dollar[0])
                return
            chain   = result['chain']
            resNum  = result['resNum']
            residue = self.molecule.decodeNameTuple((None, chain, resNum, None))
            if not residue:
                nTerror('Procheck.parseResult: residue not found (%s,%d); giving up.' % (chain, resNum))
                return
            #end if

            for field, value in result.iteritems():
                if not self.procheckEnsembleDefs[field][3]: # Checking store parameter.
                    continue
                # end if
                # Truncate for those rare instances ( < 10 for > 9,000 entries )
#pc gf phipsi can be extremely high: 
# 1b64 SER      82        34.36      this might be an installation bug as it's value in PDBe is normal.
                if value and (field in gf_LIST_STR):
                    if value > PCgFactorMaxErrorValue:
                        nTwarning("A pc g-factor for %s of %s will be truncated to %s" % ( field, value, PCgFactorMaxErrorValue))
                        value = PCgFactorMaxErrorValue
                    # end if 
                # end if
                residue.procheck[field] = value
            #end for
        #end for
        for field in gf_LIST_STR:
            resultList = NTlist()
            for residue in self.molecule.allResidues():
                value = residue.getDeepByKeys(PROCHECK_STR, field)
#                nTdebug( "For residue %s field %s found value %s" % ( residue, field, value ) )
                resultList.append(  value )
            averageTuple = resultList.average()
#            nTdebug( "resultList %s" % resultList )
            # Nones will be ignored. Empty list will return )None,,)
            if averageTuple: # get average only
                self.molecule[PROCHECK_STR][field] = averageTuple[0]
            else:
                nTwarning("No average over molecule obtained in procheck for %s" % field)
        # summary
        path = os.path.join(self.rootPath, '%s.sum' % self.molecule.name)
        if not os.path.exists(path):
            nTerror('Procheck.parseResult: file "%s" not found', path)
            return True
#        nTdebug( '> parsing sum >'+ path)
        text = open(path, 'r').read()
#        nTdebug( 'got: \n'+ text)
        if text:
            self.summary = ProcheckSummaryResult( text, self.molecule, self.ranges )
        else:
            nTerror('Procheck.parseResult: Failed to read and parse Procheck_nmr summary file (%s)', path)
            return True
        #end if

        self.postProcess()

        self.fileList = self.getPostscriptFileNames()

        return False
    #end def

    def postProcess(self):
#        for item in [ SECSTRUCT_STR ]:
#            for res in self.project.molecule.allResidues():
#                if res.has_key( item ):
#                    itemList = res[ item ]
#                    c = itemList.setConsensus()
#                    nTdebug('consensus: %s', c)
        for res in self.molecule.allResidues():
#            res.procheck.consensus = res.procheck.secStruct.setConsensus( CONSENSUS_SEC_STRUCT_FRACTION )
            res.procheck.consensus = res.procheck.secStruct.setConsensus( useLargest=True )
    #end def

    def getPostscriptFileNames(self):
        """
        Return a NTlist with (postscriptFileName, description) tuples
        """
        result = NTlist()
        path = os.path.join(self.rootPath, 'postscriptFiles.lis')
        if os.path.exists(path):
            for line in AwkLike(path, separator=':'):
                result.append( (line.dollar[2][:-1].strip(), line.dollar[1][:-6].strip()) )
        else:
            nTwarning("Failed to find %s in getPostscriptFileNames" % path)
        return result
    #end def
#end class

def runProcheck(project, ranges=None, createPlots=True, runAqua=True, parseOnly = False)   :
    """
    Adds <Procheck> instance to molecule. Run procheck and parse result.
    Return True on error.
    """
    if cingPaths.procheck_nmr == None or cingPaths.procheck_nmr == PLEASE_ADD_EXECUTABLE_HERE:
        nTmessage("No procheck_nmr installed so skipping this step")
        return

    if not project.molecule:
        nTerror('runProcheck: no molecule defined')
        return True
    #end if
    if project.molecule.modelCount == 0:
        nTwarning('runProcheck: no models for "%s"', project.molecule)
        return

    if not project.molecule.hasAminoAcid():
#    if len(project.molecule.residuesWithProperties('protein')) == 0:
        nTmessage("Skipping procheck as there is no protein in the current molecule")
        return
    # end if
    if project.molecule.has_key(PROCHECK_STR):
        del(project.molecule[PROCHECK_STR])
    #end if

    if ranges == None:
        ranges = project.molecule.ranges

    pcheck = Procheck(project)
    if not pcheck:
        nTerror("runProcheck: Failed to get procheck instance of project")
        return True

    project.molecule[PROCHECK_STR] = pcheck

    if not parseOnly:
        if not pcheck.run(ranges=ranges,createPlots=createPlots, runAqua=runAqua):
            nTerror("runProcheck: Failed to run procheck_nmr")
            return True
    else:
        pcheck.ranges = ranges
        pcheck.parseResult()

    return project.molecule[PROCHECK_STR]
#end def

def restoreProcheck( project, tmp=None ):
    """
    Optionally restore procheck results
    """
    if project.procheckStatus.completed:
        nTmessage('==> Restoring procheck results')
        project.runProcheck(parseOnly=True, ranges = project.procheckStatus.ranges)
#end def

def getProcheckSecStructConsensus( res ):
    """ Returns None for error, or one of [' ', 'H', E' ]
    """
    secStructList = res.getDeepByKeys(PROCHECK_STR,SECSTRUCT_STR)
    result = None
    if secStructList:
        secStructList = to3StatePC( secStructList )
#        result = secStructList.getConsensus(CONSENSUS_SEC_STRUCT_FRACTION) # will set it if not present yet.
        result = secStructList.getConsensus(useLargest=True) # will set it if not present yet.
#    nTdebug('secStruct res: %s %s %s', res, secStructList, secStruct)
    return result

def removeTempFiles( todoDir ):
#    whatifDir        = project.mkdir( project.molecule.name, project.moleculeDirectories.whatif  )
#    nTdebug("Removing temporary files generated by Procheck")
    try:
        removeListLocal = ["prodata", "ps.number", "aqua.cmm", "resdefs.dat", "mplot.in", '.log' ]
        removeList = []
        for fn in removeListLocal:
            removeList.append( os.path.join(todoDir, fn) )

        for extension in [ "*.ave", "*.pdb", "*.new", "*.str", "*.noe", "*.nrc", "*.nrv", "*.rms", "*.scr", "*.prm" ]:
            for fn in glob(os.path.join(todoDir,extension)):
                removeList.append(fn)
        for fn in removeList:
            if not os.path.exists(fn):
#                nTdebug("procheck.removeTempFiles: Expected to find a file to be removed but it doesn't exist: " + fn )
                continue
#            nTdebug("Removing: " + fn)
            os.unlink(fn)
    except:
        nTdebug("procheck.removeTempFiles: Failed to remove all temporary files that were expected")
#end def


# register the functions
methods  = [(runProcheck, None)
           ]
#saves    = []
restores = [(restoreProcheck, None)
           ]
#exports  = []
