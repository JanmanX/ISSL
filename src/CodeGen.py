from antlr4 import *

from antlr_python.ISSLParser import ISSLParser
from antlr_python.ISSLListener import ISSLListener
from antlr_python.ISSLVisitor import ISSLVisitor

from AST import *
import SMEILSymbols 


def generateTypeCode(datatype : DataTypeNode):
    t = datatype.type
    dims = ""

    if datatype.dims is not None:
        dims = "".join(["[{0}]".format(d) for d in datatype.dims])

    return dims+t

def generateVarDeclCode(var : VarNode):
    return SMEILSymbols.SME_VARDECL_FMT.format(
                            var.idNode.id,
                            generateTypeCode(var.type),
                            "0") 


def generateProcCode(stage : StageNode, buses):
    # "in" busses
    parameters_in = ", ".join(["in {0}".format(b) for b in ASTBusReads().getBusesRead(stage)])

    # "out" busses
    driver_buses = [b.idNode.id for b in buses if b.driver == stage.idNode.id]
    parameters_out = " ".join(", out {0}".format(b) for b in driver_buses)

    # parameters
    parameters = parameters_in + parameters_out

    # vars
    varDecls = "\n".join([generateVarDeclCode(v) for v in stage.vars])

    # code
    code = SMEILStageCodeGenerator().generateStageCode(stage)

    return SMEILSymbols.SME_PROC_FMT.format(
           stage.idNode,
           parameters,
           varDecls,
           code
    )


#def generateChannelCode(channel: Channel):
#    return SMEILSymbols.SME_CHANNEL_FMT.format(channel.name, channel.type)
#
#
#
#def generateBusCode(bus: Bus):
#    channels = ""
#    for c in bus.channels:
#        channels += generateChannelCode(c)
#
#    exposed = (SMEILSymbols.SME_BUS_MODIFIER_EXPOSED 
#                if bus.exposed 
#                else SMEILSymbols.SME_BUS_MODIFIER_NONE)
#    return SMEILSymbols.SME_BUS_FMT.format(exposed, bus.name, channels)
#

def generateNetworkCode(name, busses, procs):
    return ""
#    busses = "".join([CodeGenSMEIL.generateBusCode(b) for b in busses])
#    return SMEILSymbols.SME_NETWORK_FMT.format(name, busses, "")



def generateSMEILCode(ast : SpecificationNode):
    procs = "\n".join([generateProcCode(s, ast.buses) for s in ast.stages])
    network = generateNetworkCode("main", ast.buses, ast.clock.stages)

    return "{0}\n\n{1}".format(
        procs,
        network
    )


class SMEILStageCodeGenerator(ASTVisitor):
    def generateStageCode(self, node : StageNode):
        return self.visit(node) 

    def visit(self, node):
        if(isinstance(node, SpecificationNode)): return self.visitSpecificationNode(node)
        elif(isinstance(node, BusNode)): return self.visitBusNode(node)
        elif(isinstance(node, ChannelNode)): return self.visitChannelNode(node) 
        elif(isinstance(node, ClockNode)): return self.visitClockNode(node)
        elif(isinstance(node, StageNode)): return self.visitStageNode(node)
        elif(isinstance(node, ForNode)): return self.visitForNode(node)
        elif(isinstance(node, IfNode)): return self.visitIfNode(node)
        elif(isinstance(node, BlockNode)): return self.visitBlockNode(node)
        elif(isinstance(node, AssignNode)): return self.visitAssignNode(node)
        elif(isinstance(node, VarNode)): return self.visitVarNode(node)
        elif(isinstance(node, VarDeclNode)): return self.visitVarDeclNode(node)
        elif(isinstance(node, InfixExprNode)): return self.visitInfixExprNode(node)
        elif(isinstance(node, IDNode)): return self.visitIDNode(node)
        elif(isinstance(node, InitializerListNode)): return self.visitInitializerListNode(node)
        elif(isinstance(node, DataTypeNode)): return self.visitDatatypeNode(node)
        elif(isinstance(node, ValueNode)): return self.visitValueNode(node)
        else: print(node); raise TypeError("Unknown node type: {0}".format(type(node)))

        return None


    def visitStageNode(self, node : StageNode):
        return ";\n".join([self.visit(s) for s in node.stats])

    def visitForNode(self, node : ForNode):
        return SMEILSymbols.SME_FOR_FMT.format(
            self.visit(node.iteratorId),
            self.visit(node.fromExpr),
            self.visit(node.toExpr),
            self.visit(node.stat)
        ) 

    def visitIfNode(self, node : IfNode):
        return SMEILSymbols.SME_IF_FMT.format(
            self.visit(node.expr),
            self.visit(node.stat)
        )

    def visitBlockNode(self, node : BlockNode):
        return "{{\n {0} \n}}".format(";\n".join([self.visit(s) for s in node.stats])) 

    def visitAssignNode(self, node : AssignNode):
        return (self.visit(node.idNode) 
                + SMEILSymbols.ASSIGN 
                + self.visit(node.expr))

    def visitInfixExprNode(self, node : InfixExprNode):
        return self.visit(node.left) + node.op + self.visit(node.right)

    def visitIDNode(self, node : IDNode):
        return node.id 

    def visitInitializerListNode(self, node : InitializerListNode):
        return "[ " + ", ".join([self.visit(e) for e in node.exprs]) + "]" 

    def visitValueNode(self, node : ValueNode):
        return str(node.value)






class ASTBusReads(ASTVisitor):
    def getBusesRead(self, stage):
        self.stage = stage
        self.buses = []
        self.visit(self.stage)        
        return set(self.buses)

    def visitIDNode(self, node : IDNode):
        if '.' in node.id:
            busName = node.id.split('.')[0]
            self.buses.append(busName)           

    def visitAssignNode(self, node : AssignNode):
        # We do not want to visit the left side, as we are only interested in
        # reads.
        self.visit(node.expr)


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



