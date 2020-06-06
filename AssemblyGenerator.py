from pycparser import c_parser

from FunctionVisitor import *
from GlobalVarVisitor import *

from Variable import *

from Assembly import *
from Label import *
from Instruction import *
from Directive import *


class AssemblyGenerator(object):
    """used to create Assembly from an Syntax Tree (AST)"""

    def __init__(self):
         self.Assembly = Assembly()

    def WorkFromAST(self, ast):
        print("getting global Variables")
        gblVisit = GlobalVarVisitor()
        gblVisit.visit(ast)
        global KnownGlobalVariables

        print("getting Functions")
        funcVisit = FunctionVisitor(gblVisit.Variables)
        funcVisit.visit(ast);

        print('appending default starting Assembly')
        self.Assembly.AppendDirective(Directive('instructionsize 16'))

        print('working through syntax tree ...')
        for func in KnownFunctions:
            self.Assembly.AppendAssembly(func.GetAssembly())

        print('appending DataSegment')
        self.Assembly.AppendAssembly(gblVisit.GetAssemblyForAll())

    def GetInTextform(self):
        return self.Assembly.ToString()
