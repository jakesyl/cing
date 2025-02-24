"""The jsonpickle.tags module provides the custom tags
used for pickling and unpickling Python objects.

These tags are keys into the flattened dictionaries
created by the Pickler class.  The Unpickler uses
these custom key names to identify dictionaries
that need to be specially handled.
"""
from cing.Libs.jsonTools.compat import set


FUNCTION = 'py/function'
ID = 'py/id'
INITARGS = 'py/initargs'
ITERATOR = 'py/iterator'
JSON_KEY = 'json://'
NEWARGS = 'py/newargs'
NEWOBJ = 'py/newobj'
OBJECT = 'py/object'
REDUCE = 'py/reduce'
REF = 'py/ref'
REPR = 'py/repr'
SEQ = 'py/seq'
SET = 'py/set'
STATE = 'py/state'
TUPLE = 'py/tuple'
TYPE = 'py/type'
# GWV
# INFO = 'py/info'  # key used for info to be part of unpickler context
# VERSION = 'py/version'  # key used to store version information; added to unpickler context
# REVISION = 'py/revision'  # key used to store version information; added to unpickler context
ITEMS = 'py/items'  # key to store items of AnyDictHandler
VALUES = 'py/values'  # key to store values of AnyListHandler

# All reserved tag names
RESERVED = set([
    FUNCTION,
    ID,
    INITARGS,
    ITERATOR,
    NEWARGS,
    NEWOBJ,
    OBJECT,
    REDUCE,
    REF,
    REPR,
    SEQ,
    SET,
    STATE,
    TUPLE,
    TYPE,
    ITEMS,
    VALUES
])
