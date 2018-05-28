"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""
from lines import Comment
from lines import Import

""" Base for all code block object classes """
class Base:
    def __init__(self, name):
        self.name = name
        self.code = []

    #add segment of code to code block
    def add(self,component):
        self.code.append(component) 
    
    #add ending bracket to code block
    def end(self):
        tabs = ''
        if type(self) is Method:
            tabs = '\t'
        if type(self) is Statement:
            tabs = '\t\t'
        self.code.append('{0}}}\n\n'.format(tabs))
    
    #get java code representation of object
    def __str__(self):
        contents = ''
        for c in self.code:
            contents += str(c)
        return contents

""" class code block object class"""
class Class(Base):
    def __init__(self, name, public = True):
        Base.__init__(self, name)
        if public: 
            self.code.append('public class {0} {{\n\n'.format(self.name))
        else:
            self.code.append('class {0} {{\n\n'.format(self.name))

""" header object class """
class Header:
    def __init__(self):
        self.components = {'start':'/*','course_id':'\tCourse: ','student_name':'\tStudent Name: ','student_id':'\tStudent ID: ','program_id':'\tProgram ','due_date':'\tDue Date: ','honor_code':'\tHonor Code: ','program_description':'\tProgram Description: ','end':'*/'}
    #add content to header
    def add(self, name, line = ''):
        if name not in self.components:
            print('add error in header')
            return
        self.components[name] += line
    #empty function to avoid errors
    def end(self):
        pass
    #get java comment representation of header
    def __str__(self):
        contents = ''
        for k,v in self.components.items():
            contents += v + '\n' 
        return contents

""" method code block object class"""
class Method(Base):
    def __init__(self, name, t = 'void', p = ''):
        Base.__init__(self, name) 
        self.type = t
        self.param = p
        if self.name == 'main':
            self.param = 'String[] args'
        self.code.append('\tpublic static {0} {1} ({2}){{\n\n'.format(self.type,self.name,self.param))

""" program object class"""
class Program:
    def __init__(self, name):
        self.name = name
        self.header = None
        self.imports = {}
        self.comments = []
        self.classes = {}
    
    #add component to program by calling specific add function below
    def add(self,item):
        if type(item) == Class:
            self.add_class(item.name,item)
        elif type(item) == Comment:
            self.add_comment(item)
        elif type(item) == Header:
            self.set_header(item)
        elif type(item) == Import:
            self.add_import(item.name,item)
    
    def add_class(self,name, c):
        self.classes[name] = c 

    def add_comment(self, c):
        self.comments.append(c) 

    def add_import(self,name,i):
        self.imports[name] = i

    def set_header(self,header):
        self.header = header
    #get java code representation of entire program
    def __str__(self):
        code = ''
        if self.header:
            code = str(self.header)
        for k,v in self.imports.items():
            code += str(v) 
        for c in self.comments:
            code += str(c) 
        for k,v in self.classes.items():
            code += str(v) 
        return code
        
""" statement code block object class"""
class Statement(Base):
    def __init__(self, name, condition = ''):
        Base.__init__(self, name) 
        if condition != '':
            self.code.append('\t\t{0} ({1}) {{\n\n'.format(self.name,condition))
        else:
            self.code.append('\t\t{0} {{\n\n'.format(self.name))  