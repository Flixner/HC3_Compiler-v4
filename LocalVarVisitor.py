from pycparser import c_ast

from Variable import *


class LocalVarVisitor(c_ast.NodeVisitor):
    """used to pick out the local Variables from a C-Code-Segment (Syntax Tree)"""

    def __init__(self, init_offset):
        self.variables = []
        self.current_offset = init_offset
        self.compound = []
        self.compound_nr = 0

    def visit_Compound(self, node):
        self.compound_nr = self.compound_nr + 1
        self.compound.append(self.compound_nr)
        if node.block_items is not None:
            for n in node.block_items:
                self.visit(n)
            self.compound.pop(-1)

    def visit_ID(self, node):
        if GetFirstVariable(node.name, self.compound, self.variables) is None:
            raise Exception(
                str(node.coord) + ": Error: '" + node.name + "' undeclared (first use in this function)")

    def visit_FuncCall(self, node):
        if node.args is not None:
            for expr in node.args:
                self.visit(expr)

    def visit_Decl(self, node):
        if type(node.type) == c_ast.TypeDecl:
            el = Variable.FromDecl(node)
            if el is None:
                return
            if node.init is not None:
                self.visit(node.init)

            if GetFirstVariableCompound(el.Name, self.compound, self.variables) == self.compound_nr:
                raise Exception(str(node.coord) + ": Error: redeclaration of ‘" + el.Name + "’")

            el.Offset = self.current_offset
            el.compound = self.compound[-1]

            self.current_offset += 1
            self.variables.append(el)

        elif type(node.type) == c_ast.PtrDecl:
            raise Exception(str(node.coord) + ": ERROR: Pointer Declaration not supported ")

        elif type(node.type) == c_ast.ArrayDecl:
            raise Exception(str(node.coord) + ": ERROR: Array Declaration not supported ")

        else:
            raise Exception(str(node.coord) + ": ERROR: Unknown type of Declaration")
