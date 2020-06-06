class Instruction:
    """A single Instruction to be used within an Assembly"""

    def __init__(self, mnemonic, params, comment):
        self.Mnemonic = mnemonic
        self.Params = params
        self.Comment = comment

    def __str__(self):
        return self.ToString()

    def ToString(self):
        ret = '\t'
        ret += self.Mnemonic
        ret += ' '
        for para in self.Params:
            ret += str(para)
            ret += ' '
        ret += ';\t\t'
        ret += str(self.Comment) 
        ret += '\n'
        return ret
