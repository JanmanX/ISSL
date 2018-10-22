from antlr4 import *

from antlr_python.ISSLParser import ISSLParser
from antlr_python.ISSLListener import ISSLListener
from antlr_python.ISSLVisitor import ISSLVisitor

from SymbolValidator import *

SME_PROC_PROLOGUE_FMT = "proc {0} ({1}) {{ \n"

SME_BUS_FMT = """
bus {0} {{
{1}
}}
"""

SME_CHANNEL_FMT = "\t{0}: {1};\n"

SME_NETWORK_FMT = """
network {0}() {{
{1}

{2} 
}}
"""

class CodeGenSMEIL(ISSLListener):
    # CodeGens
    @staticmethod
    def generateProcCode(name, vars, bus, code):
        pass

    @staticmethod
    def generateChannelCode(channel: Channel):
        return SME_CHANNEL_FMT.format(channel.name, channel.type)

    @staticmethod
    def generateBusCode(bus: Bus):
        channels = ""
        for c in bus.channels:
            channels += CodeGenSMEIL.generateChannelCode(c)

        return SME_BUS_FMT.format(bus.name, channels)

    @staticmethod
    def generateNetworkCode(name, busses, procs):
        busses = "\n".join([CodeGenSMEIL.generateBusCode(b) for b in busses])
        return SME_NETWORK_FMT.format(name, busses, "") 

    def __init__(self, symbolTable):
        self.symbolTable = symbolTable
        self.code = ""
        self.procs = ""
        self.network = ""

    # Enter a parse tree produced by ISSLParser#specification.
    def enterSpecification(self, ctx:ISSLParser.SpecificationContext):
        pass

    # Exit a parse tree produced by ISSLParser#specification.
    def exitSpecification(self, ctx:ISSLParser.SpecificationContext):
        busses = [b for b in self.symbolTable if isinstance(b, Bus)]
        self.network = CodeGenSMEIL.generateNetworkCode("main", busses, None) 
        self.code = self.procs + self.network


    # Enter a parse tree produced by ISSLParser#specs.
    def enterSpecs(self, ctx:ISSLParser.SpecsContext):
        pass

    # Exit a parse tree produced by ISSLParser#specs.
    def exitSpecs(self, ctx:ISSLParser.SpecsContext):
        pass

    # Enter a parse tree produced by ISSLParser#stage_specification.
    def enterStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
        name = ctx.ID().getText()
        stage = getStageFromSymbolTable(name, self.symbolTable)
        
        # "in" busses
        parameters = ", ".join(["in {0}".format(b) for b in stage.reads])
        
        # "out" busses
        # Get all busses which have channels with the current process as its 
        # driver
        driver_busses = [b.name for b in self.symbolTable 
                            if isinstance(b,Bus) and any(c.driver == name for c in b.channels)]
        # Remove duplicates
        driver_busses = list(set(driver_busses))
        parameters += " ".join([", out {0}".format(b) for b in driver_busses])
        self.procs += SME_PROC_PROLOGUE_FMT.format(name, parameters)


    # Exit a parse tree produced by ISSLParser#stage_specification.
    def exitStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
        self.procs += "} \n\n"


    # Enter a parse tree produced by ISSLParser#for.
    def enterFor(self, ctx:ISSLParser.ForContext):
        pass

    # Exit a parse tree produced by ISSLParser#for.
    def exitFor(self, ctx:ISSLParser.ForContext):
        pass


    # Enter a parse tree produced by ISSLParser#if.
    def enterIf(self, ctx:ISSLParser.IfContext):
        pass

    # Exit a parse tree produced by ISSLParser#if.
    def exitIf(self, ctx:ISSLParser.IfContext):
        pass


    # Enter a parse tree produced by ISSLParser#block.
    def enterBlock(self, ctx:ISSLParser.BlockContext):
        pass

    # Exit a parse tree produced by ISSLParser#block.
    def exitBlock(self, ctx:ISSLParser.BlockContext):
        pass


    # Enter a parse tree produced by ISSLParser#assign.
    def enterAssign(self, ctx:ISSLParser.AssignContext):
        pass

    # Exit a parse tree produced by ISSLParser#assign.
    def exitAssign(self, ctx:ISSLParser.AssignContext):
        pass


    # Enter a parse tree produced by ISSLParser#varDecl.
    def enterVarDecl(self, ctx:ISSLParser.VarDeclContext):
        pass

    # Exit a parse tree produced by ISSLParser#varDecl.
    def exitVarDecl(self, ctx:ISSLParser.VarDeclContext):
        pass


    # Enter a parse tree produced by ISSLParser#parens.
    def enterParens(self, ctx:ISSLParser.ParensContext):
        pass

    # Exit a parse tree produced by ISSLParser#parens.
    def exitParens(self, ctx:ISSLParser.ParensContext):
        pass


    # Enter a parse tree produced by ISSLParser#MulDiv.
    def enterMulDiv(self, ctx:ISSLParser.MulDivContext):
        pass

    # Exit a parse tree produced by ISSLParser#MulDiv.
    def exitMulDiv(self, ctx:ISSLParser.MulDivContext):
        pass


    # Enter a parse tree produced by ISSLParser#AddSub.
    def enterAddSub(self, ctx:ISSLParser.AddSubContext):
        pass

    # Exit a parse tree produced by ISSLParser#AddSub.
    def exitAddSub(self, ctx:ISSLParser.AddSubContext):
        pass


    # Enter a parse tree produced by ISSLParser#id.
    def enterId(self, ctx:ISSLParser.IdContext):
        pass

    # Exit a parse tree produced by ISSLParser#id.
    def exitId(self, ctx:ISSLParser.IdContext):
        pass


    # Enter a parse tree produced by ISSLParser#int.
    def enterInt(self, ctx:ISSLParser.IntContext):
        pass

    # Exit a parse tree produced by ISSLParser#int.
    def exitInt(self, ctx:ISSLParser.IntContext):
        pass


    # Enter a parse tree produced by ISSLParser#EqNeq.
    def enterEqNeq(self, ctx:ISSLParser.EqNeqContext):
        pass

    # Exit a parse tree produced by ISSLParser#EqNeq.
    def exitEqNeq(self, ctx:ISSLParser.EqNeqContext):
        pass


    # Enter a parse tree produced by ISSLParser#qualified_id.
    def enterQualified_id(self, ctx:ISSLParser.Qualified_idContext):
        pass

    # Exit a parse tree produced by ISSLParser#qualified_id.
    def exitQualified_id(self, ctx:ISSLParser.Qualified_idContext):
        pass


    # Enter a parse tree produced by ISSLParser#r_type.
    def enterR_type(self, ctx:ISSLParser.R_typeContext):
        pass

    # Exit a parse tree produced by ISSLParser#r_type.
    def exitR_type(self, ctx:ISSLParser.R_typeContext):
        pass


