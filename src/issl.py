#!/usr/bin/python3

from antlr4 import *
from antlr_python.ISSLLexer import ISSLLexer
from antlr_python.ISSLParser import ISSLParser

from SymbolTableGenerator import SymbolTableGenerator
from CodeGen import CodeGen
import sys
import os

#from antlr_python.ISSLParser import ISSLParser
#from antlr_python.ISSLListener import ISSLListener

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

    # Build Symbol Table
    symbolTableGenerator = SymbolTableGenerator(parser)
    symbolTableGenerator.visit(tree)
    symbolTable = symbolTableGenerator.symbolTable

    # TODO: Type Check

    # CodeGen
    codeGen = CodeGen(parser, symbolTable)
    #code = codeGen.visit(tree, symbolTable)



if __name__ == "__main__":
    # execute only if run as a script
    main()
