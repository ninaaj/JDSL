"""
	Christina Trotter
	CSCI 658
	Assignment #4
	5/5/18
"""
""" base for object and variable object class"""
class OVB:
    def __init__(self, name, t):
        self.name = name
        self.type = t
    #get java code rep
    def __str__(self):
        return '\t\t{0} {1};\n\n'.format(self.type,self.name)   

""" assignment object class"""
class Assignment:
    def __init__(self,name,contents):
        self.name = name
        self.contents = contents
        self.is_object() # check if instantiating an object
    #get java code rep
    def __str__(self):
        return '\t\t{0} = {1};\n\n'.format(self.name,self.contents)
    #if instantiating object and word new in front of assignment contents
    def is_object(self):
        if self.contents[0].isupper() and '(' in self.contents and ')' in self.contents:
            self.contents = 'new ' + self.contents

""" comment object class"""
class Comment:
    def __init__(self, contents):
        self.contents = contents
    #get java code rep
    def __str__(self):
        return '\t\t//{0}\n\n'.format(self.contents)

""" fragment object class"""
class Fragment:
    def __init__(self, contents):
        self.contents = contents
    #get java code rep
    def __str__(self):
        return '\t\t{0};\n\n'.format(self.contents)

""" import object class"""
class Import:
    def __init__(self, name):
        self.name = name
    #get java code rep
    def __str__(self):
        return 'import java.util.{0};\n\n'.format(self.name)

""" object object class"""
class Object(OVB):
    def __init__(self, name, t):
        OVB.__init__(self, name, t) 

""" print statement object class"""
class Print:
    def __init__(self,contents,variables = None):
        self.contents = contents
        self.variables = variables
    #get java code rep
    def __str__(self):
        if self.variables:
            vstr = ''
            for v in self.variables:
                vstr += ',{0}'.format(v)
            return '\t\tSystem.out.printf("{0}"{1});\n\n'.format(self.contents,vstr)
        return '\t\tSystem.out.print("{0}");\n\n'.format(self.contents)

""" return statement object class"""
class Return:
    def __init__(self, contents = ''):
        self.contents = contents
    #get java code rep
    def __str__(self):
        return '\t\treturn {0};\n\n'.format(self.contents)

""" variable object class"""
class Variable(OVB):
    def __init__(self, name, t):
        OVB.__init__(self, name, t)   