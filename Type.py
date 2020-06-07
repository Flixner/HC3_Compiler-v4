class Type:
    """A datatype of the C-Code (SyntaxTree)"""

    def __init__(self, name):
        self.Name = name

    def __eq__(self, other):
        if other is None:
            return False
        else:
            return self.Name == other.Name

    @staticmethod
    def FromDecl(decl):
        name = decl.type.type.names[0]
        if name not in ['short', 'float', 'void', 'char']:
            raise Exception('ERROR: invalid Datatype: ' + name + ' @' + str(decl.coord))

        return Type(name)

    def IsFloating(self):
        return self.Name == 'float'

    def IsVoid(self):
        return self.Name == 'void'

    def IsChar(self):
        return self.Name == 'char'
