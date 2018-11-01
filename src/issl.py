#!/usr/bin/python3

from antlr4 import *
from antlr_python.ISSLLexer import ISSLLexer
from antlr_python.ISSLParser import ISSLParser

# from SymbolValidator import DefPhase, RefPhase
# from CodeGen import generateSMEILCode
from AST import *
from ErrorControl import verifyAST 
from CodeGen import generateSMEILCode

# from CodeGen import CodeGen
import sys
import os
from pprint import pprint


class Jenny(ASTVisitor):
    def visitIDNode(self, node:  IDNode):
        print("Visited IDNode: {0}".format(node.id))


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

    astBuilder = ASTBuilder()
    ast = astBuilder.visit(tree)

    # Check Refs
    ref_errors = verifyAST(ast)
    if len(ref_errors) > 0:
        pprint(ref_errors)
        exit(0)

    # TODO: Type Check

    # Generate code
    code = generateSMEILCode(ast)


    print(code)
  #  exit(0)
  #  # Definition phase 
  #  defs = DefPhase()
  #  walker.walk(defs, tree)
  #  # Reference phase
  #  refs = RefPhase(defs.symbolTable)
  #  walker.walk(refs, tree)

  #  # Type Check
  #  # TODO

  #  # CodeGen
  #  codeGen = CodeGenSMEIL(refs.symbolTable)
  #  print(codeGen.visit(tree))



if __name__ == "__main__":
    # execute only if run as a script
    main()
