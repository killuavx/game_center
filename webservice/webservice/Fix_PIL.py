# -*- encoding=utf-8 -*-
# Pillow < 2.0.0 supports Python versions 2.4, 2.5, 2.6, 2.7; Pillow >= 2.0.0
# supports Python versions 2.6, 2.7, 3.2, 3.3.
# 
# Note
# 
# Pillow >= 2.1.0 no longer supports "import _imaging". Please use "from
# PIL.Image import core as _imaging" instead.
# Pillow>=2.0.0 no is<type>Type function
#
# type stuff
#

def isStringType(t):
    return isinstance(t, str)

##
# (Internal) Checks if an object is a tuple.

def isTupleType(t):
    return isinstance(t, tuple)

##
# (Internal) Checks if an object is an image object.

def isImageType(t):
    return hasattr(t, "im")

# (Internal) Checks if an object is a string, and that it points to a
# directory.

def isDirectory(f):
    return isStringType(f) and os.path.isdir(f)


def isNumberType(x): 
    from numbers import Number as NumberType
    return isinstance(x, NumberType)

def isSequenceType(t):
    from collections import Sequence as SequenceType
    return isinstance(t, SequenceType)

import operator
operator.isNumberType = isNumberType
operator.isSequenceType = isSequenceType

