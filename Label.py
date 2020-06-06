class Label:
    """A Label to be used within an Assembly"""

    def __init__(self, name):
        self.Name = name
    
    @staticmethod
    def FromCoord(coord, postfix):
        coord_string = str(coord)
        coord_string = coord_string.replace(':',  '_')
        coord_string = coord_string.replace('.',  '_')
        coord_string = coord_string.replace('\\', '_')
        coord_string = coord_string.replace('-',  '_')
        return Label(coord_string + '_' + postfix)

    def __str__(self):
        return self.ToString()

    def ToString(self):
        return self.Name + ': \n'
