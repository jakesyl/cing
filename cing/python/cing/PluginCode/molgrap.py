"""
Adds methods:
    Molecule.export2gif()
    
Molmol fails to compile on Mountain Lion OSX as of 2012-08-08 on development machine.  
Actually, this works again with XQuartz installed and symbolic links from
/usr/X11R6 to /opt/X11R6 etc.  
"""
from cing import cingDirMolmolScripts
from cing import cingDirTmp
from cing import cingPythonCingDir
from cing import cingRoot
from cing import issueListUrl
from cing.Libs import disk
from cing.Libs.Imagery import convertImageMagick
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.Libs.TypeChecking import check_string
from cing.Libs.TypeChecking import check_type
from cing.core.constants import * #@UnusedWildImport
from cing.core.molecule import Molecule
from cing.core.parameters import cingPaths
from cing.core.parameters import directories
from glob import glob

if True: # block
    useModule = True
    if not cingPaths.convert:
        nTdebug("Missing convert which is a dep for Molgrap")
        useModule = False
    if not cingPaths.ghostscript:
        nTdebug("Missing ghostscript which is a dep for Molgrap")
        useModule = False
    if not cingPaths.molmol:
        nTdebug("Missing molmol which is a dep for Molgrap")
        useModule = False
    if not cingPaths.povray:
        nTdebug("Missing povray which is a dep for Molgrap")
        useModule = False

    if not useModule:
        raise ImportWarning('Molgrap')
#    nTmessage('Using Molgrap')

class Molgrap(NTdict):
    def __init__(self, backcolor = 'cing_turqoise', project = None):
        NTdict.__init__(self)
        self.csh_script_dir = cingDirMolmolScripts
        self.backcolor = backcolor # see csh script definitions.
#        self.backcolor = 'bmrb_yellow' # see csh script definitions.
#        self.backcolor = 'cing_turqoise' # see csh script definitions.
#        self.backcolor = 'white' # see csh script definitions.
        self.projectDirTmp = cingDirTmp
        if project:
            self.projectDirTmp = os.path.abspath(project.path(directories.tmp))
#            nTdebug("Resetting Molgrap.projectDirTmp from %s to %s" % (cingDirTmp, self.projectDirTmp))
#        nTdebug('Using self.projectDirTmp: ' + self.projectDirTmp)

    def run(self, molecule, path, export = True):
        """
        Creates a large gif to path for the given molecule.
        Return True on error and False on success.
        """
        if molecule.modelCount == 0:
            nTwarning('runMolgrap: no models for "%s"', molecule)
            return

        if not os.environ.has_key('MOLMOLHOME'):
            nTmessage('MOLMOLHOME not defined by user, using a temporary one')
            os.putenv('MOLMOLHOME', self.projectDirTmp)

        apath = os.path.abspath(path)
        if apath != path:
#            nTdebug("Using the absolute path ["+apath+"] from relative path: [" +path+"]")
            path = apath
        root, file, _ext = nTpath(path)
        entry_code = file


        if root and not os.path.exists(root):
            nTerror("Molgrap.run: Given path root is absent; not creating.")
            return True

        pdb_first_file_name = os.path.join(self.projectDirTmp, file + "_001.pdb")
        pov_file_name = os.path.join(self.projectDirTmp, file + ".pov")
        pov_cor_file_name = os.path.join(self.projectDirTmp, file + "_cor.pov")

#        nTdebug( "pdb_first_file_name: "+ pdb_first_file_name)

        if not os.path.exists(pdb_first_file_name):
            export = True

        if export:
#            nTdebug("First looking for atoms that should not be fed to molmol")
#            nTdebug("Just as a side note once a Calcium in an xeasy project example screwed up the image generation.")

#            skippedAtoms = [] # Keep a list of skipped atoms for later
#            skippedResidues = []
#            for res in molecule.allResidues():
##                TODO: why do the ions from the example xeasy project need to be removed here?
##                they cause molmol to write an invalid povray file.
##                consider switching to PyMol.
#                if not (res.hasProperties('protein') or res.hasProperties('nucleic')):
#                    skippedResidues.append(res)
#                    for atm in res.allAtoms():
#                        atm.pdbSkipRecord = True
#                        skippedAtoms.append( atm )
#            if skippedResidues:
#                nTwarning('Molgrap.run: non-protein residues will be skipped:' + repr(skippedResidues))
            # Molmol speaks Dyana which is close to cyana but residue names need to be translated to
            # was CYANA
            molecule.toPDB(pdb_first_file_name, convention = IUPAC, model = 0)
            # Restore the 'default' state
#            for atm in skippedAtoms:
#                atm.pdbSkipRecord = False

        if not os.path.exists(pdb_first_file_name):
            nTerror("Molgrap.run: Failed to materialize first model PDB file")
            return True

#        nTdebug("Doing molmol on: "+ entry_code)

        status = self._make_molmol_pov_file(
            pdb_first_file_name,
            entry_code,
            self.backcolor
        )

        if status:
            nTerror("Molgrap.run: while doing molmol for: " + entry_code)
            return True

        if not os.path.isfile(pov_file_name):
            nTerror('Molgrap.run: failed to generate povray file "%s" for %s', pov_file_name, entry_code)
            return True

        status = self._substitute_nans(
                pov_file_name,
                pov_cor_file_name
            )
        if status:
            nTerror("Molgrap.run: Doing molmol_povray_substitute._substitute_nans for: " + entry_code)
            return True

        if not os.path.isfile(pov_cor_file_name):
            nTerror("Molgrap.run: no corrected pov ray file generated for: " + entry_code)
            return True

#        print "DEBUG: Doing render/convert", entry_code

        status = self._render_convert_pov_file(
            pov_file_name = pov_cor_file_name,
            id = entry_code,
            results_dir = root,
            )
        if status:
            nTmessage( "Molgrap.run: rendered/converted entry: %s" % entry_code)
            return True
        # end if
#        ## Remove temporary files if successful and possible
        if 1: # DEFAULT: True
            try:
                os.unlink( pdb_first_file_name )
                os.unlink( pov_file_name )
                os.unlink( pov_cor_file_name )
            except:
                pass
            # end try
        # end if

    def _make_molmol_pov_file(self, pdb_file_name, id, backcolor):
        """
        Makes molmol images using a csh script. Note that these commands are only valid
        on Unix.
        """
        script_file_name = os.path.join (self.projectDirTmp, id + "_molmol.csh")
        log_file_name = os.path.join (self.projectDirTmp, id + "_molmol_python.log")
        script_file = open(script_file_name, 'w')
        script_file.write('#!/bin/csh\n')
        script_file.write('set id              = %s\n' % id)
        script_file.write('set csh_script_dir  = %s\n' % self.csh_script_dir)
        script_file.write('set tmp_dir         = %s\n' % self.projectDirTmp)
        script_file.write('set pdb_file        = %s\n' % pdb_file_name)
        script_file.write('set backcolor       = %s\n' % backcolor)
        script_file.write('set executableMm    = %s\n' % cingPaths.molmol)
        script_file.write('set mac_dir         = %s\n' % os.path.join(cingRoot, "scripts", "molmol"))
        script_file.write('\n')
        script_file.write('$csh_script_dir/molmol_image.csh $pdb_file $tmp_dir $id $csh_script_dir $backcolor $executableMm $mac_dir \n')
        script_file.write('exit $status\n')
        script_file.close()
        os.chmod(script_file_name, 0755)
        program = ExecuteProgram(script_file_name, rootPath = self.projectDirTmp, redirectOutputToFile = log_file_name)
        if program(""):
            nTerror("Failed shell command: " + script_file_name)
            return True
#        try:
#            os.unlink(script_file_name)
#            os.unlink(log_file_name)
#        except:
#            pass
        return None # not needed
    def _render_convert_pov_file(self, pov_file_name, id, results_dir):
        """
        Render pov ray file and convert output using a csh script.
        """

        script_file_name = os.path.join (self.projectDirTmp, id + "_render_convert_pov.csh")
        log_file_name = os.path.join (self.projectDirTmp, id + "_render_convert_pov_python.log")
        script_file = open(script_file_name, 'w')
        script_file.write('#!/bin/csh\n')
        script_file.write('set id              = %s\n' % id)
        script_file.write('set csh_script_dir  = %s\n' % self.csh_script_dir)
        script_file.write('set results_dir     = %s\n' % results_dir)
        script_file.write('set tmp_dir         = %s\n' % self.projectDirTmp)
        script_file.write('set pov_file_name   = %s\n' % pov_file_name)
        script_file.write('set executablePov   = %s\n' % cingPaths.povray)
        script_file.write('set executableConv  = %s\n' % cingPaths.convert)
        script_file.write('\n')
        script_file.write('$csh_script_dir/render_convert.csh $pov_file_name $tmp_dir $id $results_dir $executablePov $executableConv \n')
        script_file.write('exit $status\n')
        script_file.close()
        os.chmod(script_file_name, 0755)


        program = ExecuteProgram(script_file_name, rootPath = self.projectDirTmp, redirectOutputToFile = log_file_name)
        if program(""):
            nTerror("Failed shell command: " + script_file_name)
            nTerror("Suggestion 1: Have you installed povray-includes or similar?")
            nTerror("              For some Linuxes the file 'colors.inc' doesn't come with povray")
            nTerror("Suggestion 2: Are the file permissions in povray.conf lenient enough? See e.g. [File I/O Security] in:")
            nTerror("                /opt/local/etc/povray/3.6/povray.conf AND ~/.povray/3.6/povray.conf")
            nTerror("Suggestion 3: Complex X-ray topology then consider looking at %s%s" % (issueListUrl,233))
            return True
#        try:
#            os.unlink(script_file_name)
#            os.unlink(log_file_name)
#        except:
#            pass
        return None # not needed

    def _substitute_nans(self, file_name_in, file_name_out):
        """
        Setup replacement lists
        Can not use a dictionary as order of replacements matter.
        """
        org = [
            r'<nan, nan, nan>, <nan, nan, nan>, <nan, nan, nan>',
            r'<nan, nan, nan>',
            r'<nan, nan,',
            ]
        new = [
            r'<0.0, 0.0, 0.0>, <0.1, 0.0, 0.0>, <0.0, 0.1, 0.0>',
            r'<0.0, 0.0, 0.0>',
            r'<0.0, 0.0,',
            ]
        self._substitute(file_name_in, file_name_out, org, new)

    def _substitute(self, file_name_in, file_name_out, org, new):
        """
        Substitute from a dictionary the content of a file writting to another
        """

        output_text = open(file_name_in, 'r').read()
        for i in range(len(org)):
            #print "DEBUG: Doing replace of: org[i]"
            output_text = output_text.replace(org[i], new[i])
        open(file_name_out, 'w').write(output_text)

def export2gif(molecule, pathMolGif, project = None):
    """Return True on error but will still put a default image in."""
    check_type(molecule, 'Molecule')
    check_string(pathMolGif)
    if project:
        check_type(project, 'Project')
#    nTdebug("Now in cing.Plugincode.molgrap#export2gif")
    m = Molgrap(project = project)
    m.run(molecule, pathMolGif)
    failed = False
    if not os.path.exists(pathMolGif):
        failed = True
        src =  os.path.join( cingPythonCingDir, 'PluginCode', DATA_STR, 'UnknownImage.gif' )
#        if os.path.exists(pathMolGif): # disable when done testing.
#            os.unlink(pathMolGif)
        nTmessage("copying default image from %s to %s" % (src, pathMolGif))
#        os.link(src, pathMolGif) # us a real copy JFD: fails between 2 filesystems
        disk.copy(src, pathMolGif) # us a real copy
#        os.symlink(src, pathMolGif) # funny, the extension on mac fails to show up for this file only; other extensions are shown ok...
    # end if
    pathMolGifPinup = pathMolGif[:-4] + '_pin.gif'
    if convertImageMagick(pathMolGif, pathMolGifPinup, options='-geometry 114x80'):
        nTerror("convertImageMagick failed for: " + pathMolGifPinup)
    # end if
    
    if failed:
        return True
    return None


Molecule.export2gif = export2gif

def removeTempFiles( todoDir ):
#    whatifDir        = project.mkdir( project.molecule.name, project.moleculeDirectories.whatif  )
    nTdebug("Removing temporary files generated by molgrap")
    try:
#        removeListLocal = ["prodata", "ps.number", "aqua.cmm", "resdefs.dat", "mplot.in", '.log' ]
        removeList = []
#        for fn in removeListLocal:
#            removeList.append( os.path.join(todoDir, fn) )

        for extension in [ "mol_*" ]:
            for fn in glob(os.path.join(todoDir,extension)):
                removeList.append(fn)
        for fn in removeList:
            if not os.path.exists(fn):
                nTdebug("molgrap.removeTempFiles: Expected to find a file to be removed but it doesn't exist: " + fn )
                continue
#            nTdebug("Removing: " + fn)
            os.unlink(fn)
    except:
        nTdebug("molgrap.removeTempFiles: Failed to remove all temporary files that were expected")
#end def

# register the functions
methods = []