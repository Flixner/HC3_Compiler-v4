from pycparser import c_ast
from Assembly import *
from Label import *
from Instruction import *


def processFixedPoint(operation,coordinates):
    """creates Assembly for all the different Binary Operations (+,-,*,...)
    using fixedPoint Data and therefore instructions
    Source Registers r10, r12
    Destination Register r10
    r10 = r10 - r12"""

    assem = Assembly()

    if operation == '+':
        assem.AppendInstruction(Instruction('ADD', ['r10', 'r12'], 'add source B'))
    elif operation == '-':
        assem.AppendInstruction(Instruction('SUB', ['r10', 'r12'], 'sub source B'))
    elif operation == '*':
        assem.AppendInstruction(Instruction('MUL', ['r10', 'r12'], 'mul source B'))
    elif operation == '/':
        assem.AppendInstruction(Instruction('DIV', ['r10', 'r12'], 'div by source B'))
    elif operation == '%':
        assem.AppendInstruction(Instruction('MOD', ['r10', 'r12'], 'mod by source B'))
    elif operation == '&':
        assem.AppendInstruction(Instruction('AND', ['r10', 'r12'], 'bitwise and source B'))
    elif operation == '|':
        assem.AppendInstruction(Instruction('OR' , ['r10', 'r12'], 'bitwise or source B'))
    elif operation == '^':
        assem.AppendInstruction(Instruction('MOV', ['r11', 'r12'], 'B'))
        assem.AppendInstruction(Instruction('NOT', ['r11'], 'not B'))
        assem.AppendInstruction(Instruction('AND', ['r11', 'r10'], 'A and not B'))
        assem.AppendInstruction(Instruction('NOT', ['r10'], 'not A'))
        assem.AppendInstruction(Instruction('AND', ['r10', 'r12'], 'not A and B'))
        assem.AppendInstruction(Instruction('OR' , ['r10', 'r11'], 'bitwise xor source B'))
    elif operation == '!=':
        assem.AppendInstruction(Instruction('SUB', ['r10', 'r12'], 'if A == B ==> r10 == 0'))
        assem.AppendInstruction(Instruction('BZ' , ['r10', Label.FromCoord(coordinates, 'one').Name],  'creating a logical not'))
        assem.AppendInstruction(Instruction('MOV', ['r10', 'r0'], 'result = TRUE'))
        assem.AppendInstruction(Instruction('ADDI', ['r10', '1'], ''))
        assem.AppendInstruction(Instruction('BZ' , ['r0' , Label.FromCoord(coordinates, 'end').Name],  'done'))
        assem.AppendLabel(Label.FromCoord(coordinates, 'one'))
        assem.AppendInstruction(Instruction('MOV', ['r10', 'r0' ] , 'result = FALSE'))
        assem.AppendLabel(Label.FromCoord(coordinates, 'end'))
    elif operation == '==':
        assem.AppendInstruction(Instruction('SUB', ['r10', 'r12'], 'if A == B ==> r10 == 0'))
        assem.AppendInstruction(Instruction('BZ' , ['r10', Label.FromCoord(coordinates, 'one').Name],  'creating a logical not'))
        assem.AppendInstruction(Instruction('MOV', ['r10', 'r0' ] , 'result = FALSE'))
        assem.AppendInstruction(Instruction('BZ' , ['r0' , Label.FromCoord(coordinates, 'end').Name],  'done'))
        assem.AppendLabel(Label.FromCoord(coordinates, 'one'))
        assem.AppendInstruction(Instruction('MOV', ['r10','r0' ], 'result = TRUE'))
        assem.AppendInstruction(Instruction('ADDI',['r10','1'  ], ''))
        assem.AppendLabel(Label.FromCoord(coordinates, 'end'))
    elif operation == '<':
        assem.AppendInstruction(Instruction('SUB', ['r12', 'r10'], 'if A < B ==> r12 > 0'))
        assem.AppendInstruction(Instruction('BPOS',['r12', Label.FromCoord(coordinates, 'one').Name],  'comparing with zero'))
        assem.AppendInstruction(Instruction('MOV', ['r10', 'r0' ] , 'result = FALSE'))
        assem.AppendInstruction(Instruction('BZ',  ['r0' , Label.FromCoord(coordinates, 'end').Name],  'done'))
        assem.AppendLabel(Label.FromCoord(coordinates, 'one'))
        assem.AppendInstruction(Instruction('MOV', ['r10','r0' ], 'result = TRUE'))
        assem.AppendInstruction(Instruction('ADDI',['r10','1'  ], ''))
        assem.AppendLabel(Label.FromCoord(coordinates, 'end'))
    elif operation == '>':
        assem.AppendInstruction(Instruction('SUB', ['r10', 'r12'], 'if A > B ==> r10 > 0'))
        assem.AppendInstruction(Instruction('BPOS',['r10', Label.FromCoord(coordinates, 'one').Name],  'comparing with zero'))
        assem.AppendInstruction(Instruction('MOV', ['r10', 'r0' ] , 'result = FALSE'))
        assem.AppendInstruction(Instruction('BZ',  ['r0' , Label.FromCoord(coordinates, 'end').Name],  'done'))
        assem.AppendLabel(Label.FromCoord(coordinates, 'one'))
        assem.AppendInstruction(Instruction('MOV', ['r10','r0' ], 'result = TRUE'))
        assem.AppendInstruction(Instruction('ADDI',['r10','1'  ], ''))
        assem.AppendLabel(Label.FromCoord(coordinates, 'end'))
    elif operation == '<=':
        assem.AppendInstruction(Instruction('SUB', ['r12', 'r10'], 'if A =< B ==> r12 >= 0'))
        assem.AppendInstruction(Instruction('BPOS', ['r12', Label.FromCoord(coordinates, 'one').Name], 'comparing with zero'))
        assem.AppendInstruction(Instruction('BZ', ['r12', Label.FromCoord(coordinates, 'one').Name], 'comparing with zero'))
        assem.AppendInstruction(Instruction('MOV', ['r10', 'r0'], 'result = FALSE'))
        assem.AppendInstruction(Instruction('BZ', ['r0', Label.FromCoord(coordinates, 'end').Name], 'done'))
        assem.AppendLabel(Label.FromCoord(coordinates, 'one'))
        assem.AppendInstruction(Instruction('MOV', ['r10', 'r0'], 'result = TRUE'))
        assem.AppendInstruction(Instruction('ADDI', ['r10', '1'], ''))
        assem.AppendLabel(Label.FromCoord(coordinates, 'end'))
    elif operation == '>=':
        assem.AppendInstruction(Instruction('SUB', ['r10', 'r12'], 'if A >= B ==> r10 >= 0'))
        assem.AppendInstruction(Instruction('BPOS',['r10', Label.FromCoord(coordinates, 'one').Name],  'comparing with zero'))
        assem.AppendInstruction(Instruction('BZ', ['r10', Label.FromCoord(coordinates, 'one').Name], 'comparing with zero'))
        assem.AppendInstruction(Instruction('MOV', ['r10', 'r0' ] , 'result = FALSE'))
        assem.AppendInstruction(Instruction('BZ',  ['r0' , Label.FromCoord(coordinates, 'end').Name],  'done'))
        assem.AppendLabel(Label.FromCoord(coordinates, 'one'))
        assem.AppendInstruction(Instruction('MOV', ['r10','r0' ], 'result = TRUE'))
        assem.AppendInstruction(Instruction('ADDI',['r10','1'  ], ''))
        assem.AppendLabel(Label.FromCoord(coordinates, 'end'))
    elif operation == '<<':
        assem.AppendInstruction(Instruction('SLO', ['r10', 'r12'], 'Arithmetic-shift the value in R10 by the value in R12 to the left and store the result in R10'))
    elif operation == '>>':
        assem.AppendInstruction(Instruction('SLOR', ['r10', 'r12'], 'Arithmetic-shift the value in R10 by the value in R12 to the right and store the result in R10'))
    else:
        return None
    return assem

def processFloatingPoint(operation,coordinates):
    """creates Assembly for all the different Binary Operations (+,-,*,...)
    using floatingPoint Data and therefore instructions
    Source Registers f1, f2
    Destination Register f0
    f0 = f1 - f2"""

    assem = Assembly()

    if operation == '+':
        assem.AppendInstruction(Instruction('ADD', ['f0', 'f2'], 'add source B'))
    elif operation == '-':
        assem.AppendInstruction(Instruction('SUB', ['f0', 'f2'], 'sub source B'))
    elif operation == '*':
        assem.AppendInstruction(Instruction('MUL', ['f0', 'f2'], 'mul source B'))
    elif operation == '/':
        assem.AppendInstruction(Instruction('DIV', ['f0', 'f2'], 'div by source B'))
    else:
        return None
    return assem