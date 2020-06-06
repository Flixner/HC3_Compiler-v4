from pycparser import c_ast
from LocalVarVisitor import *
from ImperativeVisitor import *

from Variable import *
from Type import *

from Assembly import *
from Label import *
from Instruction import *

from Function import *

class FunctionVisitor(c_ast.NodeVisitor):
    """Visitor used to search for function definitions and declarations and managing them"""
    def __init__(self, globalVars):
        self.GlobalVars = globalVars

    def visit_FuncDef(self, node):
        functionName = node.decl.name
        paramVariables = []
        if node.decl.type.args != None:
            for paramDecl in node.decl.type.args.params:
                paramVar = Variable.FromDecl(paramDecl)
                if paramVar != None:
                    if paramVar.Type.IsVoid():
                        raise Exception('ERROR: parameter cant be void @' + str(node.coord))
                    else:
                        paramVariables.append(paramVar)
        existingFunc = Function.SearchByName(functionName)
        if existingFunc != None:
            if existingFunc.Body != None:
                raise Exception('multiple definition of ' + functionName + ' @' +str (node.coord))

            else:
                if existingFunc.Params == paramVariables:
                    existingFunc.Body = node.body
                    print('filling Function declaration of ' + functionName + ' with definition')
                else:
                    raise Exception('ERROR: conflicting Function definition of ' + functionName + ' with declaration')
        else:
            KnownFunctions.append(Function(functionName, paramVariables, node.body, Type.FromDecl(node.decl.type), self.GlobalVars))
            print('Function definition for: ' + functionName)

    def visit_FuncDecl(self, node):
        functionName = node.type.declname
        paramVariables = []
        if node.args != None:
            for paramDecl in node.args.params:
                paramVar = Variable.FromDecl(paramDecl)
                if paramVar != None:
                    if paramVar.Type.IsVoid():
                        raise Exception('ERROR: parameter cant be void @' + str(node.coord))
                    else:
                        paramVariables.append(paramVar)
        if Function.SearchByName(functionName) != None:
            raise Exception('ERROR: multiple declaration of ' + functionName + ' @' +str (node.coord))
        else:
            KnownFunctions.append(Function(functionName, paramVariables, None, Type.FromDecl(node), self.GlobalVars))
            print('Function declaration for: ' + functionName)