from antlr4 import *

from antlr_python.ISSLParser import ISSLParser
from antlr_python.ISSLListener import ISSLListener
from antlr_python.ISSLVisitor import ISSLVisitor


SME_PROC_ADD = """
proc add (in addBusIn)
    bus addBusOut {
        val: {0} = 0;
    }
{
    addBusOut.val = addBusIn.val1 + addBusIn.val2;
}
"""
SME_PROC_SUB = """
proc sub (in subBusIn)
    bus subBusOut {
        val: {0} = 0;
    }
{
    subBusOut.val = subBusIn.val1 - subBusIn.val2;
}
"""

SME_PROC_IF = """
proc sub (in subBusIn)
    bus subBusOut {
        val: {0} = 0;
    }
{
    subBusOut.val = subBusIn.val1 - subBusIn.val2;
}
"""



SME_MAIN_NETWORK = """
network main() {
   {0} 
}
"""


class CodeGen(ISSLVisitor):
    def __init__(self, parser:ISSLParser, symbolTable):
        self.parser = parser
        self.symbolTable = symbolTable   # [{ID, type, attribute}]

    # Visit a parse tree produced by ISSLParser#specification.
    def visitSpecification(self, ctx:ISSLParser.SpecificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#specs.
    def visitSpecs(self, ctx:ISSLParser.SpecsContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#register_specification.
    def visitRegister_specification(self, ctx:ISSLParser.Register_specificationContext):
       return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#register.
    def visitRegister(self, ctx:ISSLParser.RegisterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#clock_specification.
    def visitClock_specification(self, ctx:ISSLParser.Clock_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#instruction_specification.
    def visitInstruction_specification(self, ctx:ISSLParser.Instruction_specificationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#while.
    def visitWhile(self, ctx:ISSLParser.WhileContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#if.
    def visitIf(self, ctx:ISSLParser.IfContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#block.
    def visitBlock(self, ctx:ISSLParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#assign.
    def visitAssign(self, ctx:ISSLParser.AssignContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#parens.
    def visitParens(self, ctx:ISSLParser.ParensContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#MulDiv.
    def visitMulDiv(self, ctx:ISSLParser.MulDivContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#AddSub.
    def visitAddSub(self, ctx:ISSLParser.AddSubContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#id.
    def visitId(self, ctx:ISSLParser.IdContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#int.
    def visitInt(self, ctx:ISSLParser.IntContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#EqNeq.
    def visitEqNeq(self, ctx:ISSLParser.EqNeqContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#access_specifier.
    def visitAccess_specifier(self, ctx:ISSLParser.Access_specifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#r_type.
    def visitR_type(self, ctx:ISSLParser.R_typeContext):
          return self.visitChildren(ctx)


