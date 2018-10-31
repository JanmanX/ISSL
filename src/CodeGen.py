from antlr4 import *

from antlr_python.ISSLParser import ISSLParser
from antlr_python.ISSLListener import ISSLListener
from antlr_python.ISSLVisitor import ISSLVisitor

from AST import *
from SymbolValidator import *
import SMEILSymbols 


def generateTypeCode(datatype : DataTypeNode):
    t = datatype.type
    dims = "".join(["[{0}]".format(d) for d in datatype.dims])
    return dims+t

def generateVarDeclCode(var : VarNode):
    return SMEILSymbols.SME_VARDECL_FMT.format(
                            var.id,
                            generateTypeCode(var.type),
                            "0") 


def generateProcCode(stage : StageNode):
    varDecls = "\n".join([generateVarDeclCode(v) for v in stage.vars])

    return SMEILSymbols.SME_PROC_FMT.format(
           stage.id,
            
    )

        # "in" busses
        parameters_in = ", ".join(["in {0}".format(b) for b in stage.reads])

        # "out" busses
        # Get all busses which have channels with the current process as its
        # driver
        driver_busses = [b.name for b in self.symbolTable
                            if isinstance(b,Bus) and any(c.driver == name for c in b.channels)]
        # Remove duplicates
        driver_busses = list(set(driver_busses))
        parameters_out = " ".join([", out {0}".format(b) for b in driver_busses])
        parameters = ""

        # define vars
        vars_ = "".join([CodeGenSMEIL.generateVarDeclCode(v) for v in stage.vars])

        code = "".join([self.visit(s) for s in ctx.stat()])

        return SMEILSymbols.SME_PROC_FMT.format(
            name,
            parameters,
            vars_, 
            code
        )




def generateChannelCode(channel: Channel):
    return SMEILSymbols.SME_CHANNEL_FMT.format(channel.name, channel.type)



def generateBusCode(bus: Bus):
    channels = ""
    for c in bus.channels:
        channels += generateChannelCode(c)

    exposed = (SMEILSymbols.SME_BUS_MODIFIER_EXPOSED 
                if bus.exposed 
                else SMEILSymbols.SME_BUS_MODIFIER_NONE)
    return SMEILSymbols.SME_BUS_FMT.format(exposed, bus.name, channels)


def generateNetworkCode(name, busses, procs):
    return ""
#    busses = "".join([CodeGenSMEIL.generateBusCode(b) for b in busses])
#    return SMEILSymbols.SME_NETWORK_FMT.format(name, busses, "")



def generateSMEILCode(ast : SpecificationNode):
    procs = "\n".join([generateProcCode(s) for s in ast.stages])
    network = generateNetworkCode("main", ast.buses, ast.clock.stages)

    return "{0}\n\n{1}".format(
        procs,
        network
    )


class CodeGenSMEIL(ISSLVisitor):

    def __init__(self, symbolTable):
        self.symbolTable = symbolTable

    def defaultResult(self):
        return ""

    def aggregateResult(self, aggregate, nextResult):
        return aggregate + nextResult


    # Visit a parse tree produced by ISSLParser#specification.
    def visitSpecification(self, ctx:ISSLParser.SpecificationContext):
        procs = self.visitChildren(ctx)

        busses = [b for b in self.symbolTable if isinstance(b, Bus)]
        network = CodeGenSMEIL.generateNetworkCode("main", busses, None)

        return procs + "\n\n" + network 

    # Visit a parse tree produced by ISSLParser#specs.
    def visitSpecs(self, ctx:ISSLParser.SpecsContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by ISSLParser#bus_specification.
    def visitBus_specification(self, ctx:ISSLParser.Bus_specificationContext):
        return self.defaultResult()

    # Visit a parse tree produced by ISSLParser#clock_specification.
    def visitClock_specification(self, ctx:ISSLParser.Clock_specificationContext):
        return self.defaultResult()

    # Visit a parse tree produced by ISSLParser#clock_stage.
    def visitClock_stage(self, ctx:ISSLParser.Clock_stageContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by ISSLParser#stage_specification.
    def visitStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
        name = ctx.ID().getText()
        stage = getStageFromSymbolTable(name, self.symbolTable)

        # "in" busses
        parameters_in = ", ".join(["in {0}".format(b) for b in stage.reads])

        # "out" busses
        # Get all busses which have channels with the current process as its
        # driver
        driver_busses = [b.name for b in self.symbolTable
                            if isinstance(b,Bus) and any(c.driver == name for c in b.channels)]
        # Remove duplicates
        driver_busses = list(set(driver_busses))
        parameters_out = " ".join([", out {0}".format(b) for b in driver_busses])
        parameters = ""

        # define vars
        vars_ = "".join([CodeGenSMEIL.generateVarDeclCode(v) for v in stage.vars])

        code = "".join([self.visit(s) for s in ctx.stat()])

        return SMEILSymbols.SME_PROC_FMT.format(
            name,
            parameters,
            vars_, 
            code
        )


    # Visit a parse tree produced by ISSLParser#for.
    def visitFor(self, ctx:ISSLParser.ForContext):
        qualified_id = self.visit(ctx.qualified_id())
        from_ = self.visit(ctx.from_())
        to = self.visit(ctx.to())
        stat = self.visit(ctx.stat())
        return SMEILSymbols.SME_FOR_FMT.format(
            qualified_id,
            from_,
            to,
            stat
        )


    # Visit a parse tree produced by ISSLParser#if.
    def visitIf(self, ctx:ISSLParser.IfContext):
        expr = self.visit(ctx.expr())
        stat = self.visit(ctx.stat())
        return SMEILSymbols.SME_IF_FMT.format(
            expr,
            stat
        )

    # Visit a parse tree produced by ISSLParser#block.
    def visitBlock(self, ctx:ISSLParser.BlockContext):
        return "{\n " + "\n".join([self.visit(s) for s in ctx.stat()]) + "\n}\n"


    # Visit a parse tree produced by ISSLParser#assign.
    def visitAssign(self, ctx:ISSLParser.AssignContext):
        left = self.visit(ctx.qualified_id())
        expr = self.visit(ctx.expr())
        return left + " = " + expr + ";\n"


    # Visit a parse tree produced by ISSLParser#varDecl.
    def visitVarDecl(self, ctx:ISSLParser.VarDeclContext):
        left = ctx.ID().getText()
        expr = self.visit(ctx.expr())
        return left + " = " + expr + ";\n"


    # Visit a parse tree produced by ISSLParser#parens.
    def visitParens(self, ctx:ISSLParser.ParensContext):
        return "(" + self.visit(ctx.expr()) + ")"


    # Visit a parse tree produced by ISSLParser#MulDiv.
    def visitMulDiv(self, ctx:ISSLParser.MulDivContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = (SMEILSymbols.OP_MUL
                if ctx.op.type == ISSLParser.OP_MUL
                else SMEILSymbols.OP_DIV)  
        return left + op + right 
 
    # Visit a parse tree produced by ISSLParser#AddSub.
    def visitAddSub(self, ctx:ISSLParser.AddSubContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = (SMEILSymbols.OP_ADD 
                if ctx.op.type == ISSLParser.OP_ADD
                else SMEILSymbols.OP_SUB)  
        return left + op + right 

    # Visit a parse tree produced by ISSLParser#EqNeq.
    def visitEqNeq(self, ctx:ISSLParser.EqNeqContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = (SMEILSymbols.OP_EQ
                if ctx.op.type == ISSLParser.OP_EQ
                else SMEILSymbols.OP_NEQ)  
        return left + op + right 

    # Visit a parse tree produced by ISSLParser#id.
    def visitId(self, ctx:ISSLParser.IdContext):
        return ctx.getText()

    # Visit a parse tree produced by ISSLParser#int.
    def visitInt(self, ctx:ISSLParser.IntContext):
        return ctx.getText()

    # Visit a parse tree produced by ISSLParser#array.
#    def visitArray(self, ctx:ISSLParser.ArrayContext):
#        return "[" + ",".join(self.visitChildren(ctx)) + "]"


    # Visit a parse tree produced by ISSLParser#qualified_id.
    def visitQualified_id(self, ctx:ISSLParser.Qualified_idContext):
        return ctx.getText()




#class CodeGenSMEIL(ISSLListener):
#    # CodeGens
#    @staticmethod
#    def generateProcCode(name, vars, bus, code):
#        pass
#
#    @staticmethod
#    def generateChannelCode(channel: Channel):
#        return SME_CHANNEL_FMT.format(channel.name, channel.type)
#
#    @staticmethod
#    def generateBusCode(bus: Bus):
#        channels = ""
#        for c in bus.channels:
#            channels += CodeGenSMEIL.generateChannelCode(c)
#
#        return SME_BUS_FMT.format(bus.name, channels)
#
#    @staticmethod
#    def generateNetworkCode(name, busses, procs):
#        busses = "\n".join([CodeGenSMEIL.generateBusCode(b) for b in busses])
#        return SME_NETWORK_FMT.format(name, busses, "")
#
#    def __init__(self, symbolTable):
#        self.symbolTable = symbolTable
#        self.code = ""
#        self.procs = ""
#        self.network = ""
#
#    # Enter a parse tree produced by ISSLParser#specification.
#    def enterSpecification(self, ctx:ISSLParser.SpecificationContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#specification.
#    def exitSpecification(self, ctx:ISSLParser.SpecificationContext):
#        busses = [b for b in self.symbolTable if isinstance(b, Bus)]
#        self.network = CodeGenSMEIL.generateNetworkCode("main", busses, None)
#        self.code = self.procs + self.network
#
#
#    # Enter a parse tree produced by ISSLParser#specs.
#    def enterSpecs(self, ctx:ISSLParser.SpecsContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#specs.
#    def exitSpecs(self, ctx:ISSLParser.SpecsContext):
#        pass
#
#    # Enter a parse tree produced by ISSLParser#stage_specification.
#    def enterStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
#        name = ctx.ID().getText()
#        stage = getStageFromSymbolTable(name, self.symbolTable)
#
#        # "in" busses
#        parameters = ", ".join(["in {0}".format(b) for b in stage.reads])
#
#        # "out" busses
#        # Get all busses which have channels with the current process as its
#        # driver
#        driver_busses = [b.name for b in self.symbolTable
#                            if isinstance(b,Bus) and any(c.driver == name for c in b.channels)]
#        # Remove duplicates
#        driver_busses = list(set(driver_busses))
#        parameters += " ".join([", out {0}".format(b) for b in driver_busses])
#        self.procs += SME_PROC_PROLOGUE_FMT.format(name, parameters)
#
#
#    # Exit a parse tree produced by ISSLParser#stage_specification.
#    def exitStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
#        self.procs += "} \n\n"
#
#
#    # Enter a parse tree produced by ISSLParser#for.
#    def enterFor(self, ctx:ISSLParser.ForContext):
#
#        pass
#
#    # Exit a parse tree produced by ISSLParser#for.
#    def exitFor(self, ctx:ISSLParser.ForContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#if.
#    def enterIf(self, ctx:ISSLParser.IfContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#if.
#    def exitIf(self, ctx:ISSLParser.IfContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#block.
#    def enterBlock(self, ctx:ISSLParser.BlockContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#block.
#    def exitBlock(self, ctx:ISSLParser.BlockContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#assign.
#    def enterAssign(self, ctx:ISSLParser.AssignContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#assign.
#    def exitAssign(self, ctx:ISSLParser.AssignContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#varDecl.
#    def enterVarDecl(self, ctx:ISSLParser.VarDeclContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#varDecl.
#    def exitVarDecl(self, ctx:ISSLParser.VarDeclContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#parens.
#    def enterParens(self, ctx:ISSLParser.ParensContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#parens.
#    def exitParens(self, ctx:ISSLParser.ParensContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#MulDiv.
#    def enterMulDiv(self, ctx:ISSLParser.MulDivContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#MulDiv.
#    def exitMulDiv(self, ctx:ISSLParser.MulDivContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#AddSub.
#    def enterAddSub(self, ctx:ISSLParser.AddSubContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#AddSub.
#    def exitAddSub(self, ctx:ISSLParser.AddSubContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#id.
#    def enterId(self, ctx:ISSLParser.IdContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#id.
#    def exitId(self, ctx:ISSLParser.IdContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#int.
#    def enterInt(self, ctx:ISSLParser.IntContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#int.
#    def exitInt(self, ctx:ISSLParser.IntContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#EqNeq.
#    def enterEqNeq(self, ctx:ISSLParser.EqNeqContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#EqNeq.
#    def exitEqNeq(self, ctx:ISSLParser.EqNeqContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#qualified_id.
#    def enterQualified_id(self, ctx:ISSLParser.Qualified_idContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#qualified_id.
#    def exitQualified_id(self, ctx:ISSLParser.Qualified_idContext):
#        pass
#
#
#    # Enter a parse tree produced by ISSLParser#r_type.
#    def enterR_type(self, ctx:ISSLParser.R_typeContext):
#        pass
#
#    # Exit a parse tree produced by ISSLParser#r_type.
#    def exitR_type(self, ctx:ISSLParser.R_typeContext):
#        pass


