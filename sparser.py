# -*- coding: utf-8 -*-
""" The file *sparser.py* includes a parser for *Koord* programs
which enables us to construct a symbol table. We use the *declAst*
class to store declarations. This parser is a first pass to create
the symbol table and generate declarations.

.. module::sparser
   :synopsis: symbol table Parser.
.. moduleauthor:: Ritwika Ghosh <rghosh9@illinois.edu>
"""

from ply import *
from asts import *
from scanner import *
from indentlexer import *


def p_pgm(p):
    '''pgm : agnt defs modules declblock initblock events'''
    p[0] = p[4]


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
        p[0] = p[1] + p[2]
    # empty
    else:
        p[0] = []


def p_module(p):
    '''module : MODULE CID COLON NL INDENT adecls sdecls DEDENT'''
    # (modulename,list of actuator decls, list of sensordecls)
    p[0] = []


def p_adecls(p):
    '''adecls : ACTUATORS COLON NL INDENT decls DEDENT
                     | empty
    '''
    p[0] = []


def p_sdecls(p):
    '''sdecls : SENSORS COLON NL INDENT decls DEDENT
              | empty
    '''
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
        p[0] = DeclAst(p[1], p[2])
    else:
        p[0] = DeclAst(p[1], p[2], p[4])


def p_type(p):
    '''type : INT
            | FLOAT
            | POS
            | BOOLEAN
    '''
    p[0] = p[1]


def p_pid(p):
    '''pid : PID
    '''
    p[0] = ExprAst(RESTYPE, p[1])


def p_varname(p):
    '''varname : LID
    '''
    p[0] = ExprAst(VARTYPE, p[1])


def p_numbots(p):
    '''numbots : NUMBOTS
    '''
    p[0] = ExprAst(RESTYPE, p[1])


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
    p[0] = p[1] + p[2] + p[3]


def p_awdecls(p):
    '''
    awdecls : ALLWRITE COLON NL INDENT decls DEDENT
            | empty
    '''
    if len(p) > 2:
        for decl in p[5]:
            decl.set_scope(ALLWRITE)
        p[0] = p[5]
    else:
        p[0] = []


def p_ardecls(p):
    '''
    ardecls : ALLREAD COLON NL INDENT decls DEDENT
            | empty
    '''
    if len(p) > 2:
        for decl in p[5]:
            decl.set_scope(ALLREAD)
        p[0] = p[5]
    else:
        p[0] = []


def p_locdecls(p):
    '''
    locdecls : LOCAL COLON NL INDENT decls DEDENT
            | empty
    '''
    if len(p) > 2:
        p[0] = p[5]
    else:
        p[0] = []


def p_initblock(p):
    '''initblock : INIT COLON NL INDENT stmts DEDENT
            | empty
    '''
    p[0] = []


def p_stmts(p):
    '''
    stmts : stmt stmts
          | stmt
    '''
    p[0] = []


def p_stmt(p):
    '''
    stmt : asgn
    '''
    p[0] = []


def p_asgn(p):
    '''asgn : varname ASGN exp NL
    '''
    p[0] = []


def p_events(p):
    '''events : event events
              | event '''
    p[0] = []


def p_event(p):
    '''event : LID COLON NL INDENT PRE COLON cond NL effblock DEDENT
    '''
    p[0] = []


def p_effblock(p):
    '''effblock : EFF COLON NL INDENT stmts DEDENT
                | EFF COLON stmt
    '''
    p[0] = []


def p_cond(p):
    '''cond :  LPAR cond AND cond RPAR
            | LPAR cond OR cond RPAR
            | LPAR cond op cond RPAR
            | LPAR NOT cond RPAR
            | exp
    '''
    p[0] = []


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


class symparser(object):
    '''We create a parser class which can take in a different lexical analyzer as well
    '''

    def __init__(self, lexer=None):
        '''
        The symbol table parser class

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
            result (list) : return the symbol table as a list

        '''
        self.lexer.input(code)
        result = self.parser.parse(lexer=self.lexer)
        return result
