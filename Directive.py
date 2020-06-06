class Directive():
    """A Directive to be used within an Assembly"""

    def __init__(self, command):
        self.Command = command
    
    def __str__(self):
        return self.ToString()

    def ToString(self):
        return '#' + self.Command + '\n'
