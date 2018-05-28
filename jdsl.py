"""
	Christina Trotter
	5/27/19
	Python 3.6.2
	
	This is a delimiter directed parser

    Notes: run this file
"""
import os.path as op, re, sys, traceback
from ijpb import IJPB
from cps import TLLParser
""" Java Program Parser Object """
class JVP:
    __instance = None
    def __new__(cls, filename, trace):
        if cls.__instance is None:
            cls.__instance = object.__new__(cls)
            jdsl = None
            try:
                jdsl = open(filename, 'r+')
            except Exception as e:
                print(str(e))
            cls.__instance.loader = JVParser(jdsl) 
            cls.__instance.loader.trace('\n\nloaded file {0}'.format(filename))
            if trace == 'N':
                cls.__instance.loader.disable_trace()
            cls.__instance.loader.run()
            cls.__instance.program = cls.__instance.loader.get_program()
            return cls.__instance.program

""" Java Program Parser that inherits from the Icremental Java Program Builder """
class JVParser(IJPB):
    def __init__(self, input):
        IJPB.__init__(self)
        self.input = input
        self.line_parser = None
    
    def run(self):
        self.set_line_parser(TLLParser(self))
        try:
            for line in self.input:
                self.line_parser.parse(line)
        except Exception as e:
            print(str(e))
        self.finish_program()
        return

    def set_line_parser(self, line_parser):
        self.line_parser = line_parser
        return

""" JDSL Object, where the program begins and receives user input """
class JDSL:
    __instance = None
    def __new__(cls):
        if cls.__instance is None:
            filename, trace = cls.get_user_input()
            cls.__instance = object.__new__(cls)
            cls.__instance.program = JVP(filename,trace)
        return cls.__instance
    @classmethod
    def get_user_input(cls):
        filename, trace = '',None
        while filename[-5:] != '.jdsl' or not op.isfile(filename):
            filename = input('enter a valid .jdsl filename: ')
        print('\ndo you want to enable tracing?')
        while trace not in ['Y','y','N','n']:
            trace = input('\nenter Y or N: ')
        return filename, trace


if __name__ == '__main__':
    try:
        print('\nSimple Java Program Builder\n')
        JDSL()
        print('\nGoodbye!\n')
    except Exception as e:
        print(str(e))
        _, _, tb = sys.exc_info()
        print(traceback.format_list(traceback.extract_tb(tb)[-1:])[-1])