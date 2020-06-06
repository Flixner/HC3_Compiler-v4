from LocalVarVisitor import *
from Variable import *

KnownFunctions = []


class Function:
    """representation of a C-Function"""

    @staticmethod
    def SearchByName(name):
        for func in KnownFunctions:
            if func.Name == name:
                return func
        return None

    def __init__(self, name, parameters, body, return_type, global_vars):
        self.Name = name
        self.Body = body
        self.LocalVariables = []
        self.ReturnType = return_type
        self.Params = parameters
        self.GlobalVars = global_vars

    def GetEntryAssembly(self):
        ret = Assembly()
        ret.AppendLabel(Label(self.Name))
        if self.Name == 'main':
            ret.AppendInstruction(Instruction('LUI', ['r22', '0xFFDF'], 'initialise STACK'))
            ret.AppendInstruction(Instruction('LLI', ['r22', '0xFFDF'], ''))
            ret.AppendInstruction(Instruction('MOV', ['r1', 'r22'],     ''))

        else:
            ret.AppendInstruction(Instruction('STORE', ['r2', 'r1'], 'function entry-point'))
            ret.AppendInstruction(Instruction('SUBI',  ['r1', '1'],  'together with above: save(push) FUNC on stack'))
            ret.AppendInstruction(Instruction('STORE', ['r3', 'r1'], 'push LINK on stack (just in case)'))
            ret.AppendInstruction(Instruction('SUBI',  ['r1', '1'],  '...'))
            ret.AppendInstruction(Instruction('MOV',   ['r2', 'r1'], 'set Function Basepointer = STACK on calltime'))
        return ret

    def GetParameterAssembly(self):
        ret = Assembly()

        local_var_visit = LocalVarVisitor(1)
        i = 0
        while len(self.Params) > i:
            self.Params[i].compound = 1
            local_var_visit.variables.append(self.Params[i])
            i = i + 1

        # take care of local variables
        local_var_visit.visit(self.Body)
        self.LocalVariables = local_var_visit.variables
        i = 0
        while len(self.LocalVariables) - i * 32 > 32:
            ret.AppendInstruction(Instruction('SUBI', ['r1', str(32)],
                                              '    reserve space for local variables on stack'))
            i = i + 1
        if len(self.LocalVariables) - i * 32 > 0:
            ret.AppendInstruction(Instruction('SUBI', ['r1', str(len(self.LocalVariables) - i * 32)],
                                              '    reserve space for local variables on stack'))
        i = len(self.Params) - 1
        while i >= 0:
            local_var_visit.variables[i].Offset = len(self.LocalVariables) - i
            i = i - 1

        return ret

    def GetBodyAssembly(self):
        from ImperativeVisitor import ImperativeVisitor
        ret = Assembly()
        imp_visit = ImperativeVisitor(self)
        imp_visit.visit(self.Body)
        ret.AppendAssembly(imp_visit.Assembly)
        return ret

    def GetExitAssembly(self):
        ret = Assembly()
        if self.Name == 'main':
            ret.AppendInstruction(Instruction('JL', ['r0', 'r0'], 'return'))
        else:
            ret.AppendInstruction(Instruction('MOV',  ['r1', 'r2'],
                                              'mark local variables as undeclared (just move STACK back)'))
            ret.AppendInstruction(Instruction('ADDI', ['r1', '1'],  'pop LINK back from stack'))
            ret.AppendInstruction(Instruction('LOAD', ['r3', 'r1'], '...'))
            ret.AppendInstruction(Instruction('ADDI', ['r1', '1'],  'pop FUNC back from stack'))
            ret.AppendInstruction(Instruction('LOAD', ['r2', 'r1'], '...'))
            ret.AppendInstruction(Instruction('JL',   ['r0', 'r3'], 'return'))
        return ret

    def GetAssembly(self):
        ret = Assembly()
        if self.Body is not None:
            ret.AppendAssembly(self.GetEntryAssembly())
            ret.AppendAssembly(self.GetParameterAssembly())
            ret.AppendAssembly(self.GetBodyAssembly())
            ret.AppendAssembly(self.GetExitAssembly())
        return ret
