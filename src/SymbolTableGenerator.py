from antlr4 import *

import collections
from antlr_python.ISSLParser import ISSLParser
from antlr_python.ISSLListener import ISSLListener
from antlr_python.ISSLVisitor import ISSLVisitor

Bus = collections.namedtuple("Bus", ['name', 'channels'])
Channel = collections.namedtuple("Channel", ['name','type'])
Stage = collections.namedtuple("Stage", ['name', 'vars'])
Var = collections.namedtuple("Var", ['name', 'type'])

class SymbolTableGenerator(ISSLListener):
    # Enter a parse tree produced by ISSLParser#specification.
    def enterSpecification(self, ctx:ISSLParser.SpecificationContext):
        self.symbolTable = []

    # Exit a parse tree produced by ISSLParser#specification.
    def exitSpecification(self, ctx:ISSLParser.SpecificationContext):
        pass

    # Enter a parse tree produced by ISSLParser#bus_specification.
    def enterBus_specification(self, ctx:ISSLParser.Bus_specificationContext):
        self.currentBus = Bus(ctx.ID().getText(),[])

    # Exit a parse tree produced by ISSLParser#bus_specification.
    def exitBus_specification(self, ctx:ISSLParser.Bus_specificationContext):
        self.symbolTable.append(self.currentBus)
        self.currentBus = None

    # Enter a parse tree produced by ISSLParser#channel_specification.
    def enterChannel_specification(self, ctx:ISSLParser.Channel_specificationContext):
        self.currentBus.channels.append(Channel(ctx.ID().getText(), ctx.r_type().getText()))

    # Enter a parse tree produced by ISSLParser#stage_specification.
    def enterStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
        self.currentStage = Stage(ctx.ID().getText(),[])

    # Exit a parse tree produced by ISSLParser#stage_specification.
    def exitStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
        self.symbolTable.append(self.currentStage)
        self.currentStage = None

    # Enter a parse tree produced by ISSLParser#varDecl.
    def enterVarDecl(self, ctx:ISSLParser.VarDeclContext):
        self.currentStage.vars.append(Var(ctx.ID().getText(), 
                                            ctx.r_type().getText()))


class SymbolChecker(ISSLListener):
    # Enter a parse tree produced by ISSLParser#specification.
    def enterSpecification(self, ctx:ISSLParser.SpecificationContext):
        self.symbolTable = []

    # Exit a parse tree produced by ISSLParser#specification.
    def exitSpecification(self, ctx:ISSLParser.SpecificationContext):
        pass

    # Enter a parse tree produced by ISSLParser#bus_specification.
    def enterBus_specification(self, ctx:ISSLParser.Bus_specificationContext):
        self.currentBus = Bus(ctx.ID().getText(),[])

    # Exit a parse tree produced by ISSLParser#bus_specification.
    def exitBus_specification(self, ctx:ISSLParser.Bus_specificationContext):
        self.symbolTable.append(self.currentBus)
        self.currentBus = None

    # Enter a parse tree produced by ISSLParser#channel_specification.
    def enterChannel_specification(self, ctx:ISSLParser.Channel_specificationContext):
        self.currentBus.channels.append(Channel(ctx.ID().getText(), ctx.r_type().getText()))

    # Enter a parse tree produced by ISSLParser#stage_specification.
    def enterStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
        self.symbolTable.append(Stage(ctx.ID().getText()))





#class SymbolTableGenerator(ISSLVisitor):
#    def __init__(self, parser:ISSLParser):
#        self.parser = parser
#
#    # Visit a parse tree produced by ISSLParser#specification.
#    def visitSpecification(self, ctx:ISSLParser.SpecificationContext):
#        return [].append(self.visitChildren(ctx))
#
#
#    def visitBus_specification(self, ctx:ISSLParser.Bus_specificationContext):
#        channels = []
#        print(ctx.getChildren())
#        for i in range(ctx.getChildCount()):
#            c = ctx.getChild(i)
#
#            channels.append(c.accept(self))
#
#        b = Bus(ctx.ID().getText(), channels)
#        print(b)
#        return b
#    def visitChannel_specification(self, ctx:ISSLParser.Channel_specificationContext):
#        return Channel(ctx.ID().getText(), ctx.r_type().getText()) 
#
#