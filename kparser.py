# -*- coding: utf-8 -*-
""" The file *kparser.py* includes a parser for *Koord* programs
which enables us to generate Java code. We use the abstract syntax
tree module to construct the syntax tree from this parser.
The syntax of *Koord* is given as follows :

:pgm: **agnt defs modules declblock initblock events**

:agnt: AGENT CID NL

:defs: **def defs**
     | **empty**

:def: **enumdef**

:enumdef: DEF ENUM CID COLON NL INDENT **names** DEDENT

:names: **names** COMMA LID | LID

:modules: **module** **modules**
        | **empty**
:module: MODULE CID COLON NL INDENT **adecls sdecls** DEDENT
:adecls: ACTUATORS COLON NL INDENT **decls** DEDENT
       | **empty**
:sdecls: SENSORS COLON NL INDENT **decls** DEDENT
       | **empty**
:decls: **decl** **decls**
      | **empty**

:decl: **type** **varname** ASGN **exp** NL
     | **type varname** NL

:type: INT | FLOAT | POS | BOOLEAN

:varname: LID

:exp: **num** | **bval**

:num: INUM | FNUM

:bval: TRUE | FALSE

:declblock: **awdecls ardecls locdecls**

:awdecls: ALLWRITE COLON NL INDENT **decls** DEDENT | **empty**

:ardecls: ALLREAD COLON NL INDENT **decls** DEDENT | **empty**

:locdecls: LOCAL COLON NL INDENT **decls** DEDENT | **empty**

:initblock: INIT COLON NL INDENT **stmts** DEDENT | **empty**

:stmts: **stmt stmts** | **stmt**

:stmt: **asgn**

:asgn: **varname** ASGN **exp** NL


The parser uses the indentation lexer to tokenize the code,
and passes the parsed result as an abstract syntax
tree to the compiler, which in turn generates java code.

.. module::kparser
   :synopsis: Parser.
.. moduleauthor:: Ritwika Ghosh <rghosh9@illinois.edu>
"""

from ply import *
from asts import *
from scanner import *
from indentlexer import *
global wnum
wnum = 0

def p_pgm(p):
    '''pgm : agnt defs modules declblock initblock events'''
    p[0] = PgmAst(p[1], p[5], p[6], p[3][0] + p[4])


def p_agnt(p):
    '''agnt : AGENT CID NL'''
    p[0] = p[2]


def p_defs(p):
    '''defs : def defs
            | empty
    '''
    p[0] = []


def p_def(p):
    '''def : enumdef
    '''
    p[0] = []


def p_enumdef(p):
    '''enumdef : DEF ENUM CID COLON NL INDENT names NL DEDENT
    '''
    p[0] = []


def p_names(p):
    '''
    names : names COMMA LID
          | LID
    '''
    p[0] = []


def p_modules(p):
    '''modules : module modules
               | empty
    '''
    # module modules
    if len(p) > 2:
        # [modulenames],[associated declarations]
        p[0] = ([p[1][0]] + p[2][0], [p[1][1]] + p[2][1])
    # empty
    else:
        p[0] = ([], [])


def p_module(p):
    '''module : MODULE CID COLON NL INDENT adecls sdecls DEDENT'''
    # (modulename,list of actuator decls, list of sensordecls)
    p[0] = (p[2], p[6], p[7])


def p_adecls(p):
    '''adecls : ACTUATORS COLON NL INDENT decls DEDENT
                     | empty
    '''
    if len(p) > 2:
        p[0] = p[5]
    else:
        p[0] = []


def p_sdecls(p):
    '''sdecls : SENSORS COLON NL INDENT decls DEDENT
              | empty
    '''
    if len(p) > 2:
        p[0] = p[5]
    else:
        p[0] = []


def p_decls(p):
    '''decls : decl decls
             | empty
    '''
    # decl decls
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    # decl
    else:
        p[0] = []


def p_decl(p):
    '''decl : type varname ASGN exp NL
            |  type varname NL
    '''
    if len(p) == 4:
        p[0] = []
    else:
        p[0] = []


def p_type(p):
    '''type : INT
            | FLOAT
            | POS
            | BOOLEAN
    '''
    p[0] = []


def p_pid(p):
    '''pid : PID
    '''
    p[0] = ExprAst(RESTYPE, p[1])


def p_numbots(p):
    '''numbots : NUMBOTS
    '''
    p[0] = ExprAst(RESTYPE, p[1])


def p_varname(p):
    '''varname : LID
    '''
    p[0] = ExprAst(VARTYPE, p[1])


precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'BY'),
)


def p_exp(p):
    '''exp : bracketexp
           | exp PLUS exp
           | exp TIMES exp
           | exp MINUS exp
           | exp BY exp
           | varname
           | num
           | bval
           | pid
           | numbots
    '''
    if len(p) == 2:
        p[0] = p[1]
    elif len(p) == 4:
        p[0] = ExprAst(ARITHTYPE, p[1], p[2], p[3])


def p_bracketexp(p):
    '''bracketexp : LPAR exp RPAR '''
    p[0] = p[2]


def p_num(p):
    '''
    num : INUM
        | FNUM
    '''
    p[0] = ExprAst(NUMTYPE, p[1])


def p_bval(p):
    '''
    bval : TRUE
         | FALSE
    '''
    p[0] = ExprAst(BVAL, p[1])


def p_declblock(p):
    '''
    declblock : awdecls ardecls locdecls
    '''
    p[0] = p[1] + p[2]


def p_awdecls(p):
    '''
    awdecls : ALLWRITE COLON NL INDENT decls DEDENT
            | empty
    '''
    if len(p) is 2:
        p[0] = []
    else:
        p[0] = ['allwrite']


def p_ardecls(p):
    '''
    ardecls : ALLREAD COLON NL INDENT decls DEDENT
            | empty
    '''
    if len(p) is 2:
        p[0] = []
    else:
        p[0] = ['allread']


def p_locdecls(p):
    '''
    locdecls : LOCAL COLON NL INDENT decls DEDENT
            | empty
    '''
    p[0] = []


def p_initblock(p):
    '''initblock : INIT COLON NL INDENT stmts DEDENT
            | empty
    '''
    if len(p) > 2:
        p[0] = InitAst(p[5])
    else:
        p[0] = p[1]


def p_stmts(p):
    '''
    stmts : stmt stmts
          | stmt
    '''
    if len(p) > 2:
        p[0] = [p[1]] + p[2]
    else:
        p[0] = [p[1]]


def p_stmt(p):
    '''
    stmt : asgn
         | atomic
    '''
    p[0] = p[1]


def p_asgn(p):
    '''asgn : varname ASGN exp NL
    '''
    p[0] = (AsgnAst(p[1], p[3]))


def p_atomic(p):
    '''atomic : ATOMIC COLON NL INDENT stmts DEDENT
    '''
    global wnum
    p[0] = AtomicAst(wnum,p[5])
    wnum += 1


def p_events(p):
    '''events : event events
              | event '''
    dlist = [p[1]]
    if len(p) > 2:
        dlist += p[2]
    p[0] = dlist


def p_event(p):
    '''event : LID COLON NL INDENT PRE COLON cond NL effblock DEDENT
    '''
    p[0] = EventAst(p[1], p[7], p[9])


def p_effblock(p):
    '''effblock : EFF COLON NL INDENT stmts DEDENT
                | EFF COLON stmt
    '''
    if len(p) > 4:
        p[0] = p[5]
    else:
        p[0] = p[3]


def p_cond(p):
    '''cond :  LPAR cond AND cond RPAR
            | LPAR cond OR cond RPAR
            | LPAR cond op cond RPAR
            | LPAR NOT cond RPAR
            | LPAR cond RPAR
            | exp
    '''
    if len(p) == 6:
        p[0] = CondAst(p[2], p[3], p[4])
    elif len(p) == 5:
        p[0] = CondAst(p[3], p[2], None)
    elif len(p) == 4:
        p[0] = p[2]
    else:
        p[0] = CondAst(p[1])


def p_op(p):
    '''op : EQ
          | NEQ
          | GEQ
          | LEQ
          | GT
          | LT
    '''
    p[0] = p[1]


def p_empty(p):
    '''empty :'''
    pass


def p_error(p):
    '''to find line with error
    '''
    print("syntax error in input on line ", p.lineno, p.type)


class myparser(object):
    '''We create a parser class which can take in a different lexical analyzer as well
    '''

    def __init__(self, lexer=None):
        '''
        The basic parser class

        Args:
            lexer (lexer) : the lexer to tokenize the code.

        '''
        self.lexer = IndentLexer()
        self.parser = yacc.yacc()

    def parse(self, code):
        '''
        The function to take code as input, tokenize it using the lexer,
        and parse it.

        Args:
            code (str) : code to be parsed.

        Returns:
            result (PgmAst) : return the abstract syntax tree of the program

        '''
        self.lexer.input(code)
        result = self.parser.parse(lexer=self.lexer)
        return result
