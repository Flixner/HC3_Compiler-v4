from Label import *
from Instruction import *
from Directive import *

class Assembly():
    """Complete Assembly: containing Instructions, Directives and Labels"""

    def __init__(self):
        self.Code = []

    def AppendInstruction(self, instruction):
        self.Code.append(instruction)

    def AppendDirective(self, directive):
        self.Code.append(directive)

    def AppendLabel(self, label):
        self.Code.append(label)

    def AppendAssembly(self, assembly):
        self.Code = self.Code + assembly.Code

    def __str__(self):
        return self.ToString

    def ToString(self):
        ret = ''
        for el in self.Code:
            ret += str(el)
        return ret
