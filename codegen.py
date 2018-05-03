# -*- coding: utf-8 -*-
""" The file *codegen.py* includes the code generation functions
which takes in the abstract syntax trees and generates the corresponding
java code.

.. module::codegen
   :synopsis: Code generation functions.
.. moduleauthor:: Ritwika Ghosh <rghosh9@illinois.edu>
"""

import generic
from asts import is_ast
from asttypes import *
from ic import gen_ic
import mdecls


def get_package_decl(app_name):
    '''
    Function to generate package declaration from application name.
    '''
    return generic.add_nl(generic.mk_stmt("package " + app_name.lower()), 2)


def get_class_decl(app_name):
    '''
    Function to generate the Java class declaration.

    '''
    return "public class " + app_name.title() + "App extends LogicThread "


def get_class_method(app_name):
    '''
    class generation method with gvh input
    '''
    return "public " + app_name.title() + "(GlobalVarHolder gvh) "


def get_starl_code(app_code, symtab, delta=100):
    '''
    function for wrapping the event code in the loop. This is where you can change DELTA.
    '''
    return_code = "@Override\n"
    return_code += "public List<Object> callStarL() "
    dsm_code = mk_dsms(symtab)

    app_code = generic.mk_stmt("sleep(" + str(delta) + ")") + app_code
    app_code = dsm_code + "while(true) " + generic.mk_block(app_code, 1)

    return_code += generic.mk_block(app_code, 1)
    return return_code


def createval(dtype):
    """

    :param dtype: datatype for creating numeric default value
    :return:
    """
    if dtype == 'int':
        return 0
    if dtype == 'float':
        return 0.0


def mk_dsms(symtab):
    """
    creating DSM variables
    :param symtab: input symbol table
    :return: string with dsm declarations.
    """
    ret_str = ""
    for decl in symtab:
        if decl.get_scope() == ALLWRITE:
            decl_str = 'dsm.createMW("' + str(decl.get_varname())
            decl_str += '",' + str(createval(str(decl.get_dtype()))) + ")"
            ret_str += generic.mk_stmt(decl_str)
    return ret_str


def get_vars(expr):
    """

    :param expr: expression
    :return: variables in an expression
    """
    if not is_ast(expr):
        return []
    if expr is None:
        return []
    elif expr.get_type() == NULLTYPE:
        return []
    elif expr.get_type() == VARTYPE:
        return [(expr.lexp, None)]
    elif expr.get_type() == ARTYPE:
        return [(expr.varname, expr.access)]
    elif expr.get_type() == NUMTYPE:
        return []
    elif expr.get_type() == BVAL:
        return []
    else:
        return get_vars(expr.get_lexp()) + get_vars(expr.get_rexp())


def ar_get_codegen(var, owner):
    """

    :param var: variable name
    :param owner: pid
    :return: Get code generation for allread
    """
    ret_str = 'dsm.get("' + str(var)
    ret_str += '",name.replaceAll("[0-9]","")+String.valueOf('
    ret_str += str(owner) + '))'
    return ret_str



def aw_get_codegen(var, owner):
    """

    get code generation for allwrite
    """
    return 'dsm.get("' + str(var) + '","*")'


def ar_put_codegen(var):
    """

    :param var: variable
    :return: put code generation for allread
    """
    return 'dsm.put("' + str(var) + '"+name,name,' + str(var) + ');'


def aw_put_codegen(var):
    """

    :param var: variable
    :return: put code generation for allwrite
    """
    return 'dsm.put("' + str(var) + '","*",' + str(var) + ');'



def checknull(var, stages=False, event=None):
    """

    auxiliary function for checking if variable is null, break or continue accordingly
    """
    stmt = ""
    if stages:
        stmt = "break"
    else:
        stmt = "continue"
    return "if (" + str(var) + " == null) {" + stmt + ";}"


def codegen(input_ast, symtab, tabs=0, wnum=0):
    '''
    The main code generation function. It takes as input an AST,
    and returns its corresponding java code. It is called recursively
    on the branches of the syntax tree.

    Args:
        input_ast (ast): if its not an AST, then return nothing, else generate code.
        tabs (int): indentation for generated java program.

    Returns:
        generated_code (str): java code as a string.

    '''
    generated_code = ""

    if not is_ast(input_ast):
        return str(input_ast)

    inputast_type = input_ast.get_type()

    if inputast_type == PGMTYPE:

        app_name = input_ast.get_name()
        include_code = ""

        for flag in input_ast.get_flags():
            include_code += generic.mk_indent(gen_ic(flag), tabs)

        generated_code += get_package_decl(app_name)
        generated_code += include_code
        generated_code += get_class_decl(app_name)
        block_code = generic.add_nl(mdecls.mandatory_decls(input_ast, wnum), 2)

        decl_code = ""
        for decl in symtab:
            decl_code += codegen(decl, [], 0, wnum)

        block_code += generic.mk_indent(decl_code, tabs)
        block_code += get_class_method(app_name)

        init_code = mdecls.mandatory_inits(input_ast, wnum)
        init = input_ast.get_init()
        if init is not None:
            init_code += codegen(init, symtab, tabs, wnum)
        block_code += generic.mk_block(init_code, tabs + 1)

        event_code = ""
        for event in input_ast.get_events():
            event_code += codegen(event, symtab, tabs, wnum)
        block_code += generic.mk_indent(get_starl_code(event_code, symtab), tabs)

        generated_code += generic.mk_block(block_code, tabs + 1)

    elif inputast_type == DECLTYPE:
        dtype = input_ast.get_dtype()
        varname = input_ast.get_varname()
        value = input_ast.get_value()
        decl_str = codegen(dtype, symtab) + " " + codegen(varname, symtab)
        if value is not None:
            decl_str += " = " + codegen(value, symtab)
        generated_code += generic.mk_stmt(decl_str)

    elif inputast_type == BVAL or inputast_type == NUMTYPE:
        generated_code = str(input_ast)

    elif inputast_type == INITTYPE:
        for stmt in input_ast.get_stmts():
            generated_code += codegen(stmt, symtab, tabs, wnum)

    elif inputast_type == EVENTTYPE:
        ename = input_ast.get_name()
        pre_code = "//" + str(ename) + "\n"
        pre_code += "if (" + codegen(input_ast.get_pre(), symtab, 0, wnum) + ")"
        generated_code += generic.mk_indent(pre_code, tabs).rstrip()
        eff_code = ""
        for stmt in input_ast.get_eff():
            eff_code += codegen(stmt, symtab, tabs, wnum)
        eff_code += generic.mk_indent("continue;", tabs)
        generated_code += generic.mk_block(eff_code, tabs + 1)

    elif inputast_type == ASGNTYPE:
        lvar = codegen(input_ast.get_lvar(), symtab, 0, wnum)
        rexp = codegen(input_ast.get_rexp(), symtab, 0, wnum)
        generated_code += generic.mk_stmt(lvar + " = " + rexp)

    elif inputast_type == NUMTYPE:
        generated_code += str(input_ast)

    elif inputast_type == BVAL:
        generated_code += str(input_ast)

    elif inputast_type == VARTYPE:
        generated_code += str(input_ast)

    elif inputast_type == ARITHTYPE:
        generated_code += "(" + codegen(input_ast.get_lexp(), symtab, 0, wnum)
        generated_code += " " + str(input_ast.get_op())
        generated_code += " " + codegen(input_ast.get_rexp(), symtab, 0, wnum) + ")"

    elif inputast_type == RESTYPE:
        generated_code += str(input_ast)

    elif inputast_type == CONDTYPE:
        if input_ast.rexp is not None:
            generated_code += "(" + codegen(input_ast.get_lexp(), symtab, 0, wnum)
            generated_code += " " + str(input_ast.get_op()) + " "
            generated_code += codegen(input_ast.get_rexp(), symtab, 0, wnum) + ")"
        elif input_ast.op is not None:
            generated_code += str(input_ast.get_op())
            generated_code += "(" + codegen(input_ast.lexp, symtab, 0, wnum) + ")"
        else:
            generated_code += codegen(input_ast.get_lexp(), symtab, 0, wnum)

    elif inputast_type == ATOMICTYPE:
        swnum = str(input_ast.get_wnum())
        atomic_pre = "if(!wait" + swnum + ")"
        atomic_code = generic.mk_stmt("mutex" + swnum + ".requestEntry(0)")
        atomic_code += generic.mk_stmt("wait" + swnum + " = true")
        atomic_code = atomic_pre + generic.mk_block(atomic_code, 1)

        entry_pre = "if (mutex" + swnum + ".clearToEnter(0)) "
        entry_code = ""
        for stmt in input_ast.stmts:
            entry_code += codegen(stmt, symtab, 0, wnum)
        entry_code += generic.mk_stmt("mutex" + swnum + ".exit(0)")
        entry_code = entry_pre + generic.mk_block(entry_code, 1)
        generated_code += atomic_code + entry_code

    return generated_code
