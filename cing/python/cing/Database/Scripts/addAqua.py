"""
Copy BMRB to Aqua with mods.
"""
from cing import NTdb
from cing.core.constants import * #@UnusedWildImport

nuclList = ('GUA', 'CYT', 'ADE', 'THY', 'URA',
            'RGUA', 'RCYT', 'RADE', 'RTHY', 'RURA',
            )
mapCing2Aqua = {
                  'GUA': 'G',
                  'CYT': 'C',
                  'ADE': 'A',
                  'THY': 'T',
                  'URA': 'U',

                  'RGUA': 'G',
                  'RCYT': 'C',
                  'RADE': 'A',
                  'RTHY': 'T',
                  'RURA': 'U',
                  }


for res in NTdb:
    res.nameDict[AQUA] = res.nameDict[IUPAC]

    if res.name in nuclList:
        res.nameDict[AQUA] = mapCing2Aqua[res.name]

    for atm in res:
        atm.nameDict[AQUA] = atm.nameDict[IUPAC]

stream = open('dbTable-new', 'w')
NTdb.exportDef(stream=stream)
stream.close()

