#-*- coding: utf-8 -*-
'''
Storing the abstract syntax tree types here.
The developer is to add the type here to add a
code generation function for any new AST.

PGMTYPE :
'pgm'

DECLTYPE :
'decl'

BVAL :
'bval'

NUMTYPE :
'num'

EXPTYPE :
'exp'

EVENTTYPE :
"evnt"

ATOMICTYPE :
'atmc'

ASGNTYPE :
'asgn'

CONDTYPE :
'cond'

ITE :
'ite'

INIT:
'init'

.. module::asttypes
   :synopsis: abstract syntax tree type list
.. moduleauthor:: Ritwika Ghosh <rghosh9@illinois.edu>
'''
LOCAL = 0
ALLWRITE = 1
ALLREAD = 2

PGMTYPE = 'pgm'
DECLTYPE = 'decl'
BVAL = 'bval'
NUMTYPE = 'num'
EXPTYPE = 'exp'
EVENTTYPE = "evnt"
ATOMICTYPE = 'atmc'
ASGNTYPE = 'asgn'
CONDTYPE = 'cond'
INITTYPE = 'init'
ITE = 'ite'
ARITHTYPE = 'arith'
RESTYPE = 'res'
VARTYPE = 'var'
NULLTYPE = 'null'
ARTYPE = 'ar'
AWTYPE = 'aw'