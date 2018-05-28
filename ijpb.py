"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""
import copy as cp
from blocks import *
from lines import *

""" Incremental Java Program Builder Object """
class IJPB:	
	
    def __init__(self):
        self.program = None
        self.stack = []
        self.trace_enabled = True
    
    #show parsing progress    
    def enable_trace(self):
        self.trace_enabled = True
    
    #hide parsing progress
    def disable_trace(self):
        self.trace_enabled = False
    
    #start program
    def prime_program(self, name):
        if len(self.stack) == 0:
            self.stack.append(Program(name))
    
    #check if currently not in a method
    def not_in_method(self):
        if len(self.stack) < 3 or (type(self.stack[-1]) is not Method and type(self.stack[-1]) is not Statement):
            return True
        return False
     
    #check if currently not just inside program 
    def not_only_in_program(self):
        if len(self.stack) != 1 or type(self.stack[0]) is not Program:
            return True
        return False
    
    #check if currently not just inside a class
    def not_only_in_class(self):
        if len(self.stack) < 2 or type(self.stack[-1]) is not Class:
            return True
        return False
    
    #check if not currently inside program at any level
    def not_in_program(self):
        if len(self.stack) < 1 or type(self.stack[0]) is not Program:
            return True
        return False
    
    #check if currently not inside a class
    def not_in_class(self):
        if len(self.stack) < 2 or (type(self.stack[-1]) is not Class and type(self.stack[-1]) is not Method and type(self.stack[-1]) is not Statement):
            return True
        return False

    #check if not currently not inside the header
    def not_in_header(self):
        if len(self.stack) < 2 or type(self.stack[-1]) is not Header:
            return True
        return False

    #start a class 
    def add_class(self, name):
        if self.not_only_in_program():
            self.syntax_error('Attempt to add class inside another component.')
            return
        if name == self.stack[0].name[:-5]:
            self.stack.append(Class(name))
        else:
            self.stack.append(Class(name,False))      
    
     #start a statement 
    def add_statement(self, name, con = ''):
        if self.not_in_method():
            self.syntax_error('Attempt to add statement outside of a method.')
            return
        condition = ''
        for c in con:
            condition += '{0} '.format(c) 
        self.stack.append(Statement(name,condition)) 

    #start a header 
    def add_header(self):
        if self.not_only_in_program():  
            self.syntax_error('attempt to add header inside another component')
            return
        self.stack.append(Header())
    
    #add an import to program
    def add_import(self, name):
        if self.not_only_in_program():
            self.syntax_error('attempt to add import inside another component')
            return
        self.stack[0].add(Import(name))
    
    #add content to header
    def add_content(self, name, con):
        if self.not_in_header():
            self.syntax_error('attempt to add header content outside of header')
            return        
        contents = ''
        for c in con:
            contents += '{0} '.format(c) 
        self.stack[-1].add(name,contents)

    #add a return statement to program
    def add_return(self, con):
        if self.not_in_method():
            self.syntax_error('attempt to add return statement outside of method')
        else:
            contents = ''
            for c in con:
                contents += '{0} '.format(c) 
            self.stack[-1].add(Return(contents))

    #add a print statement to program
    def add_print(self, params):
        if self.not_in_method():
            self.syntax_error('attempt to add print statement outside of method')
            return      
        if '|' in params:
            index = params.index('|')
        else:
            index = len(params) 
        contents, variables = '',params[index+1:]
        con = params[:index]
        for c in con:
            contents += '{0} '.format(c) 
        self.stack[-1].add(Print(contents, variables))

    #add a comment to program
    def add_comment(self, con):
        if self.not_in_program():
            self.syntax_error('attempt to add comment outside of program')
            return
        contents = ''
        for c in con:
            contents += '{0} '.format(c) 
        self.stack[-1].add(Comment(contents))

    #add a code fragment to program
    def add_fragment(self, contents):
        if self.not_in_method():
            self.syntax_error('attempt to add fragment outside of method')
            return
        self.stack[-1].add(Fragment(contents))

    #add a variable declaration to program
    def add_variable(self, name, ty):
        if self.not_in_class():
            self.syntax_error('attempt to add variable outside of class')
            return
        self.stack[-1].add(Variable(name,ty))

    #add an object declaration to program
    def add_object(self, name, ty):
        if self.not_in_class():
            self.syntax_error('attempt to add object outside of class')
            return
        self.stack[-1].add(Object(name,ty))

    #add an assignment to program
    def add_assignment(self, name, contents):
        if self.not_in_class():
            self.syntax_error('attempt to add assignment outside of class')
            return
        self.stack[-1].add(Assignment(name, contents))
    
    #start a method 
    def add_method(self, name, ty = 'void', p = []):
        if self.not_only_in_class():
            self.syntax_error('attempt to add method outside of class or inside another method')
            return
        if len(p) % 2 == 0:
            params = ''
            for i in range(0,len(p),2):
                if (i + 1) == (len(p) - 1):
                    params += '{0} {1}'.format(p[i],p[i+1])
                else: 
                    params += '{0} {1}, '.format(p[i],p[i+1])
            self.stack.append(Method(name,ty,params))
        else: 
            self.syntax_error('unknown error adding method')
    
    #finish a code block and add it to its parent
    def finish_component(self):
        self.stack[-1].end()
        self.stack[-2].add(self.stack[-1])
        self.stack = self.stack[:-1]

    #finish program
    def finish_program(self):
        if len(self.stack) != 1:
            self.syntax_error('attempt to finish program prematurely')
        else:
            self.program = cp.copy(self.stack[0])
            self.stack = []
            self.trace('\n..completed definition of program {0}..'.format(self.program.name))
            self.create_program_file()
    
    #write program to file
    def create_program_file(self):
        try:
            f = open(self.program.name,'w+')
            f.write(str(self.program)) 
            f.close()
            print('\n\n{0} created'.format(self.program.name))
        except Exception as e:
            print('error creating {0}'.format(self.program.name))
        
    #get program, redundant
    def get_program(self):
        return self.program
    
    #error
    def syntax_error(self, msg):
        raise RecognitionError('[Error] {0}'.format(msg))

    #output parsing progress
    def trace(self, msg):
        if self.trace_enabled:
            print(msg)


class RecognitionError(Exception):
    pass