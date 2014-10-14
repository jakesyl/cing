from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Libs.fpconst import NaN as nan #@UnresolvedImport @UnusedImport ? need for restoring the project ?
from cing.PluginCode.required.reqVasco import * #@UnusedWildImport
from cing.core.classes import * #@UnusedWildImport
from cing.core.constants import * #@UnusedWildImport
from cing.core.database import * #@UnusedWildImport
from cing.core.molecule import * #@UnusedWildImport
 
SMLstarthandlers = {}
SMLendhandlers   = {}
SMLversion       = 0.25
# version history:
#  0.1: initial version
#  0.2: NTlist and NTdict SML handlers; recursion in dict-like handlers
#  0.21: Explicitly require endHandler to return obj or None on error.
#  0.22: SML Molecule, Chain, Residue, Atom handlers
#  0.221: Atom saves shiftx
#  0.23: Molecule saves Nterminal, Cterminal in _sequence list
#  0.24: ResidueDef initial string changes

SMLsaveFormat  = 'INTERNAL_0'
SMLfileVersion = None

class SmlFile(file):
    def __init__(self, *args, **kwds):
        file.__init__(self, *args, **kwds)
        # pylint: disable=C0103
        self.NR = 0
    #end def

    def readline(self):
        # Skip empty lines and lines the start with #
        line = file.readline(self)
        self.NR += 1
        while line and (len(line)<=1 or line.lstrip().startswith('#')):
            line = file.readline(self)
            self.NR += 1
        return line
    #end def

    def readlines(self):
        lines = file.readlines(self)
        self.NR += len(lines)
        return lines
    #end def
#end def

class SMLhandler:
    """
    Base class for decoding of the Simple-markup language storage.

    JFD notes:
        - Each file may contain only one element at the top. I.e. multiple objects must be nested into a single top one.
        - Empty NTdict and NTlist are fine.
        - See example unit test cases in test_sml.py
        - The global SMLstarthandlers, SMLendhandlers get filled on the fly.
Example file:

<SML> 0.221
<PeakList> n15 keep
<Peak>  3  0
    positions       = NTlist(122.892, 1.3480000000000001, 8.0530000000000008)
    height          = (12190.0, 0.0)
    volume          = (nan, nan)
    xeasyIndex      = 20000
    resonances      = NTlist(('refine2', 'A', 502, 'N', None, 0, 'CYANA'), ('refine2', 'A', 502, 'QB', None, 0, 'CYANA'), ('refine2', 'A', 502, 'HN', None, 0, 'CYANA'))
</Peak>
<Peak>  3  1
    positions       = NTlist(121.06, 3.9929999999999999, 8.1780000000000008)
    height          = (6104.0, 0.0)
    volume          = (nan, nan)
    xeasyIndex      = 20001
    resonances      = NTlist(('refine2', 'A', 504, 'N', None, 0, 'CYANA'), ('refine2', 'A', 503, 'HA1', None, 0, 'CYANA'), ('refine2', 'A', 504, 'HN', None, 0, 'CYANA'))
</Peak>
</PeakList>
</SML>
    """
    # Using the global statement pylint: disable=W0603
    global SMLstarthandlers, SMLendhandlers     # Using global without assignment. pylint: disable=W0602
    debug = False

    def __init__(self, name):
        self.startTag = sprintf('<%s>', name)
        self.endTag   = sprintf('</%s>', name)
        self.name     = name

        SMLstarthandlers[self.startTag] = self
        SMLendhandlers[self.endTag]     = self

#        print self._className()

    def __str__(self):
        return sprintf('<SMLhandler %s>', self.name )

#    def _className(self):
#        return str(self.__class__)[7:-2].split('.')[-1:][0]

    def listHandler(self, listObj, fp, obj=None):
        """
        General list handling routine. Parses items and append to
        listObj. Obj is carried along for convenience to pass external info if needed.

        Returns listObj or None on error.
        """
        line = SMLhandler.readline( fp )
        while line:
            n = len(line)
            if n > 0 and line[1] == self.endTag:
                return self.endHandler( listObj, obj )
            elif n > 0 and SMLstarthandlers.has_key(line[1]):
                listObj.append( SMLstarthandlers[line[1]].handle( line, fp, obj ) )
            elif n > 0 and SMLendhandlers.has_key(line[1]):
                nTerror('SMLhandler.listHandler: line %d, skipping invalid closing tag "%s"', fp.NR, line[1])
                self.jumpToEndTag( fp )
                return self.endHandler( listObj, obj )
            else:
                listObj.append( eval(line[0]) )
            #end if
            line = SMLhandler.readline( fp )
        #end while

        # we should not be here
        nTerror('SMLhandler.listHandler: unterminated list')
        return None
    #end def

    def dictHandler(self, dictObj, fp, obj=None):
        """
        General dict handling routine. Parses key = value pairs and inserts into
        dictObj. Obj is carried along for convenience to pass external info if needed.

        Returns dictObj or None on error.
        """
        line = SMLhandler.readline( fp )
        while line:
            n = len(line)
            if n > 0 and line[1]==self.endTag:
                return self.endHandler( dictObj, obj )
            # version 0.2: implement recursion
            elif n > 3 and SMLstarthandlers.has_key(line[3]):
                dictObj[line[1]] = SMLstarthandlers[line[3]].handle( [' '.join(line[3:])] + line[3:], fp, obj )
            elif n > 0 and SMLendhandlers.has_key(line[1]):
                nTerror('SMLhandler.dictHandler: line %d, skipping invalid closing tag "%s"', fp.NR, line[1])
                self.jumpToEndTag( fp )
                return self.endHandler( dictObj, obj )
            elif n > 3:
#                nTdebug("Generating over 255 arguments here in sml.dictHandler ?") # http://bugs.python.org/issue12844
#                dictObj[line[1]] = eval(' '.join(line[3:])) # Original. Failing on 2kox with 640 models.
                subLine = line[3:]
#                nTdebug("subLine: %s" % str(subLine))
                jLine = ' '.join(subLine)
#                nTdebug("jLine: %s" % str(jLine))
                lineStart = str( line[0][:80] )
                if n > 250: # Real limit is 255
                    nTdebug("Function eval will crash when over 255 elements: found: %s. Line start: %s" % ( (n-1),lineStart ))
                # end if
                try:
                    dictObj[line[1]] = eval(jLine)                
                except:
                    nTwarning("Function eval crashed not restoring data from line starting with: %s" % lineStart )
#                    nTtracebackError()
                # end try
            else:
                nTerror('SMLhandler.dictHandler: line %d, incomplete "%s"', fp.NR, line[0])
            #end if
            line = SMLhandler.readline( fp )
        #end while

        # we should not be here
        nTerror('SMLhandler.dictHandler: unterminated dict')
        return None
    #end def

    def handle(self, line, fp, obj=None ):
        """
        This method should be subclassed to fit specific needs in the actual class.
        The code could serve as a starting point or dictHandler or listHandler could be
        called:

        e.g.
            object = myObject( arguments )
            return self.listHandler( object, line, fp, obj )

        Should return a object or None on error

        The code below implements handling of the SML 'root'
        """
        global SMLfileVersion

        SMLfileVersion = float(line[2])

        newObj  = None
        line = SMLhandler.readline( fp )
        n = len(line)
        while (line):
            if n > 0 and line[1]==self.endTag:
                return self.endHandler( newObj, obj )
            elif n > 0 and SMLstarthandlers.has_key(line[1]):
                handler = SMLstarthandlers[line[1]]
                newObj  = handler.handle( line, fp, obj )
            elif n > 0 and SMLendhandlers.has_key(line[1]):
                nTerror('SMLhandler.handle: line %d, skipping invalid closing tag "%s"', fp.NR, line[1])
                self.jumpToEndTag( fp )
                return self.endHandler( newObj, obj )
            else:
                nTerror('SMLhandler.handle: line %d incomplete: "%s"', fp.NR, line[0])
            #end if
            line = SMLhandler.readline( fp )
        #end while
        # we should not be here
        nTerror('SMLhandler.handle: unterminated %s', self)
        return None
    #end def

    def endHandler(self, newObj, obj=None):
        """
        This method should be sub-classed to fit specific needs in the actual class.
        Should return newObj or None on error
       """
        return newObj
    #end def

    def jumpToEndTag(self, fp):
        """
        Progress to end tag of handler
        """
        line = self.readline(fp)
        while line:
            if len(line) > 0 and line[1] == self.endTag:
                return
            line = self.readline(fp)
        #end while
        nTerror('SMLhandler.jumpToEndTag: line %d, endTag "%s" not found', fp.NR, self.endTag)
        return
    #end def

    def toSML(self, obj, fp):
        """
        This method should be subclassed to fit specific needs in the actual class.
        Should return obj or None on error
        """
        fprintf( fp, '%s\n', self.startTag )
        # code should be here
        fprintf( fp, '%s\n', self.endTag )
        return obj
    #end def

    def list2SML(self, theList, fp ):
        """
        Write element of theList to fp for restoring later with fromFile method
        Returns theList or None on error.
        """
        fprintf( fp, '%s %s %s\n', self.startTag, theList.name, theList.status )
        for item in theList:
            item.SMLhandler.toSML( item, fp )
        #end for
        fprintf( fp, '%s\n', self.endTag )
        return theList
    #end def

    def readline( fp ):
        """
        Static method to read a line from fp, split it
        return an list instance with line and split line
        """
        line = fp.readline()
        if len(line) == 0: 
            return None
        line = line[0:-1]
#        result = NTlist(line, *line.split())
        #print '>', result, '<'
        # Much quicker then previous NTlist stuff!
        if SMLhandler.debug: 
#            s = sprintf('%s l:%d> %s\n', SMLfileVersion, fp.NR, [line]+line.split())
            s = sprintf('%s l:%d> %s', SMLfileVersion, fp.NR, line)
            nTmessage(s)
        return [line]+line.split()
    #end def
    readline = staticmethod( readline )

    def fromFile( fileName, obj=None, **kwds)   :
        """
        Static method to restore new object from SML file.
        obj is carried along for convenience to pass an external info if needed.

        Returns newObj or None on error.
        """
#        nTdebug("--> fromFile")        
        if not os.path.exists( fileName ):
            nTerror('Error SMLhandler.fromFile: file "%s" does not exist\n', fileName )
            return None
        #end if
        fp   = SmlFile( fileName, 'r' )
        line = SMLhandler.readline( fp )
        if len(line) > 0 and SMLstarthandlers.has_key(line[1]):
            handler = SMLstarthandlers[line[1]]
            newObj  = handler.handle( line, fp, obj, **kwds )
        else:
            nTerror('SMLhandler.fromFile: invalid SML file line %d "%s"', fp.NR, line[0])
#        newObj  = smlhandler.handle( None, fp, obj )
        fp.close()
#        nTdebug('Restored %s from "%s"', newObj, fileName )
        return newObj
    #end def
    fromFile = staticmethod( fromFile )

    def toFile(self, object, fileName, **kwds)   :
        """
        Save element of theList to fileName for restoring later with fromFile method
        Returns object or None on error.
        """
        fp = open( fileName, 'w' )
        if not fp:
            nTerror('SMLhandle.toFile: opening "%s"\n', fileName)
            return None
        #end if
        fprintf( fp, '%s %s\n', smlhandler.startTag, SMLversion )

        if not hasattr(object,'SMLhandler'):
            nTerror('SMLHandler.toFile: object "%s" without SMLhandler method', object)
            fp.close()
            return None

        object.SMLhandler.toSML( object, fp, **kwds )
        fprintf( fp, '%s\n', smlhandler.endTag )

#        nTdebug('saved %s to "%s"', object, fileName ) # JFD adds; it's a duplicate of the nTdetail message.
        #end if
        return object
    #end def
#end class

# make one instance of the class that takes care of the basic things; i.e. initial first parse and inclusion of
# <SML> and </SML> tags
smlhandler = SMLhandler(name='SML')

# Make SML handler for NTlist
class SMLNTlistHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'NTlist' )
    #end def

    def handle(self, line, fp, obj=None):
        listObj = NTlist()
        return self.listHandler(listObj, fp, obj)
    #end def

    def toSML(self, theList, stream=sys.stdout, *args, **kwds):
        """
        Write element of theList to stream for restoring later with fromFile method
        Returns theList or None on error.
        """
        fprintf( stream, '%s\n', self.startTag )
        for item in theList:
            if hasattr(item,'SMLhandler') and item.SMLhandler != None:
                item.SMLhandler.toSML( item, stream, *args, **kwds )
            else:
                fprintf( stream, '%r\n', item )
            #end if
        #end for
        fprintf( stream, '%s\n', self.endTag )
        return theList
    #end def
#end class
NTlist.SMLhandler = SMLNTlistHandler()

# Make SMLhandlers for NTdict
class SMLNTdictHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'NTdict' )
    #end def

    def handle(self, line, fp, obj=None):
#        nTdebug("Now in SMLNTdictHandler#handle at line: %s" % str(line))
        dictObj = NTdict()
        return self.dictHandler(dictObj, fp, obj)
    #end def

    def toSML(self, theDict, stream=sys.stdout, *args, **kwds):
        """
        Write key value pairs of theDict to stream for restoring later with fromFile method
        Returns theDict or None on error.
        """
        fprintf( stream, '%s\n', self.startTag )
        for key,value in theDict.iteritems():
            fprintf( stream, '%s = ', key )
            if hasattr(value,'SMLhandler') and value.SMLhandler != None:
                value.SMLhandler.toSML( value, stream, *args, **kwds )
            else:
                fprintf( stream, '%r\n', value )
            #end if
        #end for
        fprintf( stream, '%s\n', self.endTag )
        return theDict
    #end def
#end class
NTdict.SMLhandler = SMLNTdictHandler()


# Make SMLhandlers for NTvalue
# Needed because it's a subclass of NTdict
class SMLNTvalueHandler( SMLhandler ):

    def __init__(self, name = 'NTvalue' ):
        SMLhandler.__init__( self, name = name )
    #end def

    def handle(self, line, fp, obj=None):
        nTdebug("Now in %s#handle at line: %s" % (getCallerName(), str(line)))
        dictObj = NTvalue(NaN)
        return self.dictHandler(dictObj, fp, obj)
    #end def

    def toSML(self, theDict, stream=sys.stdout, *args, **kwds):
        """
        Write key value pairs of theDict to stream for restoring later with fromFile method
        Returns theDict or None on error.
        """
#        fprintf( stream, '%s\n', self.startTag )
#        for key,value in theDict.iteritems():
#            fprintf( stream, '%s = ', key )
#            if hasattr(value,'SMLhandler') and value.SMLhandler != None:
#                value.SMLhandler.toSML( value, stream, *args, **kwds )
#            else:
#                fprintf( stream, '%r\n', value )
#            #end if
#        #end for
#        fprintf( stream, '%s\n', self.endTag )
        fprintf( stream, '%r\n', theDict )
        return theDict
    #end def
#end class
NTvalue.SMLhandler = SMLNTvalueHandler()


class SMLMoleculeHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'Molecule' )
    #end def

    def handle(self, line, fp, _tmp=None):
        """ The handle restores the attributes of Molecule
        """
        # Explicitly encode it because we want on the fly action for _sequence

        nameTuple = eval(' '.join(line[2:]))
        mol = Molecule( nameTuple[0] )
        if not mol:
            nTerror('SMLMoleculeHandler.handle: invalid line "%s"', line[0])
            return None
        #end if

        line = SMLhandler.readline( fp ) # Array of line plus words
        while line:
            n = len(line) # Number of words plus one.
            if n == 0:
                nTerror('SMLMoleculeHandler.handle: empty line')            
#            nTdebug("Line length (+1): %s and line: %s" % (n,line))
            key = line[1]
            if key==self.endTag:
                return self.endHandler( mol, None )
            # version 0.2: implement recursion
            if n > 3 and key=='_sequence'  and SMLstarthandlers.has_key(line[3]):
                _sequence = SMLstarthandlers[line[3]].handle( [' '.join(line[3:])] + line[3:], fp, mol )
                # Restore the sequence
                #print '>>', _sequence
                if SMLfileVersion < 0.23:
                # older _sequence format without N-, C-terminal defs <= 0.23
                    for chain, resName, resNum, convention in _sequence:
                        mol.addResidue( chain, resName, resNum, convention )
                    #end for
                else:
                    # Newer _sequence format with N-, C-terminal defs >= 0.23
                    for chain, resName, resNum, nTerminal, cTerminal, convention in _sequence:
                        mol.addResidue( chain, resName, resNum, convention, nTerminal, cTerminal )
                    #end for
                #end if
            elif n > 3 and SMLstarthandlers.has_key(line[3]):
                mol[key] = SMLstarthandlers[line[3]].handle( [' '.join(line[3:])] + line[3:], fp, mol )
            elif SMLendhandlers.has_key(key):
                nTerror('SMLMoleculeHandler.handle: skipping invalid closing tag "%s"', key)
            elif n > 3:
                mol[key] = eval(' '.join(line[3:]))
            else:
                nTerror('SMLMoleculeHandler.handle: incomplete line "%s"', line[0])
            #end if
            line = SMLhandler.readline( fp )
        #end while
        # we should not be here
        nTerror('SMLMoleculeHandler.handle: unterminated %s', self)
        return None
    #end def

    def endHandler(self, mol, _tmp=None):
#        nTdebug("In %s with SMLfileVersion %s" % ( getCallerName(), SMLfileVersion ))
        # Restore linkage
        mol.chains = mol._children
        mol._check()
        
        if SMLfileVersion < 0.25:
            if mol._convertResonanceSources(SMLfileVersion):
                nTerror("Failed SMLMoleculeHandler#" + getCallerName())
            # end if
        # end if            
        return mol
    #end def

    def toSML(self, mol, stream=sys.stdout ):
        """
        Write SML code for molecule to stream.
        """
        mol._sequence = NTlist()
        for res in mol.allResidues():
            mol._sequence.append( ( res.chain.name,
                                    res.translate(SMLsaveFormat) ,
                                    res.resNum,
                                    res.Nterminal,
                                    res.Cterminal,
                                    SMLsaveFormat ) ) 
        fprintf( stream, "%s  %r\n", self.startTag, mol.nameTuple(SMLsaveFormat) )
#       Can add attributes here; update endHandler if needed
        exportAttributeList = 'modelCount ranges archive_id'.split()
        for a in exportAttributeList:
            if not mol.has_key(a):
                nTcodeerror('In %s' % getCallerName())
                continue
            # end if            
            fprintf( stream, '%s = %r\n', a, mol[a] )
        #end for
        exportAttributeList = '_sequence chains resonanceSources bmrbEntryList pdbEntryList'.split()
        for exportAttribute in exportAttributeList:
#            nTdebug("Exporting molecule's %s" % exportAttribute)
            fprintf( stream, '%s = ' % exportAttribute)
            exportObject = mol[ exportAttribute ]
            exportObject.toSML( stream )
        # end for
        fprintf( stream, "%s\n", self.endTag )
    #end def
#end class
#register this handler
Molecule.SMLhandler = SMLMoleculeHandler()


class SMLChainHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'Chain' )
    #end def

    def handle(self, line, fp, molecule=None):
        # The handle restores the attributes of chain
        # Needs a valid molecule
        #print 'Chain.handle>', line, len(line)
        if molecule == None: 
            return None

        nameTuple = eval(' '.join(line[2:]))
        #print '>>', nameTuple, len(nameTuple)

        chain = molecule.decodeNameTuple(nameTuple)
        if chain == None:
            nTerror('SMLChainHandler.handle: invalid nameTuple %s, ==> Skipped chain', nameTuple)
            self.jumpToEndTag(fp)
            return None
        #end if
        return self.dictHandler(chain, fp, molecule)
    #end def

    def endHandler(self, chain, molecule=None):
        # Restore linkage
        chain.residues = chain._children
        return chain
    #end def

    def toSML(self, chain, stream=sys.stdout ):
        """
        Write SML code for chain to stream
        """
        # print value, error, model ontag line to speed up parsing and initialization
        fprintf( stream, "%s  %r\n", self.startTag, chain.nameTuple(SMLsaveFormat) )
#       Can add attributes here; update endHandler if needed
        for a in []:
            fprintf( stream, '%s = %r\n', a, chain[a] )
        #end for

        fprintf( stream, 'residues = ')
        chain.residues.toSML( stream )

        fprintf( stream, "%s\n", self.endTag )
    #end def
#end class
#register this handler
Chain.SMLhandler = SMLChainHandler()


class SMLResidueHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'Residue' )
    #end def

    def handle(self, line, fp, molecule=None):
        # The handle restores the attributes of residue
        # Needs a valid molecule
        if molecule == None: 
            return None

        nameTuple = eval(' '.join(line[2:]))
        res = molecule.decodeNameTuple(nameTuple)
        if res == None:
            nTwarning('SMLResidueHandler.handle: line %d, skipping nameTuple %s', fp.NR, str(nameTuple))
            self.jumpToEndTag(fp)
            return None
        #end if
        return self.dictHandler(res, fp, molecule)
    #end def

    def endHandler(self, res, molecule=None):
        # Restore linkage
        res.atoms = res._children
        return res
    #end def

    def toSML(self, res, stream=sys.stdout ):
        """
        Write SML code for residue to stream
        """
        fprintf( stream, "%s  %r\n", self.startTag, res.nameTuple(SMLsaveFormat) )
#       Can add attributes here; update endHandler if needed
        for a in []:
            fprintf( stream, '%s = %r\n', a, res[a] )
        #end for

        fprintf( stream, 'atoms = ')
        res.atoms.toSML( stream )

        fprintf( stream, "%s\n", self.endTag )
    #end def
#end class
#register this handler
Residue.SMLhandler = SMLResidueHandler()


class SMLAtomHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'Atom' )
    #end def

    def handle(self, line, fp, molecule=None):
        # The handle restores the attributes of atom
        # Needs a valid molecule
        if molecule == None:
            return None

        nameTuple = eval(' '.join(line[2:]))
        atm = molecule.decodeNameTuple(nameTuple)
        if atm == None: # TODO: check this code.
            # Could not find anything: to maintain compatibility of all Jurgen's old stuff; try to add it on the fly.
#            nTdebug('SMLAtomHandler.handle: line %d, could not properly decode nameTuple %s', fp.NR, str(nameTuple))
            resTuple = list(nameTuple)
            resTuple[3] = None
            resTuple = tuple(resTuple)
            res = molecule.decodeNameTuple(resTuple)
            if not res:
                nTwarning('SMLAtomHandler.handle: line %d, could not get residue, skipping nameTuple %s', fp.NR, str(nameTuple))
                self.jumpToEndTag(fp)
                return None

            # GWV: skip non-relevant N- and C-terminal atoms
            aDef = res.db.getAtomDefByName(nameTuple[3], convention=nameTuple[6])
            if aDef:
                if (   (not res.Nterminal and isNterminalAtom(aDef))
                    or (res.Nterminal and aDef.translate(INTERNAL_0) == 'HN')
                    or (not res.Cterminal and isCterminalAtom(aDef))
                   ):
#                    nTdebug('SMLAtomHandler.handle: line %d, skipping terminal atom: %s', fp.NR, str(nameTuple))
                    self.jumpToEndTag(fp)
                    return None
            #end if

            atm = res.addAtom(nameTuple[3], convention=nameTuple[6])
            if not atm:
                nTwarning('Failed to add atom in SMLAtomHandler to residue for tuple %s' % str(nameTuple))
                self.jumpToEndTag(fp)
                return None
            #end if
        #end if
        return self.dictHandler(atm, fp, molecule)
    #end def


    def endHandler(self, atm, molecule=None):
        # Restore the required linkages and indices
        for i,r in enumerate(atm.resonances):
            r.atom = atm
            r.resonanceIndex = i

        for i,c in enumerate(atm.coordinates):
            c.atom = atm
            c.model = i
        return atm
    #end def

    def toSML(self, atm, stream=sys.stdout ):
        """
        Write SML code for atom to stream
        """
        fprintf( stream, "%s  %r\n", self.startTag, atm.nameTuple(SMLsaveFormat) )
#       Can add attributes here; update endHandler if needed
        for a in ['shiftx']:
            if atm.has_key(a):
                fprintf( stream, '%s = %r\n', a, atm[a] )
        #end for

        # coordinates; only write when present
        if len(atm.coordinates) > 0:
            fprintf(stream,"coordinates = ")
            atm.coordinates.toSML( stream )
        # resonances; only write when present
        if len(atm.resonances) > 0:
            fprintf(stream,"resonances = ")
            atm.resonances.toSML( stream )

        # Minimize the number of lines by not outputting the default values
        if atm.stereoAssigned:
            fprintf( stream, 'stereoAssigned = True\n' )
        #end if

        fprintf( stream, "%s\n", self.endTag )
    #end def
#end class
#register this handler
Atom.SMLhandler = SMLAtomHandler()


#class SMLCoordinateHandler( SMLhandler ):
#
#    def __init__(self):
#        SMLhandler.__init__( self, name = 'Coordinate' )
#    #end def
#
#    def handle(self, line, fp, molecule=None):
#        # Explicit coding saved ca 30%
#        c = Coordinate(x=float(line[2]), y=float(line[3]), z=float(line[4]), Bfac=float(line[5]),occupancy=float(line[6]))
#        c.model = int(line[7])
#        line = self.readline( fp )
#        c.atomNameTuple = eval(line[0])
##        return self.dictHandler(c, fp, molecule)
#        line = self.readline( fp )
#        if line[0] == self.endTag:
#            self.endHandler(c, obj)
#            return c
#        #end if
#        # We should not be here
#        nTerror('SMLCoordinateHandler.handle: missing Coordinate endTag')
#        return None
#    #end def
#
#    def endHandler(self, c, molecule):
#        # Map the atomNameTuple
#        if obj == None: return None
#        atm = molecule.decodeNameTuple(c.atomNameTuple)
#        if atm == None:
#            nTerror('SMLCoordinateHandler.endHandler: invalid atomNameTuple (%s)', c.atomNameTuple)
#            return None
#        #end if
#        c.atom = atm
#        atm.coordinates.append(c)
#        return c
#    #end def
#
#    def toSML(self, c, stream ):
#        """
#            For coordinate
#        """
##        fprintf( stream, "%s\n", self.startTag)
##        for a in ['x','y','z','Bfac','occupancy','model']:
##            fprintf( stream, '%s = %s\n', a, repr(c[a]) )
##        #end for
#
#        # print x,y,z,Bfac,occupancy, model ontag line to speed up parsing and initialization
#        fprintf( stream, "%s %.3f %.3f %.3f %.3f %.3f %d\n",
#                         self.startTag,
#                         c.e[0], c.e[1], c.e[2],
#                         c.Bfac, c.occupancy,
#                         c.model
#               )
#        fprintf( stream, '%s\n', repr( c.atom.nameTuple(SMLsaveFormat) ) )
##        Can add attributes here; update handle
##        for a in ['model']:
##            fprintf( stream, '%s = %s\n', a, repr(c[a]) )
#        #end for
#
#        fprintf( stream, "%s\n", self.endTag )
#    #end def
##end class
#Coordinate.SMLhandler = SMLCoordinateHandler()

#Resonance inherits the SMLhandler from NTdict: that we do not want, so unassign it
Resonance.SMLhandler = None

class SMLPeakHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'Peak' )
    #end def

    def handle(self, line, fp, project=None):
        if SMLfileVersion <= 0.21:
            # older SML format <= 0.2
            pk = Peak( 0 )
        else:
            pk = Peak( int(line[2]) )
        return self.dictHandler(pk, fp, project)
    #end def

    # W0221 Arguments number differs from overridden method 
    # W0222 Signature differs from overridden method 
    # pylint: disable=W0221,W0222
    def endHandler(self, pk, project):
        if project == None:
            nTerror('Error SMLPeakHandler.endHandler: Undefined project\n')
            return None
        #end if
        if project.molecule == None:
            nTerror('Error SMLPeakHandler.endHandler: Undefined molecule\n')
            return None
        #end if

        if SMLfileVersion <= 0.21:
            pk.resonances = nTfill(None,pk.dimension)
            pk.positions  = NTlist(*pk.positions)
            del(pk['hasHeight'])
            del(pk['hasVolume'])
            pk.height = NTvalue( pk.height, pk.heightError, Peak.HEIGHT_VOLUME_FORMAT, Peak.HEIGHT_VOLUME_FORMAT2 )
            del(pk['heightError'])
            pk.volume = NTvalue( pk.volume, pk.volumeError, Peak.HEIGHT_VOLUME_FORMAT, Peak.HEIGHT_VOLUME_FORMAT2 )
            del(pk['volumeError'])

            ### REMARK: This restoring of resonances is dangerous, because it is not guranteed that the order and hence last
            #           resonance of atoms is always the same. Needs reviewing !!!

            # Check if we have to make the linkage
            if pk.atoms and project.molecule:
                #print '>>',pk.atoms
                for i in range(pk.dimension):
                    if pk.atoms[i] != None:
                        atm = project.molecule.decodeNameTuple(pk.atoms[i])
                        pk.resonances[i] = atm.resonances()
                    else:
                        pk.resonances[i] = None
                    #end if
                #end for
            #end if
        else:
            pk.height = NTvalue(pk.height[0],pk.height[1], Peak.HEIGHT_VOLUME_FORMAT, Peak.HEIGHT_VOLUME_FORMAT2)
            pk.volume = NTvalue(pk.volume[0],pk.volume[1], Peak.HEIGHT_VOLUME_FORMAT, Peak.HEIGHT_VOLUME_FORMAT2)
            pk.resonances = decode(pk.resonances, project)
        #end if
        return pk
    #end def

    def toSML(self, peak, fp):
        """
        Version 0.22: Use the encode for resonances
        """
        fprintf( fp, '%s  %d  %d\n', self.startTag, peak.dimension, peak.peakIndex )
        for a in ['positions']:
            fprintf( fp, '    %-15s = %r\n', a, peak[a] )
        #end for

        # special cases
        for a in ['height','volume']:
            fprintf( fp, '    %-15s = %r\n', a, peak[a].toTuple() )
        #end for
        if peak.has_key('xeasyIndex'):
            fprintf( fp, '    %-15s = %r\n', 'xeasyIndex', peak['xeasyIndex'] )
        # Resonances
        fprintf( fp, '    %-15s = %r\n', 'resonances', encode( peak.resonances ))
        fprintf( fp, '%s\n', self.endTag )
    #end def

#end class
Peak.SMLhandler = SMLPeakHandler()

class SMLPeakListHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'PeakList' )
    #end def

    def handle(self, line, fp, project=None):
        pl = PeakList( *line[2:] )
        if not self.listHandler(pl, fp, project): 
            return None
        if project: 
            project.peaks.append( pl )
        return pl
    #end def

    def toSML(self, pl, fp):
        return self.list2SML( pl, fp )
#end class
PeakList.SMLhandler = SMLPeakListHandler()

class SMLDistanceRestraintHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = DR_LEVEL )
    #end def

    def handle(self, line, fp, project=None):
        dr = DistanceRestraint( *line[2:] )
        return self.dictHandler(dr, fp, project)
    #end def

    # W0221 Arguments number differs from overridden method 
    # W0222 Signature differs from overridden method 
    # pylint: disable=W0221,W0222
    def endHandler(self, dr, project):
        # Parse the atomPairs tuples, map to molecule
        if project == None or project.molecule == None:
            return dr
        aps = dr.atomPairs
        dr.atomPairs = NTlist()
        for ap in aps:
            p0 = project.decodeNameTuple(ap[0])
            p1 = project.decodeNameTuple(ap[1])
            if p0 and p1:
                dr.appendPair( (p0, p1) )
                continue
            #end if
            if not p0: 
                nTerror('SMLDistanceRestraintHandler.endHandler: error p0 decoding %s', ap[0])
            if not p1: 
                nTerror('SMLDistanceRestraintHandler.endHandler: error p1 decoding %s', ap[1])
        #end for
        return dr
    #end def

    def toSML(self, dr, stream ):
        """
            For DistanceRestraint
        """
        fprintf( stream, "%s\n", self.startTag )
        for a in ['lower','upper' ]:
            fprintf( stream, '    %-15s = %s\n', a, repr(dr[a]) )
        #end for

        rl = []
        for r in dr.atomPairs:
            rl.append((r[0].nameTuple(SMLsaveFormat),r[1].nameTuple(SMLsaveFormat)))
        #end for
        fprintf( stream, '    %-15s = %s\n', 'atomPairs', repr( rl ) )
        fprintf( stream, "%s\n", self.endTag )
    #end def
#end class
DistanceRestraint.SMLhandler = SMLDistanceRestraintHandler()


class SMLDistanceRestraintListHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'DistanceRestraintList' )
    #end def

    def handle(self, line, fp, project=None):
        drl = DistanceRestraintList( *line[2:] )
        if not self.listHandler(drl, fp, project): 
            return None
        project.distances.append( drl )
        return drl
    #end def

    def toSML(self, drl, fp):
        self.list2SML( drl, fp )
    #end def
#end class
DistanceRestraintList.SMLhandler = SMLDistanceRestraintListHandler()


class SMLDihedralRestraintHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = AC_LEVEL )
    #end def

    def handle(self, line, fp, project=None):
        dr = DihedralRestraint( atoms=[], upper = 0.0 , lower =0.0 )
        return self.dictHandler(dr, fp, project)
    #end def

    # W0221 Arguments number differs from overridden method 
    # W0222 Signature differs from overridden method 
    # pylint: disable=W0221,W0222
    def endHandler(self, dr, project):
        # Parse the atoms nameTuples, map to molecule
        dr.atoms = decode( dr.atoms, project )
        if dr.atoms == None or None in dr.atoms:
            nTerror('SMLDihedralRestraintHandler.endHandler: invalid atom(s) %s', dr.atoms)
        return dr
    #end def

    def toSML(self, dr, stream ):
        """
        """
        fprintf( stream, "%s\n", self.startTag )
        for a in ['lower','upper' ]:
            fprintf( stream, '    %-15s = %s\n', a, repr(dr[a]) )
        #end for
        fprintf( stream, '    %-15s = %s\n', 'atoms', repr(encode(dr.atoms)) )

        fprintf( stream, "%s\n", self.endTag )
    #end def
#end class
DihedralRestraint.SMLhandler = SMLDihedralRestraintHandler()

class SMLDihedralRestraintListHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'DihedralRestraintList' )
    #end def

    def handle(self, line, fp, project=None):
        drl = DihedralRestraintList( *line[2:] )
        if not self.listHandler(drl, fp, project): 
            return None
        project.dihedrals.append( drl )
        return drl
    #end def

    def toSML(self, drl, fp):
        self.list2SML( drl, fp )
    #end def
#end class
DihedralRestraintList.SMLhandler = SMLDihedralRestraintListHandler()


class SMLRDCRestraintHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = RDC_LEVEL )
    #end def

    def handle(self, line, fp, project=None):
        dr = RDCRestraint( atoms=[], upper = 0.0 , lower =0.0 )
        return self.dictHandler(dr, fp, project)
    #end def

    # W0221 Arguments number differs from overridden method 
    # W0222 Signature differs from overridden method 
    # pylint: disable=W0221,W0222
    def endHandler(self, dr, project):
        # Parse the atoms nameTuples, map to molecule
        if project == None or project.molecule == None: 
            return dr
        aps = dr.atomPairs
        dr.atomPairs = NTlist()
        for ap in aps:
            p0 = project.decodeNameTuple(ap[0])
            p1 = project.decodeNameTuple(ap[1])
            if p0 and p1:
                dr.appendPair( (p0, p1) )
            else:
                if not p0: 
                    nTerror('SMLRDCRestraintHandler.endHandler: error decoding %s', ap[0])
                if not p1: 
                    nTerror('SMLRDCRestraintHandler.endHandler: error decoding %s', ap[1])
            #end if
        #end for
        return dr
    #end def

    def toSML(self, dr, stream ):
        """
            For RDCRestraint (based on DistanceRestraint)
        """
        fprintf( stream, "%s\n", self.startTag )
        for a in ['lower','upper' ]:
            fprintf( stream, '    %-15s = %s\n', a, repr(dr[a]) )
        #end for

        rl = []
        for r in dr.atomPairs:
            rl.append((r[0].nameTuple(SMLsaveFormat),r[1].nameTuple(SMLsaveFormat)))
        #end for
        fprintf( stream, '    %-15s = %s\n', 'atomPairs', repr( rl ) )
        fprintf( stream, "%s\n", self.endTag )
    #end def
#end class
RDCRestraint.SMLhandler = SMLRDCRestraintHandler()


class SMLRDCRestraintListHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'RDCRestraintList' )
    #end def

    def handle(self, line, fp, project=None):
        drl = RDCRestraintList( *line[2:] )
        if not self.listHandler(drl, fp, project): 
            return None
        project.rdcs.append( drl )
        return drl
    #end def

    def toSML(self, drl, fp):
        self.list2SML( drl, fp )
    #end def
#end class
RDCRestraintList.SMLhandler = SMLRDCRestraintListHandler()

## TODO: Didn't think this was needed.
#class SMLResonanceHandler( SMLhandler ):
#
#    def __init__(self):
#        SMLhandler.__init__( self, name = RESONANCE_LEVEL )
#    #end def
#
#    def handle(self, line, fp, project=None):
##        return True
#        r = Resonance()
#        return self.dictHandler(r, fp, project)
#    #end def
#
#    def toSML(self, r, stream ):
#        """
#            For Resonance (based on DistanceRestraint)
#        """
##        pass
#        fprintf( stream, "%s\n", self.startTag )
#        for a in ['value' ]:
#            fprintf( stream, '    %-15s = %s\n', a, repr(r[a]) )
#        #end for
#        fprintf( stream, "%s\n", self.endTag )
#    #end def
##end class
#Resonance.SMLhandler = SMLResonanceHandler()


class SMLNTListWithAttrHandler( SMLhandler ):
#    def __init__(self, name ):
#        SMLhandler.__init__( self, name = name ) # adds this handler for when restoring.
#        self.SML_SAVE_ATTRIBUTE_LIST   
    #end def
    SML_SAVE_ATTRIBUTE_LIST = None # overwritten by individual class instance to be saved.
    
    def handle(self, line, fp, obj=None):
#        nTdebug("Now in SMLNTListWithAttrHandler#handle at line: %s" % str(line))
        rlTop = NTdict()
        rlTop = self.dictHandler(rlTop, fp)        
        if rlTop == None:
            nTerror("Failed to read resonance list top object.") 
            return None
        if not obj:
            nTerror("In SMLNTListWithAttrHandler#endHandler no obj initialized")
            return
        # Skip the actual resonance creation because that is already done by molecule's handle.
        # obj is molecule This line is the only ResonanceList specific action to generalize further. 
        rl = obj.newResonances(skipAtomResonanceCreation = True ) 
        for key in self.SML_SAVE_ATTRIBUTE_LIST:
            if not hasattr( rlTop, key ):
#                nTdebug("Failed to read expected attribute in top object: %s. Set to None." % key)
                setattr(rl, key, None)
            else:
                setattr(rl, key, getattr(rlTop,key))
            # endif
#        rl.addList(rlTop.theList) # not done yet.
#        nTmessage("==> Restored %s" % rl)
        return rl
    #end def
    
#    def endHandler(self, rl, project):
#        nTdebug("Now in SMLNTListWithAttrHandler#endHandler doing nothing")
#        pass
    #end def
        
    def toSML(self, rl, fp):
        'This list will be encapsulated in a dictionary so the additional attributes can be saved.'        
        fprintf( fp, '%s\n', self.startTag )
        
        # Build customary dictionary as top object to save.     
        theDict = NTdict()
        for key in self.SML_SAVE_ATTRIBUTE_LIST:
            if not hasattr( rl, key ):
                nTcodeerror("%s failed to see attribute in top object: %s" % (rl, key))
                return
            theDict[key] = getattr(rl, key)
        theDict.theList = NTlist()
#        theDict.theList.addList(rl) # TODO: when items DO get saved.

        # save it regardless of content.
        for key,value in theDict.iteritems():
            fprintf( fp, '%s = ', key )
            if hasattr(value,'SMLhandler') and value.SMLhandler != None:
                value.SMLhandler.toSML( value, fp )
            else:
                fprintf( fp, '%r\n', value )
            #end if
        #end for            
        fprintf( fp, '%s\n', self.endTag )
        return rl
    #end def
#end class

# Generalized
ResonanceList.SMLhandler = SMLNTListWithAttrHandler(name = 'ResonanceList')
ResonanceList.SMLhandler.SML_SAVE_ATTRIBUTE_LIST = ResonanceList.SML_SAVE_ATTRIBUTE_LIST # pylint: disable=C0103


class SMLCoplanarHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = COPLANAR_LEVEL )
    #end def

    def handle(self, line, fp, project=None):
        return # ask Geerten for input
#        coplanar = Coplanar()
#        return self.dictHandler(coplanar, fp, project)
    #end def

    # W0221 Arguments number differs from overridden method 
    # W0222 Signature differs from overridden method 
    # pylint: disable=W0221,W0222
    def endHandler(self, coplanar, project):
        return # ask Geerten for input
    #end def

    def toSML(self, coplanar, stream ):
        """
            For Coplanar (based on DistanceRestraint)
        """
        return # ask Geerten for input
    #end def
#end class


class SMLCoplanarListHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'CoplanarList' )
    #end def

    def handle(self, line, fp, project=None):
        return
    #end def

    def toSML(self, drl, fp):
        return
    #end def
#end class

class SMLMolDefHandler( SMLhandler ):
    """Just a container to MolDef SMl
    """
    def __init__(self):
        SMLhandler.__init__( self, name = 'MolDef' )
    #end def
#end class
MolDef.SMLhandler = SMLMolDefHandler()

class SMLResidueDefHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'ResidueDef' )
    #end def

    def handle(self, line, fp, molDef=None):
        if molDef == None:
            nTerror('SMLResidueDefHandler.handle: file "%s" line %d, undefined molDef', fp.name, fp.NR)
            self.jumpToEndTag(fp)
            return None
        #end if
        if SMLfileVersion < 0.24:
            if len(line) < 5:
                nTerror('SMLResidueDefHandler.handle: file "%s" line %d, incomplete ResidueDef syntax "%s"', fp.name, fp.NR, line)
                self.jumpToEndTag(fp)
                return None
            #end if
#            if line[4] != INTERNAL:
#                nTerror('SMLResidueDefHandler.handle: file "%s" line %d, convention "%s" differs from current (%s)', 
#                        fp.name, fp.NR, line[4], INTERNAL)
#                self.jumpToEndTag(fp)
#                return None
#            #end if
            resDef = molDef.appendResidueDef(line[2], shortName=line[3])
        else:
            if len(line) < 4:
                nTerror('SMLResidueDefHandler.handle: file "%s" line %d, incomplete ResidueDef syntax "%s"', fp.name, fp.NR, line)
                self.jumpToEndTag(fp)
                return None
            #end if
            resDef = molDef.appendResidueDef(line[2])
        #endif

        if not resDef:
            nTerror('SMLResidueDefHandler.handle: file "%s" line %d, error initiating ResidueDef instance "%s"', fp.name, fp.NR, line[2])
            self.jumpToEndTag(fp)
            return None
        #end if
        return self.dictHandler(resDef, fp, resDef)
    #end def

    def endHandler(self, resDef, obj=None):
        resDef.postProcess()
        return resDef
    #end def

    # W0221 Arguments number differs from overridden method 
    # W0222 Signature differs from overridden method 
    # pylint: disable=W0221,W0222
    def toSML(self, resDef, stream = sys.stdout, convention = INTERNAL  ):
        """Store resDef in SML format
        """
        fprintf( stream, '\n#=======================================================================\n')
        fprintf( stream,   '#%s \t%-8s %-8s\n', ' '*len(self.startTag), 'name', 'convention')
        fprintf( stream,   '%s  \t%-8s %-8s\n', self.startTag, resDef.translate(convention), convention)
        fprintf( stream,   '#=======================================================================\n')

        # saving different residue attributes
        for attr in ['commonName','shortName','comment','nameDict']:
            fprintf( stream, "\t%-10s = %r\n", attr, resDef[attr] )
        #end for

        # clean the properties list
        props = []
        for prop in resDef.properties:
            # Do not store name and residueDef.name as property. Add those dynamically upon reading
            if not prop in [resDef.name, resDef.shortName] and not prop in props:
                props.append(prop)
            #end if
        #end for
        fprintf( stream, "\t%-10s = %r\n", 'properties', props )

        fprintf( stream, "\n\t%-10s = %s\n", 'dihedrals', '<NTlist>') # for readability (tabs), write it explicitly
        for d in resDef.dihedrals:
            d.SMLhandler.toSML( d, stream, convention=convention )
        fprintf( stream, "\t%s\n", '</NTlist>')

        fprintf( stream, "\n\t%-10s = %s\n", 'atoms', '<NTlist>') # for readability (tabs), write it explicitly
        for a in resDef.atoms:
            a.SMLhandler.toSML( a, stream, convention=convention )
        fprintf( stream, "\t%s\n", '</NTlist>')

        fprintf( stream,   '%s\n', self.endTag)
        fprintf( stream,   '#=======================================================================\n')
    #end def
#end class
ResidueDef.SMLhandler = SMLResidueDefHandler()

class SMLDihedralDefHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'DihedralDef' )
    #end def

    def handle(self, line, fp, resDef=None):
        if resDef == None:
            nTerror('DihedralDef.handle: line %d, undefined resDef', fp.NR)
            self.jumpToEndTag(fp)
            return None
        #end if
        if len(line) < 3:
            nTerror('DihedralDef.handle: line %d, incomplete DihedralDef syntax "%s"', fp.NR, line)
            self.jumpToEndTag(fp)
            return None
        #end if
        dihedDef = resDef.appendDihedral(line[2])
        return self.dictHandler(dihedDef, fp, None)
    #end def

    def endHandler(self, dihedDef, obj=None):
        dihedDef.postProcess()
        return dihedDef
    #end def

    # W0221 Arguments number differs from overridden method 
    # W0222 Signature differs from overridden method 
    # pylint: disable=W0221,W0222
    def toSML(self, dihedDef, stream = sys.stdout, convention = INTERNAL  ):
        """Store dihedDef in SML format
        """
        #print '>', convention
        fprintf( stream, '\t#---------------------------------------------------------------\n')
        fprintf( stream, '\t%s %-8s\n', self.startTag, dihedDef.name)
        fprintf( stream, '\t#---------------------------------------------------------------\n')

        if convention == INTERNAL:
            atms = dihedDef.atoms
        else:
            # convert atoms
            atms = []
            for resId,atmName in dihedDef.atoms:
                if resId != 0:
                    nTwarning('DihedralDef.exportDef: %s topology (%d,%s) skipped translation', dihedDef, resId, atmName)
                    atms.append( (resId,atmName) )
                elif not atmName in dihedDef.residueDef:
                    nTerror('DihedralDef.exportDef: %s topology (%d,%s) not decoded', dihedDef, resId, atmName)
                    atms.append( (resId,atmName) )
                else:
                    atm = dihedDef.residueDef[atmName]
                    atms.append( (resId,atm.translate(convention)) )
                #end if
            #end for
            #print 'atms', atms
        #end if
        fprintf( stream, "\t\t%-8s = %r\n", 'atoms', atms )

        for attr in ['karplus']:
            fprintf( stream, "\t\t%-8s = %r\n", attr, dihedDef[attr] )
        #end for

        fprintf( stream, '\t%s\n', self.endTag)
    #end def
#end class
DihedralDef.SMLhandler = SMLDihedralDefHandler()

class SMLAtomDefHandler( SMLhandler ):

    def __init__(self):
        SMLhandler.__init__( self, name = 'AtomDef' )
    #end def

    def handle(self, line, fp, resDef=None):
        if resDef == None:
            nTerror('AtomDef.handle: line %d, undefined resDef', fp.NR)
            self.jumpToEndTag(fp)
            return None
        #end if
        if len(line) < 3:
            nTerror('AtomDef.handle: line %d, incomplete AtomDef syntax "%s"', fp.NR, line)
            self.jumpToEndTag(fp)
            return None
        #end if
        atmDef = resDef.appendAtomDef(line[2])
        return self.dictHandler(atmDef, fp, None)
    #end def

    def endHandler(self, atmDef, obj=None):
        atmDef.postProcess()
        return atmDef
    #end def

    # W0221 Arguments number differs from overridden method 
    # W0222 Signature differs from overridden method 
    # pylint: disable=W0221,W0222
    def toSML(self, atmDef, stream = sys.stdout, convention = INTERNAL  ): 
        """Store dihedDef in SML format
        """
        #print '>', convention
        fprintf( stream, '\t#---------------------------------------------------------------\n')
        fprintf( stream, '\t%s %-8s\n', self.startTag, atmDef.translate(convention) )
        fprintf( stream, '\t#---------------------------------------------------------------\n')

        # Topology; optionally convert
        if convention == INTERNAL:
            top2 = atmDef.topology
        else:
            # convert topology
            top2 = []
            for resId,atmName in atmDef.topology:
                if resId != 0:
                    nTwarning('AtomDef.exportDef: %s topology (%d,%s) skipped translation', atmDef, resId, atmName)
                    top2.append( (resId,atmName) )
                elif not atmName in atmDef.residueDef:
                    nTerror('AtomDef.exportDef: %s topology (%d,%s) not decoded', atmDef, resId, atmName)
                    top2.append( (resId,atmName) )
                else:
                    atm = atmDef.residueDef[atmName]
                    top2.append( (resId,atm.translate(convention)) )
                #end if
            #end for
            #print 'top2', top2
        #end if
        fprintf( stream, "\t\t%-10s = %r\n", 'topology', top2 )

        # real; optionally convert
        if convention == INTERNAL or len(atmDef.real) == 0:
            real2 = atmDef.real
        else:
            real2 = []
            for a in atmDef.real:
                adef = atmDef.residueDef.getAtomDefByName( a )
                if adef == None:
                    nTerror('AtomDef.exportDef: %s real atom "%s" not decoded', atmDef, a)
                else:
                    real2.append( adef.translate( convention ) )
                #end if
            #end for
        #end if
        fprintf( stream, "\t\t%-10s = %r\n", 'real', real2 )

        # pseudo; optionally convert
        if convention == INTERNAL or atmDef.pseudo == None:
            pseudo2 = atmDef.pseudo
        else:
            pseudo2 = None
            adef = atmDef.residueDef.getAtomDefByName( atmDef.pseudo )
            if adef == None:
                nTerror('AtomDef.exportDef: %s pseudo atom "%s" not decoded', atmDef, atmDef.pseudo)
            else:
                pseudo2 = adef.translate( convention )
            #end for
        #end if
        fprintf( stream, "\t\t%-10s = %r\n", 'pseudo', pseudo2 )

        # Others
        for attr in ['nameDict','aliases','type','spinType','shift','hetatm']:
            if atmDef.has_key(attr):
                fprintf( stream, "\t\t%-10s = %r\n", attr, atmDef[attr] )
        #end for

        # clean the properties list
        props = []
        for prop in atmDef.properties:
            # Do not store name and residueDef.name as property. Add those dynamically upon reading
            if not prop in [atmDef.name, atmDef.residueDef.name, atmDef.residueDef.shortName, atmDef.spinType] and not prop in props:
                props.append(prop)
            #end if
        #end for
        fprintf( stream, "\t\t%-10s = %r\n", 'properties', props )

        fprintf( stream, '\t%s\n', self.endTag)
    #end def
#end class
AtomDef.SMLhandler = SMLAtomDefHandler()


def obj2SML( obj, smlFile, **kwds ):
    """
    Generate SML file from object.
    Return obj or None on error
    """
    if smlhandler.toFile(obj, smlFile, **kwds) == None:
        return None
    return obj
#end def

def sML2obj( smlFile, externalObject=None ):
    """
    Generate obj from smlFile
    """
#    nTdebug("--> sML2obj")
    obj = smlhandler.fromFile(smlFile, externalObject)
    return obj
#end def

#-----------------------------------------------------------------------------
# Two handy (?) routines
#-----------------------------------------------------------------------------

def encode( objects ):
    """Return a list of nametuples encoding the molecule objects (chains, residues, atoms)
    """
    result = NTlist()
    for obj in objects:
        if (obj == None):
            result.append(None)
        else:
            result.append( obj.nameTuple(SMLsaveFormat) )
        #end if
    #end for
    return result
#end def

def decode( nameTuples, refObj ):
    """
    Return a list objects, decoding the nametuples relative to refObj
    """
    result = NTlist()
    for nt in nameTuples:
        if refObj == None or nt == None:
            result.append(None)
        else:
            result.append( refObj.decodeNameTuple( nt ) )
        #end if
    #end for
    return result
#end def