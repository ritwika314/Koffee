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


def get_starl_code(app_code):
    '''
    function for wrapping the event code in the loop.
    '''
    return_code = "@Override\n"
    return_code += "public List<Object> callStarL() "
    app_code = "while(true) " + generic.mk_block(app_code, 1)
    return_code += generic.mk_block(app_code, 1)
    return return_code


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
        block_code += generic.mk_indent(get_starl_code(event_code), tabs)
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
        pre_code = "if (" + codegen(input_ast.get_pre(), symtab, 0, wnum) + ")"
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

    return generated_code
