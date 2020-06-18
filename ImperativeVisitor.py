from BinaryOperations import *
from Function import *
import numpy as np


def float16_to_binint(val):
    """ converts a python float to binary16 (IEEE 754 - half precision """
    """ https://en.wikipedia.org/wiki/Half-precision_floating-point_format# """
    return np.float16(val).view('H')


class ImperativeVisitor(c_ast.NodeVisitor):
    """Converts a pure Imperative SyntaxTree (C-Code Segment) to Assembly"""

    def __init__(self, containingFunction):
        self.ContainingFunction = containingFunction
        self.GlobalVars = containingFunction.GlobalVars
        self.LocalVars = containingFunction.LocalVariables
        self.Assembly = Assembly()
        self.FuncName = containingFunction.Name
        self.NodeDepth = 0
        self.LoopLabelForBreak = ""
        self.compound_nr = 0
        self.compound = []

    def generic_visit(self, node):
        # raise Exceptino
        #print(node)
        raise Exception(str(node.coord) + ": ERROR: Unimplemented Operator")

    def visit_Decl(self, node):
        if node.init is not None:
            self.visit(node.init)
            v = AccessVariableByName(node.name, self.compound, self.LocalVars, self.GlobalVars)
            self.Assembly.AppendAssembly(v['Assembly'])  # Loads Variable's Address into r15
            if v['Variable'].Type.IsFloating():
                if not node.type == 'float':
                    self.Assembly.AppendInstruction(Instruction('MOV', ['f0', 'r10'], 'force cast by Hardware'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r15'], 'and store result'))
            else:
                if node.type == 'float':
                    self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'f0'], 'force cast by Hardware'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r15'], 'and store result'))

    def visit_Assignment(self, node):
        # rechts von = ausfuehren (ergebnis landet immer in r10/f0)
        incomingType = self.visit(node.rvalue)
        if incomingType.IsVoid():
            raise Exception(str(node.coord) + ": ERROR: cant assign void")

        v = AccessVariableByName(node.lvalue.name, self.compound, self.LocalVars, self.GlobalVars)
        if v is None:
            raise Exception(str(node.coord) + ": ERROR: undeclared variable: '" + node.lvalue.name + "'")

        d = Arithmetic_Offset_Remove(self.NodeDepth)
        if d is not None:
            self.Assembly.AppendAssembly(d)

        self.Assembly.AppendAssembly(v['Assembly'])  # Loads Variable's Address into r15
        if v['Variable'].Type.IsFloating():  # Casting
            if not incomingType.IsFloating():
                self.Assembly.AppendInstruction(Instruction('MOV', ['f0', 'r10'], 'force cast by Hardware'))
        else:
            if incomingType.IsFloating():
                self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'f0'], 'force cast by Hardware'))

        if node.op != '=':  # Calculating
            if v['Variable'].Type.IsFloating():
                self.Assembly.AppendInstruction(Instruction('MOV', ['f2', 'f0'], 'Move to InputB'))
                self.Assembly.AppendInstruction(Instruction('LOAD', ['f0', 'r15'], 'Load Variable'))
                if node.op == '+=':
                    operationAssembly = processFloatingPoint('+', node.coord)
                elif node.op == '-=':
                    operationAssembly = processFloatingPoint('-', node.coord)
                elif node.op == '*=':
                    operationAssembly = processFloatingPoint('*', node.coord)
                elif node.op == '/=':
                    operationAssembly = processFloatingPoint('/', node.coord)
                else:
                    raise Exception(str(node.coord) + ": ERROR: invalid Assignment operator: '" + node.name + "'")
            else:
                self.Assembly.AppendInstruction(Instruction('MOV', ['r12', 'r10'], 'Move to InputB'))
                self.Assembly.AppendInstruction(Instruction('LOAD', ['r10', 'r15'], 'Load Variable'))
                if node.op == '+=':
                    operationAssembly = processFixedPoint('+', node.coord)
                elif node.op == '-=':
                    operationAssembly = processFixedPoint('-', node.coord)
                elif node.op == '*=':
                    operationAssembly = processFixedPoint('*', node.coord)
                elif node.op == '/=':
                    operationAssembly = processFixedPoint('/', node.coord)
                elif node.op == '%=':
                    operationAssembly = processFixedPoint('%', node.coord)
                elif node.op == '&=':
                    operationAssembly = processFixedPoint('&', node.coord)
                elif node.op == '|=':
                    operationAssembly = processFixedPoint('|', node.coord)
                elif node.op == '^=':
                    operationAssembly = processFixedPoint('^', node.coord)
                elif node.op == '<<=':
                    operationAssembly = processFixedPoint('<<', node.coord)
                elif node.op == '>>=':
                    operationAssembly = processFixedPoint('>>', node.coord)
                else:
                    raise Exception(str(node.coord) + ": ERROR: invalid Assignment operator: '" + node.name + "'")
            if operationAssembly != None:
                self.Assembly.AppendAssembly(operationAssembly)
            else:
                if v['Variable'].Type.IsFloating():
                    raise Exception(
                        str(node.coord) + ": ERROR: unknown operator: '" + node.op + "' using floatingPoint")
                else:
                    raise Exception(str(node.coord) + ": ERROR: unknown operator: '" + node.op + "' using fixedPoint")

        if v['Variable'].Type.IsFloating():  # Storing
            self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r15'], 'and store result'))
        else:
            #Cast short to char if variable is char
            if v['Variable'].Type.IsChar():
                castassembly = cast_short_to_char()
                self.Assembly.AppendAssembly(castassembly)
            self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r15'], 'and store result'))

        d = Arithmetic_Offset_Add(self.NodeDepth)
        if d is not None:
            self.Assembly.AppendAssembly(d)

        return v['Variable'].Type  # Assignment to Varaible forces cast

    def visit_Compound(self, node):
        # Ein Compound is ein Block aus { ...  }
        self.compound_nr = self.compound_nr + 1
        self.compound.append(self.compound_nr)
        if node.block_items is None:
            return
        for n in node.block_items:
            self.visit(n)
        self.compound.pop(-1)

    def visit_ID(self, node):
        v = AccessVariableByName(node.name, self.compound, self.LocalVars, self.GlobalVars)
        if v is None:
            raise Exception(str(node.coord) + ": ERROR: undeclared variable: '" + node.name + "'")

        d = Arithmetic_Offset_Remove(self.NodeDepth)
        if d is not None:
            self.Assembly.AppendAssembly(d)
        self.Assembly.AppendAssembly(v['Assembly'])  # Loads Variable's Address into r15
        if v['Variable'].Type.IsFloating():
            self.Assembly.AppendInstruction(Instruction('LOAD', ['f0', 'r15'], 'and load'))
        else:
            self.Assembly.AppendInstruction(Instruction('LOAD', ['r10', 'r15'], 'and load'))
        d = Arithmetic_Offset_Add(self.NodeDepth)
        if d != None:
            self.Assembly.AppendAssembly(d)
        return v['Variable'].Type

    def visit_UnaryOp(self, node):
        incomingType = self.visit(node.expr)  # result in r10
        if incomingType.IsVoid():
            raise Exception(str(node.coord) + ": ERROR: cant calculate with void")

        if node.op == 'p++':
            if incomingType.IsFloating():
                self.Assembly.AppendInstruction(Instruction('ADDI',  ['f0', 1],     'Increment'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r15'], 'the Variable at the address'))
                self.Assembly.AppendInstruction(Instruction('SUBI',  ['f0', 1],     'Decrement for usage'))
                return Type('float')
            else if incomingType.IsChar() == 'char':
                self.Assembly.AppendInstruction(Instruction('ADDI',  ['r10', 1],     'Increment'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r15'], 'the Variable at the address'))
                self.Assembly.AppendInstruction(Instruction('SUBI',  ['r10', 1],     'Decrement for usage'))
                self.Assembly.AppendsInstruction(Instruction('LUI', ['r22', ord(node.value[1])], '    load Constant char'))
                self.Assembly.AppendInstruction(Instruction('SARIR', ['r10', '8'], '    Cast short to char'))
                self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'r22'], 'move to expected position'))
                return Type('char')
            else:
                self.Assembly.AppendInstruction(Instruction('ADDI',  ['r10', 1],     'Increment'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r15'], 'the Variable at the address'))
                self.Assembly.AppendInstruction(Instruction('SUBI',  ['r10', 1],     'Decrement for usage'))
                return Type('short')
        elif node.op == '++':
            if incomingType.IsFloating():
                self.Assembly.AppendInstruction(Instruction('ADDI',  ['f0', 1],     'Increment'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r15'], 'the Variable at the address'))
                return Type('float')
            else if incomingType.IsChar() == 'char':
                self.Assembly.AppendInstruction(Instruction('ADDI',  ['r10', 1],     'Increment'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r15'], 'the Variable at the address'))
                self.Assembly.AppendsInstruction(Instruction('LUI', ['r22', ord(node.value[1])], '    load Constant char'))
                self.Assembly.AppendInstruction(Instruction('SARIR', ['r10', '8'], '    Cast short to char'))
                self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'r22'], 'move to expected position'))
                return Type('char')
            else:
                self.Assembly.AppendInstruction(Instruction('ADDI',  ['r10', 1],     'Increment'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r15'], 'the Variable at the address'))
                return Type('short')
        elif node.op == 'p--':
            if incomingType.IsFloating():
                self.Assembly.AppendInstruction(Instruction('SUBI',  ['f0', 1],     'Decrement'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r15'], 'the Variable at the address'))
                self.Assembly.AppendInstruction(Instruction('ADDI',  ['f0', 1],     'Increment for usage'))
                return Type('float')
            else if incomingType.IsChar() == 'char':
                self.Assembly.AppendInstruction(Instruction('SUBI',  ['r10', 1],     'Decrement'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r15'], 'the Variable at the address'))
                self.Assembly.AppendInstruction(Instruction('ADDI',  ['r10', 1],     'Increment for usage'))
                self.Assembly.AppendsInstruction(Instruction('LUI', ['r22', ord(node.value[1])], '    load Constant char'))
                self.Assembly.AppendInstruction(Instruction('SARIR', ['r10', '8'], '    Cast short to char'))
                self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'r22'], 'move to expected position'))
                return Type('char')
            else:
                self.Assembly.AppendInstruction(Instruction('SUBI',  ['r10', 1],     'Decrement'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r15'], 'the Variable at the address'))
                self.Assembly.AppendInstruction(Instruction('ADDI',  ['r10', 1],     'Increment for usage'))
                return Type('short')
        elif node.op == '--':
            if incomingType.IsFloating():
                self.Assembly.AppendInstruction(Instruction('SUBI',  ['f0', 1],     'Decrement'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r15'], 'the Variable at the address'))
                return Type('float')
            else if incomingType.IsChar() == 'char':
                self.Assembly.AppendInstruction(Instruction('SUBI',  ['r10', 1],     'Decrement'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r15'], 'the Variable at the address'))
                self.Assembly.AppendsInstruction(Instruction('LUI', ['r22', ord(node.value[1])], '    load Constant char'))
                self.Assembly.AppendInstruction(Instruction('SARIR', ['r10', '8'], '    Cast short to char'))
                self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'r22'], 'move to expected position'))
                return Type('char')
            else:
                self.Assembly.AppendInstruction(Instruction('SUBI',  ['r10', 1],     'Decrement'))
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r15'], 'the Variable at the address'))
                return Type('short')
        elif node.op == '~':
            if incomingType.IsFloating():
                raise Exception(str(node.coord) + ": ERROR: Invalid floating point operation '" + node.op + "'")
            else if incomingType.Char():{
                raise Exception(str(node.coord) + ": ERROR: Invalid char operation '" + node.op + "'")
            else{
               self.Assembly.AppendInstruction(Instruction('NOT', ['r10'], 'exec bitwise not'))
               return Type('short')
            }
        elif node.op == '!':
            if incomingType.IsFloating():
                raise Exception(str(node.coord) + ": ERROR: Invalid floating point operation '" + node.op + "'")
            else if incomingType.Char():{
                raise Exception(str(node.coord) + ": ERROR: Invalid char operation '" + node.op + "'")
            else{
               self.Assembly.AppendInstruction(Instruction('BZ', ['r10', Label.FromCoord(node.coord, 'inFalse').Name], 'jump if input was false'))
                self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'r0'], 'returns false forinput true'))
                self.Assembly.AppendInstruction(Instruction('BZ', ['r0', Label.FromCoord(node.coord, 'end').Name], 'work is done'))
                self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'inFalse'))
                self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'r0'], 'result = TRUE'))
                self.Assembly.AppendInstruction(Instruction('ADDI', ['r10', '1'], ''))
                self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'end'))
                return Type('short')
            }
        else:
            raise Exception(str(node.coord) + ": ERROR: Unknown unary operation '" + str(node.op) + "'")

    def visit_BinaryOp(self, node):
        # evaluate left Node
        inputTypeLeft = self.visit(node.left)  # ergebnis in r10/f0

        # push left Node on Stack
        if inputTypeLeft.IsFloating():
            self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r1'], 'push result of left node on stack'))
        else:
            self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r1'], 'push result of left node on stack'))
        self.Assembly.AppendInstruction(Instruction('SUBI', ['r1', '1'], 'in order to not interfer with right Node a'))
        self.NodeDepth = self.NodeDepth + 1
        # evaluate right Node
        inputTypeRight = self.visit(node.right)  # ergebnis in r10/f0
        if inputTypeRight.IsFloating():
            self.Assembly.AppendInstruction(Instruction('MOV', ['f2', 'f0'], 'result is new inputB'))
        else:
            self.Assembly.AppendInstruction(Instruction('MOV', ['r12', 'r10'], 'result is new inputB'))

        # pop leftNode back and use as input A
        self.Assembly.AppendInstruction(Instruction('ADDI', ['r1', '1'], 'pop result of left node'))
        self.NodeDepth = self.NodeDepth - 1
        if self.NodeDepth < 0:
            raise Exception(str(node.coord) + ": ERROR: Arithmetic Stack underflow")
        if inputTypeLeft.IsFloating():
            self.Assembly.AppendInstruction(Instruction('LOAD', ['f0', 'r1'], 'and put in register for result'))
        else:
            self.Assembly.AppendInstruction(Instruction('LOAD', ['r10', 'r1'], 'and put in register for result'))

        if inputTypeLeft.IsVoid() or inputTypeRight.IsVoid():
            raise Exception(str(node.coord) + ": ERROR: cant calculate with void")

        # depending on Datatype generate according Assembly and cast if needed
        floating = inputTypeLeft.IsFloating() or inputTypeRight.IsFloating()
        if not floating:
            operationAssembly = processFixedPoint(node.op, node.coord)
            if operationAssembly is not None:
                self.Assembly.AppendAssembly(operationAssembly)
            else:
                raise Exception(str(node.coord) + ": ERROR: unknown operator: '" + node.op + "' using fixedPoint")
            return Type('short')
        else:
            # convert the weaker Datatype to stronger (short -> float)
            if not inputTypeLeft.IsFloating():
                self.Assembly.AppendInstruction(Instruction('MOV', ['f0', 'r10'], 'force cast by Hardware'))
            if not inputTypeRight.IsFloating():
                self.Assembly.AppendInstruction(Instruction('MOV', ['f2', 'r12'], 'force cast by Hardware'))

            operationAssembly = processFloatingPoint(node.op, node.coord)
            if operationAssembly is not None:
                self.Assembly.AppendAssembly(operationAssembly)
            else:
                raise Exception(str(node.coord) + ": ERROR: unknown operator: '" + node.op + "' using floatingPoint")
            return Type('float')

    def visit_TernaryOp(self, node):
        self.visit(node.cond)  # ergebnis in r10/f0

        self.Assembly.AppendInstruction(
            Instruction('BZ', ['r10', Label.FromCoord(node.coord, 'false_op').Name], 'jump if condition false'))
        self.Assembly.AppendInstruction(
            Instruction('BZ', ['r0', Label.FromCoord(node.coord, 'then_op').Name],
                        'jump to thenBlock if condition true'))

        self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'false_op'))
        self.Assembly.AppendInstruction(
            Instruction('LUI', ['r22', Label.FromCoord(node.coord, 'else_op').Name], 'jump to else Block'))
        self.Assembly.AppendInstruction(Instruction('LLI', ['r22', Label.FromCoord(node.coord, 'else_op').Name], ''))
        self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

        self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'then_op'))

        true_type = self.visit(node.iftrue)
        index = len(self.Assembly.Code)
        self.Assembly.AppendInstruction(
            Instruction('LUI', ['r22', Label.FromCoord(node.coord, 'end_op').Name], 'jump over else Block'))
        self.Assembly.AppendInstruction(Instruction('LLI', ['r22', Label.FromCoord(node.coord, 'end_op').Name], ''))
        self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

        self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'else_op'))

        false_type = self.visit(node.iffalse)
        if true_type.IsFloating() and (not false_type.IsFloating()):
            self.Assembly.AppendInstruction(Instruction('MOV', ['f0', 'r10'], 'force cast by Hardware'))
        if (not true_type.IsFloating()) and false_type.IsFloating():
            self.Assembly.Code.insert(index + 1, Instruction('MOV', ['f0', 'r10'], 'force cast by Hardware'))
        self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'end_op'))
        if true_type.IsFloating() or false_type.IsFloating():
            return Type('float')
        else:
            return Type('short')

    def visit_Constant(self, node):
        # ToDo: ggf.  split into two 16bit Values
        
        floating = ('.' in node.value) or ('f' in node.value)
        if node.type == 'char':
            self.Assembly.AppendInstruction(Instruction('LUI', ['r22', ord(node.value[1])], '    load Constant char'))
            self.Assembly.AppendInstruction(Instruction('SARIR', ['r10', '8'], '    Cast short to char'))
            self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'r22'], 'move to expected position'))
            return Type('char')
        elif floating:
            self.Assembly.AppendInstruction(
                Instruction('LUI', ['f0', float16_to_binint(node.value)], '     load Constant'))
            self.Assembly.AppendInstruction(
                Instruction('LLI', ['f0', float16_to_binint(node.value)], '     load Constant'))
            return Type('float')
        else:
            self.Assembly.AppendInstruction(Instruction('LUI', ['r22', node.value], '    load Constant'))
            self.Assembly.AppendInstruction(Instruction('LLI', ['r22', node.value], '    load Constant'))
            self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'r22'], 'move to expected position'))
            return Type('short')

    def visit_Expr(self, node):
        floating = ('.' in node.value) or ('f' in node.value)
        if floating:
            self.Assembly.AppendInstruction(Instruction('LUI', ['f0', node.value], '     load Constant'))
            self.Assembly.AppendInstruction(Instruction('LLI', ['f0', node.value], '     load Constant'))
            return Type('float')
        else:
            self.Assembly.AppendInstruction(Instruction('LUI', ['r22', node.value], '    load Constant'))
            self.Assembly.AppendInstruction(Instruction('LLI', ['r22', node.value], '    load Constant'))
            self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'r22'], 'move to expected position'))
            return Type('short')

    def visit_FuncCall(self, node):

        # fetch build-in-functions
        if node.name.name == 'SetLEDR':
            if len(node.args.exprs) != 1:
                raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            v = self.visit(node.args.exprs[0])  # ergebnis in r10 or f0
            if v == Type('float'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r7'], 'set LEDR'))
            elif v == Type('short'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r7'], 'set LEDR'))
            return Type('void')
        elif node.name.name == 'SetHEX0':
            if len(node.args.exprs) != 1:
                raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            v = self.visit(node.args.exprs[0])  # ergebnis in r10 or f0
            self.Assembly.AppendInstruction(Instruction('ADDI', ['r7', 1], '    GOTO HEX0'))
            if v == Type('float'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r7'], 'set HEX0'))
            elif v == Type('short'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r7'], 'set HEX0'))
            self.Assembly.AppendInstruction(Instruction('SUBI', ['r7', 1], '    GOTO LEDR'))
            return Type('void')
        elif node.name.name == 'SetHEX1':
            if len(node.args.exprs) != 1:
                raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            v = self.visit(node.args.exprs[0])  # ergebnis in r10 or f0
            self.Assembly.AppendInstruction(Instruction('ADDI', ['r7', 2], '    GOTO HEX1'))
            if v == Type('float'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r7'], 'set HEX1'))
            elif v == Type('short'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r7'], 'set HEX1'))
            self.Assembly.AppendInstruction(Instruction('SUBI', ['r7', 2], '    GOTO LEDR'))
            return Type('void')
        elif node.name.name == 'SetHEX2':
            if len(node.args.exprs) != 1:
                raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            v = self.visit(node.args.exprs[0])  # ergebnis in r10 or f0
            self.Assembly.AppendInstruction(Instruction('ADDI', ['r7', 3], '    GOTO HEX2'))
            if v == Type('float'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r7'], 'set HEX2'))
            elif v == Type('short'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r7'], 'set HEX2'))
            self.Assembly.AppendInstruction(Instruction('SUBI', ['r7', 3], '    GOTO LEDR'))
            return Type('void')
        elif node.name.name == 'SetHEX3':
            if len(node.args.exprs) != 1:
                raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            v = self.visit(node.args.exprs[0])  # ergebnis in r10 or f0
            self.Assembly.AppendInstruction(Instruction('ADDI', ['r7', 4], '    GOTO HEX3'))
            if v == Type('float'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r7'], 'set HEX3'))
            elif v == Type('short'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r7'], 'set HEX3'))
            self.Assembly.AppendInstruction(Instruction('SUBI', ['r7', 4], '    GOTO LEDR'))
            return Type('void')
        elif node.name.name == 'SetHEX4':
            if len(node.args.exprs) != 1:
                raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            v = self.visit(node.args.exprs[0])  # ergebnis in r10 or f0
            self.Assembly.AppendInstruction(Instruction('ADDI', ['r7', 5], '    GOTO HEX4'))
            if v == Type('float'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r7'], 'set HEX4'))
            elif v == Type('short'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r7'], 'set HEX4'))
            self.Assembly.AppendInstruction(Instruction('SUBI', ['r7', 5], '    GOTO LEDR'))
            return Type('void')
        elif node.name.name == 'SetHEX5':
            if len(node.args.exprs) != 1:
                raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            v = self.visit(node.args.exprs[0])  # ergebnis in r10 or f0
            self.Assembly.AppendInstruction(Instruction('ADDI', ['r7', 6], '    GOTO HEX5'))
            if v == Type('float'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r7'], 'set HEX5'))
            elif v == Type('short'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r7'], 'set HEX5'))
            self.Assembly.AppendInstruction(Instruction('SUBI', ['r7', 6], '    GOTO LEDR'))
            return Type('void')
        elif node.name.name == 'SetHEX6':
            if len(node.args.exprs) != 1:
                raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            v = self.visit(node.args.exprs[0])  # ergebnis in r10 or f0
            self.Assembly.AppendInstruction(Instruction('ADDI', ['r7', 7], '    GOTO HEX6'))
            if v == Type('float'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r7'], 'set HEX6'))
            elif v == Type('short'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r7'], 'set HEX6'))
            self.Assembly.AppendInstruction(Instruction('SUBI', ['r7', 7], '    GOTO LEDR'))
            return Type('void')
        elif node.name.name == 'SetHEX7':
            if len(node.args.exprs) != 1:
                raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            v = self.visit(node.args.exprs[0])  # ergebnis in r10 or f0
            self.Assembly.AppendInstruction(Instruction('ADDI', ['r7', 8], '    GOTO HEX7'))
            if v == Type('float'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r7'], 'set HEX7'))
            elif v == Type('short'):
                self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r7'], 'set HEX7'))
            self.Assembly.AppendInstruction(Instruction('SUBI', ['r7', 8], '    GOTO LEDR'))
            return Type('void')
        elif node.name.name == 'GetSW':
            if node.args is not None:
                if len(node.args.exprs) != 0:
                    raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            self.Assembly.AppendInstruction(Instruction('LOAD', ['r10', 'r8'], 'get SW'))
            return Type('short')
        elif node.name.name == 'GetKEY0':
            if node.args is not None:
                if len(node.args.exprs) != 0:
                    raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            self.Assembly.AppendInstruction(Instruction('ADDI', ['r8', 1], '    GOTO KEY0'))
            self.Assembly.AppendInstruction(Instruction('LOAD', ['r10', 'r8'], 'get KEY0'))
            self.Assembly.AppendInstruction(Instruction('SUBI', ['r8', 1], '    GOTO SW'))
            return Type('short')
        elif node.name.name == 'GetKEY1':
            if node.args is not None:
                if len(node.args.exprs) != 0:
                    raise Exception(str(node.coord) + ": ERROR: too many arguments to function'" + node.name.name + "'")
            self.Assembly.AppendInstruction(Instruction('ADDI', ['r8', 2], '    GOTO KEY1'))
            self.Assembly.AppendInstruction(Instruction('LOAD', ['r10', 'r8'], 'get KEY1'))
            self.Assembly.AppendInstruction(Instruction('SUBI', ['r8', 2], '    GOTO SW'))
            return Type('short')
        else:
            # not build-in

            func = Function.SearchByName(node.name.name)
            if (func == None):
                raise Exception(str(node.coord) + ": ERROR: call of undeclared function '" + node.name.name + "'")
                return Type('short')
            if len(func.Params) < len(node.args.exprs):
                raise Exception(str(node.coord) + ": ERROR: too many arguments to function '" + node.name.name + "'")
            elif len(func.Params) > len(node.args.exprs):
                raise Exception(str(node.coord) + ": ERROR: too few arguments to function '" + node.name.name + "'")
            else:
                i = 0
                if len(node.args.exprs) > i:
                    self.Assembly.AppendInstruction(Instruction('SUBI', ['r1', str(2)], ' GOTO Arguments'))
                    self.NodeDepth = self.NodeDepth + 2
                while len(node.args.exprs) > i:
                    v = self.visit(node.args.exprs[i])  # ergebnis in r10 or f0

                    if func.Params[i].Type.IsFloating():
                        if v == Type('float'):
                            self.Assembly.AppendInstruction(Instruction('STORE', ['f0', 'r1'],
                                                                        " PARA" + str(i) + " => local variable '" +
                                                                        func.Params[i].Name + "'"))
                        else:
                            raise Exception(str(node.coord) + ": ERROR: Cast Detected'")
                    else:
                        if v == Type('float'):
                            raise Exception(str(node.coord) + ": ERROR: Cast Detected'")
                        else:
                            self.Assembly.AppendInstruction(Instruction('STORE', ['r10', 'r1'],
                                                                        " PARA" + str(i) + " => local variable '" +
                                                                        func.Params[i].Name + "'"))
                    self.Assembly.AppendInstruction(Instruction('SUBI', ['r1', str(1)], ' GOTO Next Parameter'))
                    self.NodeDepth = self.NodeDepth + 1
                    i = i + 1
                if i > 0:
                    while i + 2 > 32:
                        self.Assembly.AppendInstruction(Instruction('ADDI', ['r1', 32], ' GOTO FuncCall'))
                        self.NodeDepth = self.NodeDepth - 32
                        i = i - 32
                    self.Assembly.AppendInstruction(Instruction('ADDI', ['r1', str(i + 2)], ' GOTO FuncCall'))
                    self.NodeDepth = self.NodeDepth - (i + 2)

                self.Assembly.AppendInstruction(Instruction('LUI', ['r22', node.name.name], 'r22 = &functionName'))
                self.Assembly.AppendInstruction(Instruction('LLI', ['r22', node.name.name], ''))
                self.Assembly.AppendInstruction(Instruction('JL', ['r3', 'r22'], 'jump to function'))

                if func.ReturnType.IsFloating():
                    self.Assembly.AppendInstruction(Instruction('MOV', ['f0', 'f4'], 'f0  = functionResult'))
                else:
                    self.Assembly.AppendInstruction(Instruction('MOV', ['r10', 'r4'], 'r10 = functionResult'))
                return func.ReturnType

    def visit_If(self, node):
        if node.cond == None:
            raise Exception(str(node.coord) + ": ERROR: empty condition")
            return Assembly()
        if node.iftrue == None:
            raise Exception(str(node.coord) + ": ERROR: empty then Block")
            return Assembly()
        # evaluate condition (result in r10)
        self.visit(node.cond)
        self.Assembly.AppendInstruction(
            Instruction('BZ', ['r10', Label.FromCoord(node.coord, 'false').Name], 'jump if condition false'))
        self.Assembly.AppendInstruction(
            Instruction('BZ', ['r0', Label.FromCoord(node.coord, 'then').Name], 'jump to thenBlock if condition true'))

        if node.iffalse != None:
            # else block exists
            self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'false'))
            self.Assembly.AppendInstruction(
                Instruction('LUI', ['r22', Label.FromCoord(node.coord, 'else').Name], 'jump to else Block'))
            self.Assembly.AppendInstruction(Instruction('LLI', ['r22', Label.FromCoord(node.coord, 'else').Name], ''))
            self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

            self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'then'))
            self.visit(node.iftrue)

            self.Assembly.AppendInstruction(
                Instruction('LUI', ['r22', Label.FromCoord(node.coord, 'end').Name], 'jump over else Block'))
            self.Assembly.AppendInstruction(Instruction('LLI', ['r22', Label.FromCoord(node.coord, 'end').Name], ''))
            self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

            self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'else'))
            self.visit(node.iffalse)
        else:
            # no else block
            self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'false'))
            self.Assembly.AppendInstruction(
                Instruction('LUI', ['r22', Label.FromCoord(node.coord, 'end').Name], 'jump over thenBlock'))
            self.Assembly.AppendInstruction(Instruction('LLI', ['r22', Label.FromCoord(node.coord, 'end').Name], ''))
            self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

            self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'then'))
            self.visit(node.iftrue)

        self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'end'))

    def visit_Switch(self, node):
        if node.cond == None:
            raise Exception(str(node.coord) + ": ERROR: empty condition")
            return Assembly()
        if node.stmt == None:
            raise Exception(str(node.coord) + ": ERROR: empty Compound")
            return Assembly()
        safe_coord = self.LoopLabelForBreak
        self.LoopLabelForBreak = node.coord
        # evaluate condition (result in r10)
        self.visit(node.cond)
        # move the condition on the Stack

        self.Assembly.AppendInstruction(Instruction('MOV', ['r11', 'r10'], ' MOV Condition to r11'))
        # Jump Table
        for case in node.stmt.block_items:
            if type(case) != c_ast.Case and type(case) != c_ast.Default:
                raise Exception(str(node.coord) + ": ERROR: In CaseOf -> only 'Case Constant:' and 'default' allowed")
            if type(case) == c_ast.Case:
                # Move Condition to r10
                self.visit(case.expr)
                self.Assembly.AppendInstruction(Instruction('SUB', ['r10', 'r11'], ' Check if Condtion is True'))
                self.Assembly.AppendInstruction(
                    Instruction('BZ', ['r10', Label.FromCoord(node.coord, "GOTO_" + str(case.expr.value)).Name],
                                ' Case found?'))
                self.Assembly.AppendInstruction(
                    Instruction('BZ', ['r0', Label.FromCoord(node.coord, "NEXT_" + str(case.expr.value)).Name],
                                ' Check Next Case ...'))
                self.Assembly.AppendLabel(Label.FromCoord(node.coord, "GOTO_" + str(case.expr.value)))

                self.Assembly.AppendInstruction(
                    Instruction('LUI', ['r22', Label.FromCoord(node.coord, "START_" + str(case.expr.value)).Name],
                                'jump to case'))
                self.Assembly.AppendInstruction(
                    Instruction('LLI', ['r22', Label.FromCoord(node.coord, "START_" + str(case.expr.value)).Name], ''))
                self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

                self.Assembly.AppendLabel(Label.FromCoord(node.coord, "NEXT_" + str(case.expr.value)))
        if any(type(case) == c_ast.Default for case in node.stmt.block_items):
            self.Assembly.AppendInstruction(
                Instruction('LUI', ['r22', Label.FromCoord(node.coord, "DEFAULT").Name],
                            'jump to default'))
            self.Assembly.AppendInstruction(
                Instruction('LLI', ['r22', Label.FromCoord(node.coord, "DEFAULT").Name], ''))
            self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))
        else:
            self.Assembly.AppendInstruction(
                Instruction('LUI', ['r22', Label.FromCoord(node.coord, "end").Name], 'jump to end'))
            self.Assembly.AppendInstruction(Instruction('LLI', ['r22', Label.FromCoord(node.coord, "end").Name], ''))
            self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

        # Execution
        for case in node.stmt.block_items:
            if type(case) == c_ast.Case:
                # Move Condition to r10
                self.Assembly.AppendLabel(Label.FromCoord(node.coord, "START_" + str(case.expr.value)))
                for statement in case.stmts:
                    self.visit(statement)
            elif type(case) == c_ast.Default:
                self.Assembly.AppendLabel(Label.FromCoord(node.coord, "DEFAULT"))
                for statement in case.stmts:
                    self.visit(statement)
        self.Assembly.AppendLabel(Label.FromCoord(node.coord, "end"))
        self.LoopLabelForBreak = safe_coord

    def visit_Break(self, node):  # only loop or switch
        if self.LoopLabelForBreak == "":
            raise Exception(str(node.coord) + ": ERROR: Break statement not within loop or switch")
        self.Assembly.AppendInstruction(
            Instruction('LUI', ['r22', Label.FromCoord(self.LoopLabelForBreak, 'end').Name], 'jump to exit'))
        self.Assembly.AppendInstruction(
            Instruction('LLI', ['r22', Label.FromCoord(self.LoopLabelForBreak, 'end').Name], ''))
        self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

    def visit_For(self, node):
        if node.init != None:
            if type(node.init) == c_ast.Assignment:
                self.visit(node.init)
            else:
                for decl in node.init:
                    self.visit(decl)

        safe_coord = self.LoopLabelForBreak
        self.LoopLabelForBreak = node.coord

        if type(self.Assembly.Code[-1]) == Label:  # last is label?
            loop_start_label = self.Assembly.Code[-1].Name
        else:
            self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'begin'))
            loop_start_label = Label.FromCoord(node.coord, 'begin').Name
        if node.cond != None:
            self.visit(node.cond)  # evaluate condition (result in r10)
            self.Assembly.AppendInstruction(
                Instruction('BZ', ['r10', Label.FromCoord(node.coord, 'false').Name], 'if condition false'))
            self.Assembly.AppendInstruction(
                Instruction('BZ', ['r0', Label.FromCoord(node.coord, 'continue').Name], 'jump to continue if not done'))
            self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'false'))
            self.Assembly.AppendInstruction(
                Instruction('LUI', ['r22', Label.FromCoord(node.coord, 'end').Name], 'jump to loop exit'))
            self.Assembly.AppendInstruction(Instruction('LLI', ['r22', Label.FromCoord(node.coord, 'end').Name], ''))
            self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))
            self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'continue'))
        else:
            raise Exception(str(node.coord) + ": ERROR: empty for conditions are invalid")
        if node.stmt != None:
            self.visit(node.stmt)  # forBody
        if node.next != None:
            self.visit(node.next)  # forAction
        self.Assembly.AppendInstruction(
            Instruction('LUI', ['r22', loop_start_label], 'jump back to comparison'))
        self.Assembly.AppendInstruction(Instruction('LLI', ['r22', loop_start_label], ''))
        self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

        self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'end'))
        self.LoopLabelForBreak = safe_coord

    def visit_While(self, node):
        if type(self.Assembly.Code[-1]) == Label:  # last is label?
            loop_start_label = self.Assembly.Code[-1].Name
        else:
            self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'begin'))
            loop_start_label = Label.FromCoord(node.coord, 'begin').Name

        if node.cond == None:
            raise Exception(str(node.coord) + ": ERROR: empty while conditions are invalid")
            return

        safe_coord = self.LoopLabelForBreak
        self.LoopLabelForBreak = node.coord

        self.visit(node.cond)  # evaluate condition (result in r10)
        self.Assembly.AppendInstruction(
            Instruction('BZ', ['r10', Label.FromCoord(node.coord, 'false').Name], 'if condition false'))
        self.Assembly.AppendInstruction(
            Instruction('BZ', ['r0', Label.FromCoord(node.coord, 'continue').Name], 'jump to continue if not done'))
        self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'false'))
        self.Assembly.AppendInstruction(
            Instruction('LUI', ['r22', Label.FromCoord(node.coord, 'end').Name], 'jump to loop exit'))
        self.Assembly.AppendInstruction(Instruction('LLI', ['r22', Label.FromCoord(node.coord, 'end').Name], ''))
        self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))
        self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'continue'))
        if node.stmt == None:
            raise Exception(str(node.coord) + ": ERROR: empty while bodies are invalid")
        self.visit(node.stmt)  # whileBody

        self.Assembly.AppendInstruction(
            Instruction('LUI', ['r22', loop_start_label], 'jump back to comparison'))
        self.Assembly.AppendInstruction(Instruction('LLI', ['r22', loop_start_label], ''))
        self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

        self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'end'))

        self.LoopLabelForBreak = safe_coord

    def visit_DoWhile(self, node):
        if type(self.Assembly.Code[-1]) == Label:  # last is label?
            loop_start_label = self.Assembly.Code[-1].Name
        else:
            self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'begin'))
            loop_start_label = Label.FromCoord(node.coord, 'begin').Name

        if node.stmt != None:
            self.visit(node.stmt)  # doBody
        if node.cond == None:
            raise Exception(str(node.coord) + ": ERROR: empty while conditions are invalid")
            return

        safe_coord = self.LoopLabelForBreak
        self.LoopLabelForBreak = node.coord

        self.visit(node.cond)  # evaluate condition (result in r10)
        self.Assembly.AppendInstruction(
            Instruction('BZ', ['r10', Label.FromCoord(node.coord, 'end').Name], 'condition false -> exit loop'))

        self.Assembly.AppendInstruction(
            Instruction('LUI', ['r22', loop_start_label], 'jump back to loop head'))
        self.Assembly.AppendInstruction(Instruction('LLI', ['r22', loop_start_label], ''))
        self.Assembly.AppendInstruction(Instruction('JL', ['r0', 'r22'], 'just jump'))

        self.Assembly.AppendLabel(Label.FromCoord(node.coord, 'end'))

        self.LoopLabelForBreak = safe_coord

    def visit_Return(self, node):
        if node.expr != None:
            incomingType = self.visit(node.expr)
            if incomingType.IsFloating():
                self.Assembly.AppendInstruction(Instruction('MOV', ['f4', 'f0'], 'move result into Return Register'))
            else:
                self.Assembly.AppendInstruction(Instruction('MOV', ['r4', 'r10'], 'move result into Return Register'))
        self.Assembly.AppendAssembly(self.ContainingFunction.GetExitAssembly())


def Arithmetic_Offset_Add(NodeDepth):
    assembly = Assembly()
    i = 0
    while NodeDepth - i * 32 > 32:
        i = i + 1
        assembly.AppendInstruction(
            Instruction('SUBI', ['r1', str(32)], "    Add Arithmetic offset"))
    if NodeDepth - i * 32 > 0:
        assembly.AppendInstruction(
            Instruction('SUBI', ['r1', str(NodeDepth - i * 32)], "    Add Arithmetic offset"))
        return assembly
    return None


def Arithmetic_Offset_Remove(NodeDepth):
    assembly = Assembly()
    i = 0
    while NodeDepth - i * 32 > 32:
        i = i + 1
        assembly.AppendInstruction(
            Instruction('ADDI', ['r1', str(32)], "    Remove Arithmetic offset"))
    if NodeDepth - i * 32 > 0:
        assembly.AppendInstruction(
            Instruction('ADDI', ['r1', str(NodeDepth - i * 32)], "    Remove Arithmetic offset"))
        return assembly
    return None

def cast_short_to_char():
    assem = Assembly()
    assem.AppendInstruction(Instruction('SLOI', ['r10', '8'], '    Cast short to char'))
    assem.AppendInstruction(Instruction('SARIR', ['r10', '8'], '    Cast short to char'))
    return assem
