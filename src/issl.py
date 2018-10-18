#!/usr/bin/python3

from antlr4 import *
from antlr_python.ISSLLexer import ISSLLexer
from antlr_python.ISSLParser import ISSLParser

from SymbolValidator import DefPhase, RefPhase

# from CodeGen import CodeGen
import sys
import os
from pprint import pprint


def main():
    if(len(sys.argv) < 2):
        print("USAGE: {0} <input.issl>".format(sys.argv[0]))
        sys.exit(1)

    input_file = sys.argv[1]

    # Check if file exists
    if(os.path.isfile(input_file) == False):
        print("Input file does not exist!")
        sys.exit(1)

    # Create FileStream from file
    input_stream = FileStream(input_file)

    # ---
    lexer = ISSLLexer(input_stream)
    token_stream = CommonTokenStream(lexer)
    parser = ISSLParser(token_stream)
    tree = parser.specification()
    walker = ParseTreeWalker()


    # Definition phase 
    defs = DefPhase()
    walker.walk(defs, tree)
    # Reference phase
    refs = RefPhase(defs.symbolTable)
    walker.walk(refs, tree)


    # Type Check
    # pprint(symbolTableGenerator.symbolTable)
    exit(0) 
    
    # CodeGen
    # codeGen = CodeGen(parser, symbolTable)
    #code = codeGen.visit(tree, symbolTable)



if __name__ == "__main__":
    # execute only if run as a script
    main()
