"""
	Christina Trotter
	5/27/19
	Python 3.6.2
"""

import os.path as op, re, sys, traceback
from ijpb import RecognitionError
import cps

""" The base line parser that contains the keyword methods every custom parser will need """  
class LineParser:
    def __init__(self, context):
        self.context = context
        self.line = ''
        self.words = []
    
    #functions recycled from assignment 3
    def parse(self, s):
        self.line = self.remove_comment(s).strip()
        if not self.is_blank_line():
            self.words = self.lex_words()
            try:
                self.do_parse()
            except Exception as e:
                raise RecognitionError('\n..unrecognized line "{0}" skipped..'.format(e))
        return
    
    #implemented in children classes
    def do_parse(self):
        pass
    
    #split line into tokens
    def lex_words(self):
        return self.line.split()

    #check is line is only one specific keyword
    def has_only_word(self, word):
        if self.words[0] == word:
            if len(self.words) != 1:
                self.fail_to_recognize_line()
            return True
        else:
            return False
    
    #check if line has specific keyword
    def has_keyword(self, keyword):
        return keyword == self.words[0]

    #raise error if line is unparsable
    def fail_to_recognize_line(self):
        raise RecognitionError(self.line)

    #return to parser needed for parent code block of the previously finished code
    def return_to_upper_level(self,parser):
        self.context.set_line_parser(parser)
        return

    #check if line is blank
    def is_blank_line(self):
        if self.line in ['\n','\r\n'] or self.line.isspace() or len(self.line) == 0:
            return True
        return False

    #remove comments from line
    def remove_comment(self, line):
        return re.sub(r'^\#.*\n?', '', line)
    
    #parse methods for each JDSL keyword
    def parse_assignment(self):
        self.context.trace('\n..parsing assignment..')
        self.context.add_assignment(self.words[1], self.words[2])
                
    def parse_class(self):
        self.context.trace('\n..parsing class..\n\n..defining class {0}..'.format(self.words[1]))
        self.context.add_class(self.words[1])
        self.context.set_line_parser(cps.ClassParser(self.context))
    
    def parse_comment(self):
        self.context.trace('\n..parsing comment..')
        self.context.add_comment(self.words[1:])
    
    def parse_fragment(self):
        self.context.trace('\n..parsing fragment..')
        self.context.add_fragment(self.words[1])

    def parse_header(self):
        self.context.trace('\n..parsing header..')
        self.context.add_header()
        self.context.set_line_parser(cps.HeaderParser(self.context))
    
    def parse_header_line(self):
        self.context.trace('\n..parsing header line {0}..'.format(self.words[0]))
        self.context.add_content(self.words[0],self.words[1:])
    
    def parse_import(self):
        self.context.trace('\n..parsing {0} import..'.format(self.words[1]))
        self.context.add_import(self.words[1])
    
    def parse_method(self):
        self.context.trace('\n..parsing method {0}..'.format(self.words[1]))
        if len(self.words) == 2:
            self.context.add_method(self.words[1])
        elif len(self.words) == 3:            
            self.context.add_method(self.words[1],self.words[2])
        else:
            self.context.add_method(self.words[1], self.words[2], self.words[3:])
        self.context.set_line_parser(cps.MethodParser(self.context))
    
    def parse_object(self):
        self.context.trace('\n..parsing object declaration..')
        self.context.add_object(self.words[2], self.words[1])
    
    def parse_print(self):
        self.context.trace('\n..parsing print statment..')
        self.context.add_print(self.words[1:])
    
    def parse_program(self):
        self.context.trace('\n..parsing program {0}..'.format(self.words[1]))
        self.context.trace('\n..defining program {0}..'.format(self.words[1]))
        self.context.prime_program(self.words[1])
        self.context.set_line_parser(cps.ProgramParser(self.context))
    
    def parse_return(self):
        self.context.trace('\n..parsing return statement..')
        self.context.add_return(self.words[1:])
    
    def parse_statement(self,depth = 0):
        self.context.trace('\n..parsing {0} statement..'.format(self.words[1]))       
        if len(self.words) == 2:
            self.context.add_statement(self.words[1])        
        elif len(self.words) > 2:
            self.context.add_statement(self.words[1],self.words[2:])
        self.context.set_line_parser(cps.StatementParser(self.context,depth))
    
    def parse_variable(self):
        self.context.trace('\n..parsing variable declaration..')
        self.context.add_variable(self.words[2], self.words[1])
