"""
Adds export2xplor methods to:
DistanceRestraint , DistanceRestraintList, DihedralRestraint, DihedralRestraintList,
Atom, Molecule and Project classes.

    DistanceRestraint.export2xplor()

    DistanceRestraintList.export2xplor( path  )

    DihedralRestraint.export2xplor()

    DihedralRestraintList.export2xplor( path  )

    Atom.export2xplor()

    Molecule.export2xplor( path  )

    Project.export2xplor():
        exports Molecules in xplor nomenclature
        exports DistanceRestraintLists in xplor format

    Molecule.newMoleculeFromXplor( project, path, name, models=None ):
        Generate new molecule 'name' from set of pdbFiles in XPLOR convention
        path should be in the form filename%03d.pdb, to allow for multiple files
        for each model.
        models is a list of model numbers.
        return Molecule or None on error


!!NEED to Check periodicity in dihedrals

"""

# get target in DR.
# Configure amount of data to keep. nothing, 1 mb, 10 mb, 100 mb.
# nothing is just data in cing.
# Charles mentioning that except nucleic acids the IUPAC conventions can be generated for CING.
#from Refine.refine import doSetup # This would be a circular import to avoid
from Refine.refine import * #@UnusedWildImport
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.core.classes import * #@UnusedWildImport
from cing.core.constants import * #@UnusedWildImport
from cing.core.molecule import * #@UnusedWildImport


#==============================================================================
# XPLOR stuff
#==============================================================================

# Xplor characters that need quoting
xplorWildCardList = '* % # +'.split()
# Only quote character in xplor.
xplorQuoteCharacter = '"'

def quoteAtomNameIfNeeded(atomNameXplor):
    '''
    Adds quotes to atom names if needed in xplor.
    Usually this is not even desirable as e.g. GLU HB* or U H2'
    but for CA+2 it is because it's a wild card that would not expand right.
    @param atomNameXplor:
    '''
    if '"' in  atomNameXplor:
        nTerror("A double quote may not occur in any xplor name")
        return None
    needed = False
#    for xplorWildCard in xplorWildCardList:
#        if xplorWildCard in atomNameXplor:
#            needed = True
#    if not needed:
#        return atomNameXplor

    # Now special case the ions that are the only ones that need the quotes, see ion.top
    # See $CINGROOT/python/Refine/toppar/ion.top NB this is specific to the library.
    # E.g.
#RESIdue CA2 {calcium 2+}
#  GROUp
#    ATOM CA+2 TYPE=CA+2 CHARge=+2.0 END
#END {CA2}
    reMatch = re.compile('[-+](\d)$') # The 24 character standard notation from time.asctime()
    searchObj = reMatch.search(atomNameXplor)
    if searchObj:
#        nTdebug("Special case for ions found: for %s" % atomNameXplor)
        needed = True

    if not needed:
        return atomNameXplor
    return '"%s"' % atomNameXplor

#-----------------------------------------------------------------------------
def exportAtom2xplor( atom ):
    """returns string in xplor format"""
    atomNameXplor = atom.translate(XPLOR)
    if atomNameXplor == None:
        atomNameXplor = atom.name
    # end if
    atomNameXplor = quoteAtomNameIfNeeded(atomNameXplor)
    chainId = atom.residue.chain.name
    return sprintf( '( segi %s and resi %4d and name %-4s )',
                      chainId,
                      atom.residue.resNum,
                      atomNameXplor
                   )
#end def
# add as a method to Atom Class
Atom.export2xplor = exportAtom2xplor


#-----------------------------------------------------------------------------
def exportDistanceRestraint2xplor( distanceRestraint ):
    """Return string with restraint in Xplor format
    Return None on error.
    """
    if distanceRestraint.upper == None:
        nTerror("Skipping restraint because no upper bound: %s", distanceRestraint)
        return
    dminus = distanceRestraint.upper
    if distanceRestraint.lower != None:
        dminus = distanceRestraint.upper-distanceRestraint.lower                
    s = sprintf('assi ')
    for i,atmList in enumerate( distanceRestraint.atomPairs ):
        if len(atmList) != 2:
            nTerror("Skipping restraint because bad number of atom selections. Expected 2 but found: %s in: %s", 
                    distanceRestraint, len(atmList))
            return
        
        if i != 0:
            s += sprintf( '\n  or ')                    
        for atm in atmList:
            atomSelStr = atm.export2xplor()
            if atomSelStr == None:
                nTerror("Skipping restraint because bad atom selection: %s", distanceRestraint)
                return
            s += sprintf( '%-30s ', atomSelStr )
        # end for
        if i == 0:
            s += sprintf('%8.3f  %8.3f  0.0', distanceRestraint.upper, dminus )  # syntax xplor: d, dminus, dplus
    # end for
    return s
#end def


# add as a method to DistanceRestraint Class
DistanceRestraint.export2xplor = exportDistanceRestraint2xplor


#-----------------------------------------------------------------------------
def exportDisList2xplor( drl, path)   :
    """Export a distanceRestraintList (DRL) to xplor format:
       return drl or None on error
    """
    msgHol = MsgHoL()    
    fp = open( path, 'w' )
    if not fp:
        nTerror('exportDisList2xplor: unable to open "%s"\n', path )
        return None
    #end def
    for dr in drl:
        drStr = dr.export2xplor()
        if drStr == None:
            msgHol.appendMessage(str(dr))
            continue
        fprintf( fp, '%s\n', drStr )
    #end for
    fp.close()
    msgHol.showMessage(max_messages=20)
    nTmessage('==> Exported %s to "%s"', drl, path)
    #end if
    return drl
#end def
# add as a method to DistanceRestraintList Class
DistanceRestraintList.export2xplor = exportDisList2xplor

#-----------------------------------------------------------------------------
def exportDihedralRestraint2xplor( dihedralRestraint ):
    """Return string with restraint in Xplor format
       GV 24 Sept 2007: delta adjusted to delta*0.5
    """
    s = sprintf('assign \n')
    for a in dihedralRestraint.atoms:
        s = s + sprintf( '     %-30s\n', a.export2xplor() )
    #end for

    delta = math.fabs( dihedralRestraint.upper-dihedralRestraint.lower )
    ave   = dihedralRestraint.lower + delta*0.5

    s = s + sprintf('     %8.2f %8.2f %8.2f 2\n',
                     1.0, ave, delta*0.5  # syntax xplor:
                   )
    return s
#end def
# add as a method to DihedralRestraint Class
DihedralRestraint.export2xplor = exportDihedralRestraint2xplor

#-----------------------------------------------------------------------------
def exportDihList2xplor( drl, path)   :
    """Export a dihedralRestraintList (DRL) to xplor format:
       return drl or None on error
    """
    fp = open( path, 'w' )
    if not fp:
        nTerror('exportDihList2xplor: unable to open "%s"\n', path )
        return None
    #end def
    noneWarn = False
    for dr in drl:
        # We don't want to export the restraint if it has no value
        # No upper or lower bound is as worse as not upper and lower bounds 
        if dr.lower is not None and dr.upper is not None:
            fprintf( fp, '%s\n', dr.export2xplor() )
        else:
            noneWarn = True
    #end for

    fp.close()
    nTmessage('==> Exported %s to "%s"', drl, path)
    if noneWarn:
        nTwarning('exportDihList2xplor: dihedral restraint(s) with value None not exported to xplor')
    #end if
    return drl
#end def
# add as a method to DistanceRestraintList Class
DihedralRestraintList.export2xplor = exportDihList2xplor


#-----------------------------------------------------------------------------
def exportMolecule2xplor( molecule, path, chainName = None, model = None):
    """Export coordinates of molecule to pdbFile in XPLOR convention;
       generate modelCount files,
       path should be in the form name%03d.pdb, to allow for multiple files
       for each model
       When the chain name is given then only that chain will be written.
       If it is the special case of  it will do a recursive call here.
       return Molecule or None on error
    """
    if chainName == ALL_CHAINS_STR:
        for chain in molecule.allChains():
            exportMolecule2xplor( molecule, path, chainName = chain.name)
#        nTdebug("Finished writing all chains.")
        return
    
    modelList = range(molecule.modelCount)
    if model != None:
        modelList = [ model ]
        
    for model in modelList:
        pdbFile = molecule.toPDB( model=model, convention = XPLOR, chainName = chainName)
        if not pdbFile:
            return None
        if chainName:
            pdbFileName = sprintf( path, chainName, model )
        else:
            pdbFileName = sprintf( path, model )
        pdbFile.save( pdbFileName )
        del(pdbFile)
    #end for
    return molecule
#end def
# add as a method to Molecule Class
Molecule.export2xplor = exportMolecule2xplor


def newMoleculeFromXplor( project, path, name, models=None ):
    """Generate new molecule 'name' from set of pdbFiles in XPLOR convention

       path should be in the form filename%03d.pdb, to allow for multiple files
       for each model.

       models is a optional list of model numbers, otherwise it scans for files.

       return Molecule or None on error

       NB model_000.pdb becomes model number 0. Ie model=0
    """
#    print '>', path, name, models
#    nTmessage(name,models[0])

    if models == None:
        models = NTlist()
        model = 0
        xplorFile = sprintf(path,model)
        #print '>>', xplorFile
        while os.path.exists( xplorFile ):
            model += 1
            models.append( model )
            xplorFile = sprintf(path,model)
            #print '>>', xplorFile
        #end while
        #print '>>', models
    #end if

    if len(models) == 0:
        nTerror('newMoleculeFromXplor: empty models list\n')
        return None
    #end if

    # first one:
#    modelId = models[0]
    xplorFile = sprintf( path, models[0] )
    if not os.path.exists(xplorFile):
        nTerror('newMoleculeFromXplor: file "%s" not found\n', xplorFile)
        return None
    #end if
#    project.appendMolecule( molecule )
    molecule = project.initPDB( xplorFile, name=name, convention = XPLOR )
    if not molecule:
        return None
    # now the other models:
    for model in models[1:]:
#        modelId = model - 1
        xplorFile = sprintf( path, model )
        if not molecule.importFromPDB( xplorFile, XPLOR, nmodels=1):
            return None
        #end if
    #end for

    project.molecule.updateAll()

    project.addHistory( sprintf('New molecule "%s" from XPLOR files %s (%d models)\n', name, path, molecule.modelCount ) )
    project.updateProject()
    nTdetail( '%s', molecule.format() )

    return molecule

#end def
#-----------------------------------------------------------------------------
def export2xplor( project, tmp=None ):
    """export distanceRestraintLists to xplor
       export Molecules to PDB files in xplor format
    """
    for drl in project.distances:
        drl.export2xplor( project.path( project.directories.xplor, drl.name +'.tbl' ),

                        )
    #end for

    for drl in project.dihedrals:
        drl.export2xplor( project.path( project.directories.xplor, drl.name +'.tbl' ),

                        )
    #end for

    for molName in project.moleculeNames:
        mol   = project[molName]
        path = project.path( project.directories.xplor, mol.name + '_%03d.pdb' )
        mol.export2xplor( path)
    #end for
#end def

def createProjectFromXplorMemory(name="xplorNIH", sim=None):
    '''
    Using Xplor-NIH API to generate a CING project (with specified name) from
    memory, given an Xplor-NIH Simulation. If sim is not specified, the
    current simulation will be used.

    Returns the new project.
    '''

    if sim==None:
        from simulation import currentSimulation #@UnresolvedImport
        sim= currentSimulation()
#        pass

    from tempfile import NamedTemporaryFile
    tmpfile=NamedTemporaryFile(suffix=".pdb")

    import protocol #@UnresolvedImport
    from atomSel import AtomSel #@UnresolvedImport
    tmpfile.write(protocol.writePDB("",selection=AtomSel("all",sim)))
    tmpfile.flush()

    # For now we just read an xplor generated PDB file
    project = Project.open(name, status='new')
    project.initPDB(pdbFile=tmpfile.name, convention=XPLOR)

    # Fill in for example the DRs
    #getDrFromXplorMemory( project )
    project.save()
#    project.validate() # better called from a separate routine.
    return project

def getDrFromXplorMemory( project, convention ):
    """Convert DR from XPLOR in memory to CING in memory.
       return a DistanceRestraintList or None on error
       Probably we can take convention out from the parameters
    """
    maxErrorCount = 50
    errorCount = 0

    # check the molecule
    if not project or not project.molecule:
        nTdebug("getDrFromXplorMemory: initialize molecule first")
        return None
    #end if
    molecule = project.molecule

    name = 'DR name in xplor'
    result        = project.distances.new( name=name, status='keep')
    # Temporary dictionary for fast lookup of atom objects by tuple of (segi, resi, name)
    atomDict      = molecule._getAtomDictWithChain(convention)

    drListXPLOR = [] # TODO: fill in...
    for _dr in drListXPLOR:
        atmIdxList = [[1,3],[4,6]]
        atmList = []
#        i=0
        for atmIdx in atmIdxList:
            nTdebug("Doing atmIdx: " + repr(atmIdx))
            t = ( 'A', 99, 'HA3' ) # TODO: from XPLOR
            atm = None
            if atomDict.has_key(t):
                atm = atomDict[t]
            if not atm:
                if errorCount <= maxErrorCount:
                    nTerror('Failed to decode for atom %s; line: %s', t)
                if errorCount == maxErrorCount+1:
                    nTerror("And so on")
                errorCount += 1
#                i+=1
                continue
            atmList.append( atm )
#            i+=1
        if len(atmList) != 2:
            continue
        # Unpack convenience variables.
        atm1 = atmList[0]
        atm2 = atmList[1]
#        nTdebug("atom 1: " + repr(atm1))
#        nTdebug("atom 2: " + repr(atm2))
        upper = 5. # TODO: from XPLOR
        if not upper:
            nTerror("Skipping line without valid upper bound on line: [" + upper +']')
            continue

        # ambiguous restraint, should be append to last one
        if upper == 0:
            result().appendPair( (atm1,atm2) )
            continue
        lower = 'bogus'

        r = DistanceRestraint( atomPairs= [(atm1,atm2)], lower=lower, upper=upper )
        result.append( r )
        # also store extra info if present
        peak = 9.999
        if peak:
            r.peak = peak
#        if line.NF >= 11:
#            r.SUP = line.float( 11 )
#        if line.NF >= 13:
#            r.QF = line.float( 13 )
    #end for
    if errorCount:
        nTerror("Found number of errors importing upl file: " + repr(errorCount))
    nTmessage('==> importUpl: new %s', result )
    return result
#end def

def fullRedo(project, modelCountAnneal = 200, bestAnneal = 50, best = 25):
    'Return True on error.'
        
    nTmessage("==> Recalculating and refining a new ensemble in cing.PluginCode.xplor#%s" % getCallerName())
    
    if 0: # DEFAULT: 0
        modelCountAnneal, bestAnneal, best = 4,3,2
    if project == None:
        nTerror("Failed to get a project")
        return True
    #end if

    
    parser = getRefineParser() # Get some defaults assumed to exist in the setup.
    (options, _args) = parser.parse_args([''])
    options.name = '%s_redo' % project.name
#    options.sort = 'Enoe'
    options.modelsAnneal = '0-%d' % (modelCountAnneal-1) # Needs to be specified because default is to use modelCount from project
    options.modelCountAnneal = modelCountAnneal
    options.bestAnneal = bestAnneal 
    options.best = best
    options.superpose = 'cv'
    options.overwrite=1
        
    basePath = project.path(project.directories.refine, options.name)
    nTmessage("basePath: " + basePath)
    
    nTmessage("==> Reading configuration")
    nTmessage('refinePath:     %s', config.refinePath)
    nTmessage('xplor:          %s', config.XPLOR)
    nTmessage("parameterFiles: %s", config.parameterFiles)
    nTmessage("topologyFiles:  %s", config.topologyFiles)

    parameters = fullAnnealAndRefine( config, project, options)
    if not parameters:
        nTerror("Failed to do fullAnnealAndRefine")
        return True
    #end if
#end def
        
        
#-----------------------------------------------------------------------------
# register the functions in the project class
methods  = [(newMoleculeFromXplor, None),
            (fullRedo, None)
#            (recalculate, None), # JFD really wanted it here but makes cyclic defs.
           ]
#saves    = []
#restores = []
exports  = [(export2xplor, None),
           ]
