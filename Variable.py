from Type import *
from Assembly import *


class Variable:
    def __init__(self):
        """Representation of a C-Variable"""

        self.Name = ''
        self.Type = None
        self.Offset = -1
        self.Init = 0
        self.compound = 0

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return (self.Name == other.Name) and (self.Type == other.Type)

    @staticmethod
    def FromDecl(decl):
        if decl.type.__class__.__name__ != "TypeDecl":
            # only variables
            return None
        el = Variable()
        el.Type = Type.FromDecl(decl)
        if el.Type is None:
            return None
        el.Name = decl.name
        return el


def GetFirstVariable(name, compounds, variables):
    for comp in reversed(compounds):
        for v in variables:
            if comp == v.compound:
                if v.Name == name:
                    return v
    return None


def GetFirstVariableByNameOnly(name, variables):
    for v in variables:
        if v.Name == name:
            return v


def GetFirstVariableCompound(name, compounds, variables):
    for comp in reversed(compounds):
        for v in variables:
            if comp == v.compound:
                if v.Name == name:
                    return v.compound
    return None


def GetAllVariables(name, variables):
    r_vars = []
    for v in variables:
        if v.Name == name:
            r_vars.append(v)
    return r_vars


def AccessVariableByName(name, compound, local_vars, global_vars):
    # returns None if Variable wasn't found
    # if found returns a Dictionary with ['Assembly'] to load the Variable's Address into r15
    # and ['Variable'] contains the Variable
    assembly = Assembly()

    v = GetFirstVariable(name, compound, local_vars)
    if v is not None:
        # variable lokal
        assembly.AppendInstruction(Instruction('MOV', ['r15', 'r1'], 'calculate Adress of'))
        i = 0
        while v.Offset - i * 32 > 32:
            i = i + 1
            assembly.AppendInstruction(
                Instruction('ADDI', ['r15', str(32)], "... "))
        if v.Offset - i * 32 > 0:
            assembly.AppendInstruction(
                Instruction('ADDI', ['r15', str(v.Offset - i * 32)], v.Name + " in Compound " + str(v.compound)))
        return {
            'Assembly': assembly,
            'Variable': v
        }

    v = GetFirstVariableByNameOnly(name, global_vars)
    if v is not None:
        # variable global
        assembly.AppendInstruction(Instruction('LUI', ['r23', v.Name], 'Address'))
        assembly.AppendInstruction(Instruction('LLI', ['r23', v.Name], 'of Var'))
        assembly.AppendInstruction(Instruction('MOV', ['r15', 'r23'],  'mov to expected Register'))
        return {
            'Assembly': assembly,
            'Variable': v
        }
    return None
