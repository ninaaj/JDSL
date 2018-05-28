"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""

import os.path as op, re, sys, traceback
from lp import LineParser

""" Top Level Line Parser (outside of program) """
class TLLParser(LineParser):
    def __init__(self, context):
        LineParser.__init__(self, context)
    #parse line accordingly
    def do_parse(self):   
        if self.has_keyword('program'):
            self.parse_program()
        else:
            self.fail_to_recognize_line()

""" Second Level Line Parser (inside of program)"""
class ProgramParser(LineParser):
    def __init__(self, context):
        LineParser.__init__(self, context)
    #parse line accordingly
    def do_parse(self):
        if self.has_only_word('end'):
            self.return_to_upper_level(TLLParser(self.context))
        
        elif self.has_keyword('class') and len(self.words) == 2:
            self.parse_class()
        
        elif self.has_keyword('comment') and len(self.words) > 1:
            self.parse_comment()
        
        elif self.has_only_word('header'):
            self.parse_header()
        
        elif self.has_keyword('import') and len(self.words) == 2:
            self.parse_import()
        else:
            self.fail_to_recognize_line()

""" Parser for contents of optional program header (inside of header)"""
class HeaderParser(LineParser):
    def __init__(self, context):
        LineParser.__init__(self, context)
    #parse line accordingly
    def do_parse(self):
        if self.has_only_word('end'):
            self.context.finish_component()
            self.return_to_upper_level(ProgramParser(self.context))
        elif len(self.words) > 1:
            self.parse_header_line()
        else:
            self.fail_to_recognize_line()

""" Third Level Parser (inside of class)"""
class ClassParser(LineParser):
    def __init__(self, context):
        LineParser.__init__(self, context)
    #parse line accordingly
    def do_parse(self):
        if self.has_only_word('end'):
            self.context.finish_component()
            self.return_to_upper_level(ProgramParser(self.context)) 
        
        elif self.has_keyword('comment') and len(self.words) > 1:
            self.parse_comment()
        
        elif self.has_keyword('method') and len(self.words) > 1:
            
            self.parse_method()
        else:
            self.fail_to_recognize_line()

""" Fourth Level Parser (inside of method)"""
class MethodParser(LineParser):
    def __init__(self, context):
        LineParser.__init__(self, context)
    #parse line accordingly
    def do_parse(self):
        if self.has_only_word('end'):
            self.context.finish_component()
            self.return_to_upper_level(ClassParser(self.context))
        
        elif self.has_keyword('assignment') and len(self.words) == 3:
            self.parse_assignment()
        
        elif self.has_keyword('comment') and len(self.words) > 1:
            self.parse_comment()
        
        elif self.has_keyword('fragment') and len(self.words) == 2:
            self.parse_fragment()

        elif self.has_keyword('object') and len(self.words) == 3:
            self.parse_object()
        
        elif self.has_keyword('print') and len(self.words) > 1:
            self.parse_print()
        
        elif self.has_keyword('return'):
            self.parse_return()
        
        elif self.has_keyword('statement') and len(self.words) > 1:
            self.parse_statement()
        
        elif self.has_keyword('variable') and len(self.words) == 3:
            self.parse_variable()
        
        else:
            self.fail_to_recognize_line()

""" Fifth >= Level Parser for if/else/elif statements and for/while loops (inside statements and loops, can become recursive)"""
class StatementParser(LineParser):
    def __init__(self, context, depth = 0):
        LineParser.__init__(self, context)
        self.depth = depth
    #parse line accordingly
    def do_parse(self):
        if self.has_only_word('end'):
            self.context.finish_component()
            if self.depth == 0:
                self.return_to_upper_level(MethodParser(self.context))
            else:
                self.return_to_upper_level(StatementParser(self.context,self.depth-1))
        
        elif self.has_keyword('assignment') and len(self.words) == 3:
            self.parse_assignment()
        
        elif self.has_keyword('comment') and len(self.words) > 1:
            self.parse_comment()
        
        elif self.has_keyword('fragment') and len(self.words) == 2:
            self.parse_fragment()

        elif self.has_keyword('object') and len(self.words) == 3:
            self.parse_object()
        
        elif self.has_keyword('print') and len(self.words) > 1:
            self.parse_print()
        
        elif self.has_keyword('return') and len(self.words) > 1:
            self.parse_return()
        
        elif self.has_keyword('statement') and len(self.words) > 1:
            self.parse_statement(self.depth+1)
         
        elif self.has_keyword('variable') and len(self.words) == 3:
            self.parse_variable()
        
        else:
            self.fail_to_recognize_line()

