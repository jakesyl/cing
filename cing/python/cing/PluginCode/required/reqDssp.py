'required items for this plugin for CING setup'
from cing.Libs.NTutils import * #@UnusedWildImport
from cing.PluginCode.required.reqProcheck import * #@UnusedWildImport

DSSP_STR = "dssp" # key to the entities (atoms, residues, etc under which the results will be stored
DSSP_ID_STR = 'dssp_id'

DSSP_H = 'H'
DSSP_S = 'S'
DSSP_C = ' '
DSSP_ID_H = 0
DSSP_ID_S = 1
DSSP_ID_C = 2

mapDssp2Int = {DSSP_H: DSSP_ID_H, DSSP_S : DSSP_ID_S, DSSP_C : DSSP_ID_C, None: None}

def to3StateDssp( strNTList ):
    """Personal communications JFD with Rob Hooft and Gert Vriend.

    3, H -> H
    B, E -> S
    space, S, G, T -> coil (represented by ' ')

    See namesake method in procheck class.
    """
    result = NTlist()
    for c in strNTList:
        n = DSSP_C
        if c == '3' or c == 'H':
            n = DSSP_H
        # end if
        elif c == 'B' or c == 'E':
            n = DSSP_S
        # end if
        result.append( n )
    return result
# end def

def getDsspSecStructConsensus( res ):
    """ Returns None for error, or one of ['H', 'S', ' ' ]
    NB: Always returns one of the above three even if they're all a third occurring.
    """
    secStructList = res.getDeepByKeys(DSSP_STR,SECSTRUCT_STR)
    result = None
    if secStructList:
        secStructList = to3StateDssp( secStructList )
#        result = secStructList.getConsensus(CONSENSUS_SEC_STRUCT_FRACTION) # will set it if not present yet.
        result = secStructList.getConsensus(useLargest=True) # will set it if not present yet.
#    nTdebug('secStruct res: %s %s %s', res, secStructList, secStruct)
    return result
# end def

def getDsspSecStructConsensusId( res ):
    return mapDssp2Int[getDsspSecStructConsensus(res)]
# end def


def getDsspPercentList( res ):
    """ 
    Returns None for error, or a three item list with the percentage for each of the types.
    For residues without dssp properties set it will return a three item list with all None's.
    """
    bogusResult = [ None, None, None ]
    secStructList = res.getDeepByKeys(DSSP_STR,SECSTRUCT_STR)
    if not secStructList:
#        nTdebug('Failed to get dssp secStructList for %s' % res)
        return bogusResult
    # end if
    result = [ 0., 0., 0. ] # Use floats for division later on.
    secStructList = to3StateDssp( secStructList )
    n = 0
    for secStruct in secStructList:
        secStructIdx = mapDssp2Int[secStruct]
        if secStructIdx == None:
            nTwarning('Found no map for secStruct: "%s" excluded' % secStruct)
            continue
        # end if
        result[secStructIdx] += 1
        n += 1
    # end for
    if n < 1:
        nTwarning('Failed to find any valid secStruct for %s. Returning empties.' % res)
        return bogusResult
    # end for
    # Use Python list comprehension grammar.
    result = [ 100.*result[i]/n for i in range(len(result)) ]
#    nTdebug('Returning in getDsspPercentList for %s with list: %s' % (res, str(result)))
    return result
# end def

