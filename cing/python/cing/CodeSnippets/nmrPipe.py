__author__ = 'geerten'


NIHheaderDefinitionString = """
/***/
/* fdatap.h: defines the NMRPipe data header array FDATA, and
/*           outlines some data format details.
/***/

/***/
/* The NMRPipe parameter array FDATA currently consists of 512 4-byte
/* floating-point values which describe the spectral data.  While all numerical
/* values in this array are floating point, many represent parameters
/* (such as size in points) which are integers.  Some parts of the
/* header contain packed ascii text.
/*
/* There are currently three variations of spectral data in the NMRPipe
/* format:
/*
/*   1. Single-File (1D and 2D): the data are stored in a single
/*      binary file consiting of the header followed by the
/*      spectral intensities, stored in sequential order as
/*      4-byte floats.
/*
/*   2. Multi-File (3D and 4D): the data are stored as a series
/*      of 2D file planes, each with its own complete header
/*      followed by the spectral intensities in sequential order.
/*
/*   3. Data Stream (1D-4D): the data are in the form of a pipeline
/*      stream, with a single header at the beginning followed by
/*      all of the spectral intensities in sequential order.
/*
/* The header values can be manipulated directly, but this is not
/* recommended.  Instead, the functions getParm() and setParm() can
/* be used to extract or set header values according to parameter
/* codes and the dimension of interest (if any).  See the source
/* code distribution for examples of these functions.
/*
/* The NMRPipe format was created to be compatible with an older format
/* which pre-dates phase-sensitive NMR and multidimensional NMR.
/* So, for historical reasons, there are some potentially confusing
/* aspects regarding definition of dimension sizes, data types,
/* and interleaving of real and imaginary data.
/*
/* In the NMRPipe nomenclature, the dimensions are called the X-Axis,
/* Y-Axis, Z-Axis, and A-Axis.  Some rules of thumb about the data format
/* follow:
/*
/*  1. Complex data in the X-Axis is stored as separated 1D vectors
/*     of real and imaginary points (see below).
/*
/*  2. Complex data in the Y-Axis, Z-Axis, and A-Axis is stored as
/*     interleaved real and imaginary points.
/*
/*  3. The X-Axis size is recorded as complex points.
/*
/*  4. The Z-Axis and A-Axis sizes are recorded as total points real+imag.
/*
/*  5. If both the X-Axis and Y-Axis are complex, the Y-Axis size
/*     is reported as total points real+imag.
/*
/*  6. If the X-Axis is not complex but the Y-Axis is complex,
/*     the Y-axis size is reported as complex points.
/*
/*  7. TPPI data, and Bruker QSEQ mode data are treated as real data.
/***/

/***/
/* 1D Real Format:
/*  (512-point FDATA)
/*  (N real points...)
/*
/* 1D Complex Format:
/*  (512-point FDATA)
/*  (N real points...)
/*  (N imag points...)
/*
/* 2D Hypercomplex Format;
/* (direct dimension = t2, indirect dimension = t1):
/*
/*  (512-point FDATA)
/*  (N t2=real points... for t1=1 Real)
/*  (N t2=imag points... for t1=1 Real)
/*  (N t2=real points... for t1=1 Imag)
/*  (N t2=imag points... for t1=1 Imag)
/*  (N t2=real points... for t1=2 Real)
/*  (N t2=imag points... for t1=2 Real)
/*  (N t2=real points... for t1=2 Imag)
/*  (N t2=imag points... for t1=2 Imag)
/*  ... etc ...
/*  (N t2=real points... for t1=M Real)
/*  (N t2=imag points... for t1=M Real)
/*  (N t2=real points... for t1=M Imag)
/*  (N t2=imag points... for t1=M Imag)
/*
/* 3D Hypercomplex format: consists of a series of 2D hypercomplex
/* planes above, which are alternating real and imaginary in the third
/* dimension.
/*
/* 4D Hypercomplex format: consists of a series of 3D hypercomplex
/* spectra above, which are alternating real and imaginary in the
/* fourth dimension.
/***/

/***/
/* Some useful constant definitions:
/***/

#define FDATASIZE          512   /* Length of header in 4-byte float values. */

##define FDIEEECONS   0xeeeeeeee  /* Indicates IEEE floating point format.    */
##define FDVAXCONS    0x11111111  /* Indicates DEC VAX floating point format. */
##define FDORDERCONS       2.345  /* Constant used to determine byte-order.   */
##define FDFMTCONS    FDIEEECONS  /* Floating point format on this computer.  */
##define ZERO_EQUIV       -666.0  /* Might be used as equivalent for zero.    */

/***/
/* General Parameter locations:
/***/

#define FDMAGIC        0 /* Should be zero in valid NMRPipe data.            */
#define FDFLTFORMAT    1 /* Constant defining floating point format.         */
#define FDFLTORDER     2 /* Constant defining byte order.                    */

#define FDSIZE        99 /* Number of points in current dim R|I.             */
#define FDREALSIZE    97 /* Number of valid time-domain pts (obsolete).      */
#define FDSPECNUM    219 /* Number of complex 1D slices in file.             */
#define FDQUADFLAG   106 /* See Data Type codes below.                       */
#define FD2DPHASE    256 /* See 2D Plane Type codes below.                   */

/***/
/* Parameters defining number of dimensions and their order in the data;
/* a newly-converted FID has dimension order (2 1 3 4). These dimension
/* codes are a hold-over from the oldest 2D NMR definitions, where the
/* directly-acquired dimension was always t2, and the indirect dimension
/* was t1.
/***/

#define FDTRANSPOSED 221 /* 1=Transposed, 0=Not Transposed.                  */
#define FDDIMCOUNT     9 /* Number of dimensions in complete data.           */
#define FDDIMORDER    24 /* Array describing dimension order.                */

#define FDDIMORDER1   24 /* Dimension stored in X-Axis.                      */
#define FDDIMORDER2   25 /* Dimension stored in Y-Axis.                      */
#define FDDIMORDER3   26 /* Dimension stored in Z-Axis.                      */
#define FDDIMORDER4   27 /* Dimension stored in A-Axis.                      */

/***/
/* The following parameters describe the data when it is
/* in a multidimensional data stream format (FDPIPEFLAG != 0):
/***/

#define FDPIPEFLAG    57 /* Dimension code of data stream.    Non-standard.  */
#define FDPIPECOUNT   75 /* Number of functions in pipeline.  Non-standard.  */
#define FDSLICECOUNT 443 /* Number of 1D slices in stream.    Non-standard.  */
#define FDFILECOUNT  442 /* Number of files in complete data.                */

/***/
/* The following definitions are used for data streams which are
/* subsets of the complete data, as for parallel processing:
/***/

#define FDFIRSTPLANE  77 /* First Z-Plane in subset.            Non-standard. */
#define FDLASTPLANE   78 /* Last Z-Plane in subset.             Non-standard. */
#define FDPARTITION   65 /* Slice count for client-server mode. Non-standard. */

#define FDPLANELOC    14 /* Location of this plane; currently unused.         */

/***/
/* The following define max and min data values, previously used
/* for contour level setting:
/***/

#define FDMAX        247 /* Max value in real part of data.                  */
#define FDMIN        248 /* Min value in real part of data.                  */
#define FDSCALEFLAG  250 /* 1 if FDMAX and FDMIN are valid.                  */
#define FDDISPMAX    251 /* Max value, used for display generation.          */
#define FDDISPMIN    252 /* Min value, used for display generation.          */

/***/
/* Locations reserved for User customization:
/***/

#define FDUSER1       70
#define FDUSER2       71
#define FDUSER3       72
#define FDUSER4       73
#define FDUSER5       74

/***/
/* Defines location of "footer" information appended to spectral
/* data; currently unused for NMRPipe format:
/***/

#define FDLASTBLOCK  359
#define FDCONTBLOCK  360
#define FDBASEBLOCK  361
#define FDPEAKBLOCK  362
#define FDBMAPBLOCK  363
#define FDHISTBLOCK  364
#define FD1DBLOCK    365

/***/
/* Defines data and time data was converted:
/***/

#define FDMONTH      294
#define FDDAY        295
#define FDYEAR       296
#define FDHOURS      283
#define FDMINS       284
#define FDSECS       285

/***/
/* Miscellaneous Parameters:
/***/

#define FDMCFLAG      135 /* Magnitude Calculation performed.               */
#define FDNOISE       153 /* Used to contain an RMS noise estimate.         */
#define FDRANK        180 /* Estimate of matrix rank; Non-standard.         */
#define FDTEMPERATURE 157 /* Temperature, degrees C.                        */
#define FD2DVIRGIN    399 /* 0=Data never accessed, header never adjusted.  */
#define FDTAU         199 /* A Tau value (for spectral series).             */

#define FDSRCNAME    286  /* char srcFile[16]  286-289 */
#define FDUSERNAME   290  /* char uName[16]    290-293 */
#define FDOPERNAME   464  /* char oName[32]    464-471 */
#define FDTITLE      297  /* char title[60]    297-311 */
#define FDCOMMENT    312  /* char comment[160] 312-351 */

/***/
/* For meanings of these dimension-specific parameters,
/* see the corresponding ND parameters below.
/***/

#define FDF2LABEL     16
#define FDF2APOD      95
#define FDF2SW       100
#define FDF2OBS      119
#define FDF2ORIG     101
#define FDF2UNITS    152
#define FDF2QUADFLAG  56 /* Non-standard. */
#define FDF2FTFLAG   220
#define FDF2AQSIGN    64 /* Non-standard. */
#define FDF2LB       111
#define FDF2CAR       66 /* Non-standard. */
#define FDF2CENTER    79 /* Non-standard. */
#define FDF2OFFPPM   480 /* Non-standard. */
#define FDF2P0       109
#define FDF2P1       110
#define FDF2APODCODE 413
#define FDF2APODQ1   415
#define FDF2APODQ2   416
#define FDF2APODQ3   417
#define FDF2C1       418
#define FDF2ZF       108
#define FDF2X1       257 /* Non-standard. */
#define FDF2XN       258 /* Non-standard. */
#define FDF2FTSIZE    96 /* Non-standard. */
#define FDF2TDSIZE   386 /* Non-standard. */

#define FDF1LABEL     18
#define FDF1APOD     428
#define FDF1SW       229
#define FDF1OBS      218
#define FDF1ORIG     249
#define FDF1UNITS    234
#define FDF1FTFLAG   222
#define FDF1AQSIGN   475 /* Non-standard. */
#define FDF1LB       243
#define FDF1QUADFLAG  55 /* Non-standard. */
#define FDF1CAR       67 /* Non-standard. */
#define FDF1CENTER    80 /* Non-standard. */
#define FDF1OFFPPM   481 /* Non-standard. */
#define FDF1P0       245
#define FDF1P1       246
#define FDF1APODCODE 414
#define FDF1APODQ1   420
#define FDF1APODQ2   421
#define FDF1APODQ3   422
#define FDF1C1       423
#define FDF1ZF       437
#define FDF1X1       259 /* Non-standard. */
#define FDF1XN       260 /* Non-standard. */
#define FDF1FTSIZE    98 /* Non-standard. */
#define FDF1TDSIZE   387 /* Non-standard. */

#define FDF3LABEL     20
#define FDF3APOD      50 /* Non-standard. */
#define FDF3OBS       10
#define FDF3SW        11
#define FDF3ORIG      12
#define FDF3FTFLAG    13
#define FDF3AQSIGN   476 /* Non-standard. */
#define FDF3SIZE      15
#define FDF3QUADFLAG  51 /* Non-standard. */
#define FDF3UNITS     58 /* Non-standard. */
#define FDF3P0        60 /* Non-standard. */
#define FDF3P1        61 /* Non-standard. */
#define FDF3CAR       68 /* Non-standard. */
#define FDF3CENTER    81 /* Non-standard. */
#define FDF3OFFPPM   482 /* Non-standard. */
#define FDF3APODCODE 400 /* Non-standard. */
#define FDF3APODQ1   401 /* Non-standard. */
#define FDF3APODQ2   402 /* Non-standard. */
#define FDF3APODQ3   403 /* Non-standard. */
#define FDF3C1       404 /* Non-standard. */
#define FDF3ZF       438 /* Non-standard. */
#define FDF3X1       261 /* Non-standard. */
#define FDF3XN       262 /* Non-standard. */
#define FDF3FTSIZE   200 /* Non-standard. */
#define FDF3TDSIZE   388 /* Non-standard. */

#define FDF4LABEL     22
#define FDF4APOD      53 /* Non-standard. */
#define FDF4OBS       28
#define FDF4SW        29
#define FDF4ORIG      30
#define FDF4FTFLAG    31
#define FDF4AQSIGN   477 /* Non-standard. */
#define FDF4SIZE      32
#define FDF4QUADFLAG  54 /* Non-standard. */
#define FDF4UNITS     59 /* Non-standard. */
#define FDF4P0        62 /* Non-standard. */
#define FDF4P1        63 /* Non-standard. */
#define FDF4CAR       69 /* Non-standard. */
#define FDF4CENTER    82 /* Non-standard. */
#define FDF4OFFPPM   483 /* Non-standard. */
#define FDF4APODCODE 405 /* Non-standard. */
#define FDF4APODQ1   406 /* Non-standard. */
#define FDF4APODQ2   407 /* Non-standard. */
#define FDF4APODQ3   408 /* Non-standard. */
#define FDF4C1       409 /* Non-standard. */
#define FDF4ZF       439 /* Non-standard. */
#define FDF4X1       263 /* Non-standard. */
#define FDF4XN       264 /* Non-standard. */
#define FDF4FTSIZE   201 /* Non-standard. */
#define FDF4TDSIZE   389 /* Non-standard. */

/***/
/* Header locations in use for packed text:
/***/

/* 286 287 288 289                                                     */
/* 290 291 292 293                                                     */
/* 464 465 466 467  468 469 470 471                                    */
/* 297 298 299 300  301 302 303 304  305 306 307 308  309 310 311      */
/* 312 313 314 315  316 317 318 319  320 321 322 323  324 325 326 327  */
/* 328 329 330 331  332 333 334 335  336 337 338 339  340 341 342 343  */
/* 344 345 346 347  348 349 350 351                                    */

#define SIZE_NDLABEL    8
#define SIZE_F2LABEL    8
#define SIZE_F1LABEL    8
#define SIZE_F3LABEL    8
#define SIZE_F4LABEL    8

#define SIZE_SRCNAME   16
#define SIZE_USERNAME  16
#define SIZE_OPERNAME  32
#define SIZE_COMMENT  160
#define SIZE_TITLE     60

/***/
/* The following are definitions for generalized ND parameters:
/***/

##define NDPARM      1000

##define BAD_DIM     -666
##define NULL_DIM       0
##define CUR_XDIM       1
##define CUR_YDIM       2
##define CUR_ZDIM       3
##define CUR_ADIM       4

##define ABS_XDIM      -1
##define ABS_YDIM      -2
##define ABS_ZDIM      -3
##define ABS_ADIM      -4

##define CUR_HDIM       9
##define CUR_VDIM      10

##define NDSIZE        (1+NDPARM)  /* Number of points in dimension.          */
##define NDAPOD        (2+NDPARM)  /* Current valid time-domain size.         */
##define NDSW          (3+NDPARM)  /* Sweep Width Hz.                         */
##define NDORIG        (4+NDPARM)  /* Axis Origin (Last Point), Hz.           */
##define NDOBS         (5+NDPARM)  /* Obs Freq MHz.                           */
##define NDFTFLAG      (6+NDPARM)  /* 1=Freq Domain 0=Time Domain.            */
##define NDQUADFLAG    (7+NDPARM)  /* Data Type Code (See Below).             */
##define NDUNITS       (8+NDPARM)  /* Axis Units Code (See Below).            */
##define NDLABEL       (9+NDPARM)  /* 8-char Axis Label.                      */
##define NDLABEL1      (9+NDPARM)  /* Subset of 8-char Axis Label.            */
##define NDLABEL2     (10+NDPARM)  /* Subset of 8-char Axis Label.            */
##define NDP0         (11+NDPARM)  /* Zero Order Phase, Degrees.              */
##define NDP1         (12+NDPARM)  /* First Order Phase, Degrees.             */
##define NDCAR        (13+NDPARM)  /* Carrier Position, PPM.                  */
##define NDCENTER     (14+NDPARM)  /* Point Location of Zero Freq.            */
##define NDAQSIGN     (15+NDPARM)  /* Sign adjustment needed for FT.          */
##define NDAPODCODE   (16+NDPARM)  /* Window function used.                   */
##define NDAPODQ1     (17+NDPARM)  /* Window parameter 1.                     */
##define NDAPODQ2     (18+NDPARM)  /* Window parameter 2.                     */
##define NDAPODQ3     (19+NDPARM)  /* Window parameter 3.                     */
##define NDC1         (20+NDPARM)  /* Add 1.0 to get First Point Scale.       */
##define NDZF         (21+NDPARM)  /* Negative of Zero Fill Size.             */
##define NDX1         (22+NDPARM)  /* Extract region origin, if any, pts.     */
##define NDXN         (23+NDPARM)  /* Extract region endpoint, if any, pts.   */
##define NDOFFPPM     (24+NDPARM)  /* Additional PPM offset (for alignment).  */
##define NDFTSIZE     (25+NDPARM)  /* Size of data when FT performed.         */
##define NDTDSIZE     (26+NDPARM)  /* Original valid time-domain size.        */
##define MAX_NDPARM   (27)

/***/
/* Axis Units, for NDUNITS:
/***/

#define FD_SEC       1
#define FD_HZ        2
#define FD_PPM       3
#define FD_PTS       4

/***/
/* 2D Plane Type, for FD2DPHASE:
/***/

#define FD_MAGNITUDE 0
#define FD_TPPI      1
#define FD_STATES    2
#define FD_IMAGE     3

/***/
/* Data Type (FDQUADFLAG and NDQUADFLAG)
/***/

#define FD_QUAD       0
#define FD_COMPLEX    0
#define FD_SINGLATURE 1
#define FD_REAL       1
#define FD_PSEUDOQUAD 2

/***/
/* Sign adjustment needed for FT (NDAQSIGN):
/***/

#define ALT_NONE            0 /* No sign alternation required.                */
#define ALT_SEQUENTIAL      1 /* Sequential data needing sign alternation.    */
#define ALT_STATES          2 /* Complex data needing sign alternation.       */
#define ALT_NONE_NEG       16 /* As above, with negation of imaginaries.      */
#define ALT_SEQUENTIAL_NEG 17 /* As above, with negation of imaginaries.      */
#define ALT_STATES_NEG     18 /* As above, with negation of imaginaries.      */

#define FOLD_INVERT        -1 /* Folding requires sign inversion.             */
#define FOLD_BAD            0 /* Folding can't be performed (extracted data). */
#define FOLD_ORDINARY       1 /* Ordinary folding, no sign inversion.         */
"""


# Parse and create NIH header definitions
NIHheaderDefs = NTdict()
for l in AwkLikeS( NIHheaderDefinitionString, minNF = 3 ):
    if l.dollar[1] == '#define':
        #print '>>', l.dollar[0]
        if l.NF > 5:
            comment = ' '.join(l.dollar[5:l.NF])
        else: comment = None
        NIHheaderDefs[l.dollar[2]] = int(l.dollar[3])   # store value
#        NIHheaderDefs['_'+l.dollar[2]] = (l.dollar[2],int(l.dollar[3]), comment) #store definition as _NAME
    #end if
#end for
NIHheaderDefs.keysformat() #define a format string for 'pretty' output

class NMRPipeFile( NTfile ):
    """
    Class to Read (Write?) NMRPipe file
    Reads header on opening
    """

    def __init__( self, path, dimcount=2):
        NTfile.__init__( self, path )
        self.header = parseNMRPipeHeader( self.readHeader() )
    #end def

    def readHeader( self ):
        self.rewind()
        return self.binaryRead( typecode='f', size=NIHheaderDefs.FDATASIZE )
    #end def
#end class

def parseNMRPipeHeader( data ):
    """parse an NMRPipe header
       Return an NTdict structure or None on error
    """

    # convert the data also to char format
    charData = array.array('b')
    charData.fromstring( array.array('f',data).tostring())

    # Parse and interpret the header data
    header = NTdict()

    #dimensions and dimension order; bloody pipe format
    for name in ['DIMCOUNT','SIZE','SPECNUM','TRANSPOSED']:
        n = NIHheaderDefs['FD'+name]
        header[name.lower()] = int( data[n] )
    #end for

    n1 = NIHheaderDefs.FDDIMORDER
    n2 = n1+header.dimcount
    header.dimorder = map(int, data[n1:n2])

    # dimension parameters
    for d in range(1,5):

        dim = NTdict()
        header['axis_'+str(d)] = dim
        dim.axisIndex = d

        root = 'FDF'+str(d)

        # Char's
        #define FDF4LABEL     22
        #define SIZE_F4LABEL    8
        n1 = NIHheaderDefs[root+'LABEL']*4  # 4 Bytes per float
        n2 = n1 + NIHheaderDefs['SIZE_F'+str(d)+'LABEL'] # given in Bytes
        dim.label = charData[n1:n2].tostring()

        # Int's
        #define FDF4APOD      53 /* Non-standard. */
        #define FDF4FTFLAG    31
        #define FDF4AQSIGN   477 /* Non-standard. */
        #define FDF4SIZE      32
        #define FDF4CENTER    82 /* Non-standard. */
        #define FDF4QUADFLAG  54 /* Non-standard. */
        #define FDF4UNITS     59 /* Non-standard. */
        #define FDF4APODCODE 405 /* Non-standard. */
        #define FDF4ZF       439 /* Non-standard. */
        #define FDF4X1       263 /* Non-standard. */
        #define FDF4XN       264 /* Non-standard. */
        #define FDF4FTSIZE   201 /* Non-standard. */
        #define FDF4TDSIZE   389 /* Non-standard. */
        for name in ['APOD','FTFLAG','AQSIGN','CENTER','QUADFLAG','UNITS',
                     'APODCODE','ZF','X1','XN','FTSIZE','TDSIZE'
                    ]:
            n = NIHheaderDefs[root+name]
            dim[name.lower()] = int( data[n] )
        #end for

        # float's
        #define FDF4OBS       28
        #define FDF4SW        29
        #define FDF4ORIG      30
        #define FDF4P0        62 /* Non-standard. */
        #define FDF4P1        63 /* Non-standard. */
        #define FDF4CAR       69 /* Non-standard. */
        #define FDF4OFFPPM   483 /* Non-standard. */
        #define FDF4APODQ1   406 /* Non-standard. */
        #define FDF4APODQ2   407 /* Non-standard. */
        #define FDF4APODQ3   408 /* Non-standard. */
        #define FDF4C1       409 /* Non-standard. */
        for name in ['OBS','SW','ORIG','P0','P1','CAR','OFFPPM',
                     'APODQ1','APODQ2','APODQ3','C1'
                    ]:
            n = NIHheaderDefs[root+name]
            dim[name.lower()] = data[n]
        #end for

    #end for

    # Do the mapping of axis_1 _2 _3 _4 on X, Y, Z, A using dimorder
    for xyza,axis in zip( ['X','Y','Z','A'], header.dimorder ):
        header[xyza] = header['axis_'+str(axis)]
    #end for

    # Now get sizes right; just write out all posibilities
    # BLOODY !@#$ Pipe (see definitions above)
    if (header.X.quadflag == 0):
        header.X.size      = header.size
        header.X.totalsize = header.size*2
        header.X.dataType  = 'sComplex'   # size Real, size Imag points
    else:
        header.X.size      = header.size
        header.X.totalsize = header.size
        header.X.dataType  = 'Real'
    #end if

    if (header.Y.quadflag == 0):
        if (header.X.quadflag == 0):
            header.Y.size      = header.specnum/2
            header.Y.totalsize = header.specnum
            header.Y.dataType  = 'Complex'   # Interleaved Real,Imag
        else:
            header.Y.size      = header.specnum
            header.Y.totalsize = header.specnum*2
            header.Y.dataType  = 'Complex'   # Interleaved Real,Imag
        #end if
    else:
        header.Y.size      = header.specnum
        header.Y.totalsize = header.specnum
        header.Y.dataType  = 'Real'
    #end if

    for i in ['3','4']:
        dim = header['axis_'+i]
        dim.totalsize = int( data[NIHheaderDefs['FDF'+i+'SIZE']] )
        if (dim.quadflag == 0):
            dim.size = dim.totalsize/2
            dim.dataType = 'Complex'    # Interleaved Real,Imag
        else:
            dim.size = dim.totalsize
            dim.dataType = 'Real'
        #endif
    #end for


    # Processing
    #define FDPIPEFLAG    57 /* Dimension code of data stream.    Non-standard.  */
    #define FDPIPECOUNT   75 /* Number of functions in pipeline.  Non-standard.  */
    #define FDSLICECOUNT 443 /* Number of 1D slices in stream.    Non-standard.  */
    #define FDFILECOUNT  442 /* Number of files in complete data.                */
    for name in ['PIPEFLAG','PIPECOUNT','SLICECOUNT','FILECOUNT']:
        n = NIHheaderDefs['FD'+name]
        header[name.lower()] = int( data[n] )
    #end for

    # others
    for name in ['MONTH','DAY','YEAR','HOURS','MINS','SECS',
                 'SCALEFLAG','MCFLAG'
                ]:
        n = NIHheaderDefs['FD'+name]
        header[name.lower()] = int( data[n] )
    #end for
    # others

    for name in ['NOISE','TEMPERATURE','TAU',
                 'USER1','USER2','USER3','USER4','USER5',
                 'MAX','MIN','DISPMAX', 'DISPMIN'
                ]:
        n = NIHheaderDefs['FD'+name]
        header[name.lower()] = data[n]
    #end for

    for name,i in [('SRCNAME',16),('USERNAME',16),('OPERNAME',32),
                   ('TITLE',60),('COMMENT',160)
                  ]:
        n = NIHheaderDefs['FD'+name]*4
        header[name.lower()] = charData[n:n+i].tostring()
    #end for


    # set the output formats
    for xyza in ['X','Y','Z','A'][0:header.dimcount]:
        header[xyza].keysformat()
    #end for
    header.keysformat()
    return header
#end def
