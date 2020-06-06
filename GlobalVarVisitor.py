from pycparser import c_ast

from Variable import *

from Assembly import *
from Label import *
from Instruction import *

class GlobalVarVisitor(c_ast.NodeVisitor):
    """used to pick out the Global Variables from the C-Code (Syntax Tree)"""

    def __init__(self):
        self.Variables = []
        self.CurrentOffset = 0

    def generic_visit(self, node):
        #called for all other
            if node.__class__.__name__ == "FileAST":
                for c_name, c in node.children():
                    self.visit(c)

    def visit_Decl(self, node):
        el = Variable.FromDecl(node)
        if el == None:
            return
        if node.init != None:
            if node.init.__class__.__name__ == "Constant":
                el.Init = node.init.value
            else:
                raise Exception('ERROR: cannot inititialise with non Constant @ ' + str(node.coord))

        el.Offset = self.CurrentOffset
        self.CurrentOffset += 1
        self.Variables.append(el)
        print('Variable definition for: ' + node.name)

    def GetAssemblyForSpecific(self,el):
        ret = Assembly()
        ret.AppendLabel(Label(el.Name))
        ret.AppendInstruction(Instruction('DATA', [el.Init], el.Type.Name + ' ' + el.Name))
        return ret

    def GetAssemblyForAll(self):
        ret = Assembly()
        for el in self.Variables:
            ret.AppendAssembly(self.GetAssemblyForSpecific(el))
        return ret
