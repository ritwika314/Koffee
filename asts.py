#-*- coding: utf-8 -*-
"""
ASTs, or abstract syntax trees are standard objects to help
write parsers for a language specified as a BNF grammar.
We define several useful ASTs to write our parser in the file *asts.py*.

.. module::ast
   :synopsis: abstract syntax trees for the parser.
.. moduleauthor:: Ritwika Ghosh <rghosh9@illinois.edu>
"""
from asttypes import *

def is_ast(cand):
    """
    Determines whether an object is a defined AST

    Args:
        cand (object) : candidate AST

    Returns:
        result (bool) : whether candidate is an AST in our asttypes.

    """
    try:
        try_type = cand.get_type()
        return True
    except:
        return False

class ExprAst(list):
    """
    Basic expression AST, for arithmetic and boolean
    """
    def __init__(self, etype, lexp, op=None, rexp=None):
        '''
        '''
        self.etype = etype
        self.lexp = lexp
        self.op = op
        self.rexp = rexp

    def __repr__(self):
        '''
        '''
        if self.op is None:
            return str(self.lexp)
        if self.rexp is None:
            return str(self.lexp)+ str(self.op)
        if self.lexp is None:
            return str(self.op) + str(self.rexp)
        else:
            return "( " + str(self.lexp) + " " + str(self.op) + " " + str(self.rexp) + " )"

    def get_type(self):
        '''
        This function is used to get the AST type to generate
        the java code.
        '''
        return self.etype

    def get_lexp(self):
        '''
        getter method for left child of expression.

        '''
        return self.lexp

    def get_op(self):
        '''
        getter method for operation of expression.

        '''
        return self.op

    def get_rexp(self):
        '''
        getter method for right child of expression.

        '''
        return self.rexp

    def set_lexp(self, lexp):
        '''
        setter method for left child of expression.

        '''
        self.lexp = lexp

    def set_op(self, op):
        '''
        setter method for operation of expression.

        '''
        self.op = op

class InitAst(object):
    """
    Initialization AST.
    """

    def __init__(self,stmts):
        """

        :param stmts: Required initializations
        """
        self.stmts = stmts

    def get_type(self):
        """
        This function is used to get the AST type to generate
        the java code.
        """
        return INITTYPE

    def get_stmts(self):
        """

        :return: statements in the init block
        """
        return self.stmts

class DeclAst(list):
    """
    Basic declaration AST, will be used for the symtab parser
    """
    def __init__(self, dtype, varname, value=None, scope=LOCAL, enumlist=None, module=None):
        '''
        :type enumlist: List
        '''
        self.dtype = dtype
        self.varname = varname
        self.value = value
        self.scope = scope
        self.enumlist = enumlist
        self.module = module

    def __repr__(self):
        ret_str = "(" + str(self.scope) + ") " + str(self.dtype) + " " + str(self.varname)
        return ret_str

    def get_type(self):
        '''
        This function is used to get the AST type to generate
        the java code.
        '''
        return DECLTYPE

    def get_varname(self):
        '''
        Getter method for variable name of declaration.
        '''
        return self.varname

    def get_dtype(self):
        '''
        Getter method for type of declaration.
        '''
        return self.dtype

    def get_value(self):
        '''
        Getter method for value of declaration.
        '''
        return self.value

    def get_scope(self):
        '''
        Getter method for scope of declaration.
        '''
        return self.scope

    def get_enumlist(self):
        '''
        Getter method for enumlist if declaration is enum type.
        '''
        return self.enumlist

    def get_module(self):
        '''
        Getter method for module of declaration.
        '''
        return self.module

    def set_varname(self, varname):
        '''
        Setter method for variable name of declaration.
        '''
        self.varname = varname

    def set_dtype(self, dtype):
        '''
        Setter method for type of declaration.
        '''
        self.dtype = dtype

    def set_value(self, value):
        '''
        Setter method for value of declaration.
        '''
        self.value = value

    def set_scope(self, scope):
        '''
        Setter method for scope of declaration.
        '''
        self.scope = scope

    def set_enumlist(self, enumlist):
        '''
        Setter method for enumlist if declaration is enum type.
        '''
        self.enumlist = enumlist

    def set_module(self, module):
        '''
        Setter method for module of declaration.
        '''
        self.module = module = enumlist

class PgmAst(object):
    """
    This is the AST of a general *Koord* program

    """
    def __init__(self, name, init, events, flags=None):
        '''
        :type flags: List(strings)
        '''
        self.name = name
        self.init = init
        self.events = events
        if flags is not None:
            self.flags = flags+['javadef', 'default']
        else:
            self.flags = ['javadef', 'default']

    def get_init(self):
        '''

        :return: init statements
        '''
        return self.init

    def get_events(self):
        """

        :return: events of program
        """
        return self.events

    def get_name(self):
        '''
        Get method for name.
        '''
        return self.name

    def get_type(self):
        '''
        This function is used to get the AST type to generate
        the java code.
        '''
        return PGMTYPE

    def get_flags(self):
        '''
        Get method for the program flags for various code generation requirements.
        '''
        return self.flags


    def add_flag(self, flag):
        '''
        Method to add a flag to the existing set of flags
        '''
        self.flags.append(flag)

    def has_flag(self, flag):
        '''
        Method to check whether the set of flags contains a given flag
        '''
        return flag in self.flags

class StmtAst(list):
    """
    Generic AST for statements
    """
    def __init__(self, stype):
        """
        :type stype: object
        """
        self.stype = stype

    def get_type(self):
        """

        :return: the statement type
        """
        return self.stype

    def __repr__(self):
        return "lol"

class AtomicAst(StmtAst):
    """
    Ast for atomic blocks
    """
    def __init__(self, wn, stmts):
        """

        :param wnum: (int) for each atomic block, we need wait variable.
        :param stmts: (list<stmt>) the statements to be executed atomically
        """
        self.stype = ATOMICTYPE
        self.wn = wn
        self.stmts = stmts

    def get_wnum(self):
        '''

        :return: the ith atomic block returns i
        '''
        return self.wn

    def __repr__(self):
        ret_str = "atomic:"
        for stmt in self.stmts:
            ret_str += str(stmt)
        return ret_str

    def get_type(self):
        return ATOMICTYPE

class AsgnAst(StmtAst):
    """
    The AST for assignment statements
    """

    def __init__(self, lvar, rexp):
        """

        :param lvar: Variable being assigned to
        :param rexp: Assigning expression
        """
        self.stype = ASGNTYPE
        self.lvar = lvar
        self.rexp = rexp

    def __repr__(self):
        return str(self.lvar)+" = "+str(self.rexp)

    def get_lvar(self):
        """

        :return: assignee of this statement
        """
        return self.lvar

    def get_rexp(self):
        """

        :return: expression assigned of this statement
        """
        return self.rexp

class IteAst(StmtAst):
    """
    The AST for if-then-else statements
    """
    def __init__(self, cond, then_stmts, else_stmts):
        """

        :param cond: (condAst) if condition
        :param then_stmts: (list<Stmts>) executed if cond is *true*
        :param else_stmts: (list<Stmts>) executed if cond is *false*
        """
        self.stype = ITE
        self.cond = cond
        self.then_stmts = then_stmts
        self.else_stmts = else_stmts

    def __repr__(self):
        ret_str = "if "+str(self.cond)+"\n"
        for stmt in self.then_stmts:
            ret_str += str(stmt)
        if self.else_stmts is not None:
            ret_str += "else\n"
            for stmt in self.else_stmts:
                ret_str += str(stmt)
        return ret_str

class CondAst(list):
    """
    AST for conditions.
    """

    def __init__(self, lexp, op=None, rexp=None):
        """

        :param lexp: left expression
        :param op: condition operation
        :param rexp: right expression
        """
        self.lexp = lexp
        self.rexp = rexp
        self.op = op

    def __repr__(self):
        if self.rexp is not None:
            return "( " + str(self.lexp) + " " + str(self.op) + " " + str(self.rexp) + " )"
        if self.op is not None:
            return "(" + str(self.op) + "( " + str(self.lexp) + " )" + ")"
        else:
            return "" + str(self.lexp) + ""

    def get_lexp(self):
        """

        :return: return left child
        """
        return self.lexp

    def get_rexp(self):
        """

        :return: return right child
        """
        return self.rexp

    def get_op(self):
        """

        :return: return operator
        """
        return self.op

    def get_type(self):
        """

        :return: Condition type.
        """
        return CONDTYPE

class EventAst(list):
    """
    Event AST
    """
    def __init__(self,name,pre,eff):
        """

        :param name: event name
        :param pre: event precondition
        :param eff: list of statements in effect
        """
        self.name = name
        self.pre = pre
        self.eff = eff

    def __repr__(self):
        pre_str = "pre:\n"+str(self.pre)+"\n"
        eff_str = "eff:\n"
        for stmt in self.eff:
            eff_str += str(stmt)+"\n"
        return (self.name+":\n"+pre_str+eff_str)

    def get_type(self):
        return EVENTTYPE

    def get_pre(self):
        """

        :return: precondition
        """
        return self.pre

    def get_name(self):
        """

        :return: event name
        """
        return self.name

    def get_eff(self):
        """

        :return: list of effect statements
        """
        return self.eff

def get_entry(varname, decls):
    """

    :param varname: variable
    :param decls: list of declarations (symtab)
    :return: the declaration corresponding to variable
    """
    for decl in decls:
        if str(decl.get_varname()) == varname :
            return decl
    return None
