from antlr4 import *

from antlr_python.ISSLParser import ISSLParser
from antlr_python.ISSLListener import ISSLListener
from antlr_python.ISSLVisitor import ISSLVisitor

from enum import Enum


class SpecificationNode():
    def __init__(self, buses, clock, stages):
        self.buses = buses
        self.clock = clock
        self.stages = stages

    def __repr__(self):
        return "Specification:\n{0}\n{1}\n{2}".format(
            self.clock, self.buses, self.stages)


    def getBus(self, busName):
        for b in self.buses:
            if b.name == busName:
                return b
        return None



class BusNode():
    def __init__(self, name, channels, driver=None):
        self.name = name
        self.channels = channels
        self.driver = driver
    def __repr__(self):
        return "bus(name:{0}, channels:{1}, driver:{2})".format(
            self.name, 
            self.channels,
            self.driver)

class ChannelNode():
    def __init__(self, type, id):
        self.type = type
        self.id = id
    def __repr__(self):
        return "channel(id:{0}, type:{1})".format(self.id, self.type)


class ClockNode():
    def __init__(self, stages):
        self.stages = stages
    def __repr__(self):
        return "clock:{0}".format(self.stages)

class StageNode():
    def __init__(self, idNode, vars, stats):
        self.idNode = idNode
        self.vars = vars
        self.stats = stats

    # Returns a list of buses being written to
    def busesWrittenTo(self):
        buses = []
        for stat in self.stats:
            if isinstance(stat, AssignNode):
                if '.' in stat.id:
                    buses.append(stat.id.split('.')[0]) # append bus name to list
        return buses


class ForNode():
    def __init__(self, iteratorId, fromExpr, toExpr, stat):
        self.iteratorId = iteratorId
        self.fromExpr = fromExpr
        self.toExpr = toExpr
        self.stat = stat

class IfNode():
    def __init__(self, expr, stat):
        self.expr = expr
        self.stat = stat

class BlockNode():
    def __init__(self, stats, vars):
        self.vars = vars
        self.stats = stats

class AssignNode():
    def __init__(self, idNode, expr):
        self.idNode = idNode
        self.expr = expr

class VarNode():
    def __init__(self, id, type):
        self.id = id
        self.type = type

# unused ?
class VarDeclNode():
    def __init__(self, type, id, expr):
        self.type = type
        self.id = id
        self.expr = expr

class InfixExprNode():
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right

class IDNode():
    def __init__(self, id):
        self.id = id

    def __repr__(self):
        return self.id

class InitializerListNode():
    def __init__(self, exprs):
        self.exprs = exprs

class DataTypeNode():
    def __init__(self, type, dims):
        self.type = type
        self.dims = dims # list of sizes of each dimension

    def numDimentions(self):
        if self.dims is None:
            return 0
        return len(self.dims)

    def __repr__(self):
        if self.dims is None:
            return self.type
        return "{0}{1}".format(
            self.type,
            "".join(["[{0}]".format(d) for d in self.dims])
        )



class ValueNode():
    def __init__(self, value):
        self.value = value

class Operators(Enum):
    MUL = 1
    DIV = 2
    ADD = 3
    SUB = 4
    EQ = 5
    NEQ = 6



class ASTVisitor():
    def visit(self, node):
        if(isinstance(node, SpecificationNode)): self.visitSpecificationNode(node)
        elif(isinstance(node, BusNode)): self.visitBusNode(node)
        elif(isinstance(node, ChannelNode)): self.visitChannelNode(node) 
        elif(isinstance(node, ClockNode)): self.visitClockNode(node)
        elif(isinstance(node, StageNode)): self.visitStageNode(node)
        elif(isinstance(node, ForNode)): self.visitForNode(node)
        elif(isinstance(node, IfNode)): self.visitIfNode(node)
        elif(isinstance(node, BlockNode)): self.visitBlockNode(node)
        elif(isinstance(node, AssignNode)): self.visitAssignNode(node)
        elif(isinstance(node, VarNode)): self.visitVarNode(node)
        elif(isinstance(node, VarDeclNode)): self.visitVarDeclNode(node)
        elif(isinstance(node, InfixExprNode)): self.visitInfixExprNode(node)
        elif(isinstance(node, IDNode)): self.visitIDNode(node)
        elif(isinstance(node, InitializerListNode)): self.visitInitializerListNode(node)
        elif(isinstance(node, DataTypeNode)): self.visitDatatypeNode(node)
        elif(isinstance(node, ValueNode)): self.visitValueNode(node)
        else: print(node); raise TypeError("Unknown node type: {0}".format(type(node)))



    def  visitSpecificationNode(self, node : SpecificationNode):
        for b in node.buses:
            self.visit( b)

        self.visit(node.clock)

        for s in node.stages:
            self.visit(s)  


    def visitBusNode(self, node : BusNode):
        self.visit(node.name)
        for c in node.channels:
            self.visit(c)
    

    def visitChannelNode(self, node : ChannelNode):
        self.visit(node.id)
        self.visit(node.type)

    def visitClockNode(self, node : ClockNode):
        for s in node.stages:
            self.visit(s)

    def visitStageNode(self, node : StageNode):
        self.visit(node.id)
        for v in node.vars:
            self.visit(v)
        for stat in node.stats:
            self.visit(stat)

    def visitForNode(self, node : ForNode):
        self.visit(node.iteratorId)
        self.visit(node.fromExpr)
        self.visit(node.toExpr)
        self.visit(node.stat)

    def visitIfNode(self, node : IfNode):
        self.visit(node.expr)
        self.visit(node.stat)

    def visitBlockNode(self, node : BlockNode):
        for v in node.vars:
            self.visit(v)

        for stat in node.stats:
            self.visit(stat)

    def visitAssignNode(self, node : AssignNode):
        self.visit(node.id)
        self.visit(node.expr)

    def visitVarNode(self, node : VarNode):
        self.visit(node.id)
        self.visit(node.type)

    def visitVarDeclNode(self, node : VarDeclNode):
        self.visit(node.type)
        self.visit(node.id)
        self.visit(node.expr)

    def visitInfixExprNode(self, node : InfixExprNode):
        self.visit(node.left)
        self.visit(node.right)

    def visitIDNode(self, node : IDNode):
        pass

    def visitInitializerListNode(self, node : InitializerListNode):
        pass
    
    def visitDatatypeNode(self, node : DataTypeNode):
        pass

    def visitValueNode(self, node : ValueNode):
        pass


class ASTBuilder(ISSLVisitor):
    # default result of a .visitChildren(...)
    def defaultResult(self):
        return []

    def aggregateResult(self, aggregate, nextResult):
        aggregate.append(nextResult)
        return aggregate

    # Visit a parse tree produced by ISSLParser#specification.
    def visitSpecification(self, ctx:ISSLParser.SpecificationContext):
        results = self.visitChildren(ctx)
        # for i in range(ctx.getChildCount()):
        #     childResult = ctx.getChild(i).accept(self)
        #     results.append(childResult)

        buses = [b for b in results if isinstance(b, BusNode)]
        clock = next(c for c in results if isinstance(c, ClockNode)) # only 1 clock
        stages = [s for s in results if isinstance(s, StageNode)]
    
        return SpecificationNode(buses, clock, stages) 



    # Visit a parse tree produced by ISSLParser#specs.
    def visitSpecs(self, ctx:ISSLParser.SpecsContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by ISSLParser#bus_specification.
    def visitBus_specification(self, ctx:ISSLParser.Bus_specificationContext):
        channels = [self.visit(c) for c in (ctx.channel_specification())]
        id = IDNode(ctx.ID().getText())
        return BusNode(id, channels)


    # Visit a parse tree produced by ISSLParser#channel_specification.
    def visitChannel_specification(self, ctx:ISSLParser.Channel_specificationContext):
        type = self.visit(ctx.r_type())
        print(type)
        id = IDNode(ctx.ID().getText())
        return ChannelNode(type, id)


    # Visit a parse tree produced by ISSLParser#clock_specification.
    def visitClock_specification(self, ctx:ISSLParser.Clock_specificationContext):
        return ClockNode([self.visit(i) for i in ctx.clock_stage()])

    # Visit a parse tree produced by ISSLParser#clock_stage.
    def visitClock_stage(self, ctx:ISSLParser.Clock_stageContext):
        return IDNode(ctx.ID().getText())


    # Visit a parse tree produced by ISSLParser#stage_specification.
    def visitStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
        id = IDNode(ctx.ID().getText())

        stats = [self.visit(s) for s in ctx.stat()]
        stats_modified = []
        vars = []
        for stat in stats:
            if isinstance(stat, VarDeclNode):
                vars.append(VarNode(stat.id, stat.type))
                stats_modified.append(AssignNode(stat.id, stat.expr))
            else:
                stats_modified.append(stat)

        return StageNode(id, vars, stats_modified)


    # Visit a parse tree produced by ISSLParser#for.
    def visitFor(self, ctx:ISSLParser.ForContext):
        iterator = self.visit(ctx.qualified_id())
        fromExpr = self.visit(ctx.from_())
        toExpr = self.visit(ctx.to())
        stat = self.visit(ctx.stat())
        return ForNode(iter, fromExpr, toExpr, stat)


    # Visit a parse tree produced by ISSLParser#if.
    def visitIf(self, ctx:ISSLParser.IfContext):
        expr = self.visit(ctx.expr())
        stat = self.visit(ctx.stat())
        return IfNode(expr, stat)


    # Visit a parse tree produced by ISSLParser#block.
    def visitBlock(self, ctx:ISSLParser.BlockContext):
        stats = [self.visit(s) for s in ctx.stat()]
        stats_modified = []
        vars = []
        for stat in stats:
            if isinstance(stat, VarDeclNode):
                vars.append(VarNode(stat.id, stat.type))
                stats_modified.append(AssignNode(stat.id, stat.expr))
            else:
                stats_modified.append(stat)

        return BlockNode(stats_modified, vars)


    # Visit a parse tree produced by ISSLParser#assign.
    def visitAssign(self, ctx:ISSLParser.AssignContext):
        expr = self.visit(ctx.expr())
        idStr = ctx.qualified_id().getText()
        id = IDNode(idStr)

        return AssignNode(id, expr)


    # Visit a parse tree produced by ISSLParser#varDecl.
    def visitVarDecl(self, ctx:ISSLParser.VarDeclContext):
        datatype = self.visit(ctx.datatype())
        id = IDNode(ctx.ID().getText())
        expr = ValueNode(0)
        if ctx.expr is not None:
            expr = self.visit(ctx.expr()) 

        print(datatype)
        return VarDeclNode(datatype, id, expr)


    # Visit a parse tree produced by ISSLParser#parens.
    def visitParens(self, ctx:ISSLParser.ParensContext):
        return self.visit(ctx.expr())

    # Visit a parse tree produced by ISSLParser#initializerList.
    def visitInitializerList(self, ctx:ISSLParser.InitializerListContext):
        exprs = self.visitChildren(ctx)
        return InitializerListNode(exprs)


    # Visit a parse tree produced by ISSLParser#MulDiv.
    def visitMulDiv(self, ctx:ISSLParser.MulDivContext):
        left = self.visit(ctx.left())
        right = self.visit(ctx.right())
        op = (Operators.MUL
                if ctx.op.type == ISSLParser.OP_MUL
                else Operators.DIV)  
 
        return InfixExprNode(op, left, right)


    # Visit a parse tree produced by ISSLParser#AddSub.
    def visitAddSub(self, ctx:ISSLParser.AddSubContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = (Operators.ADD
                if ctx.op.type == ISSLParser.OP_ADD
                else Operators.SUB)  
 
        return InfixExprNode(op, left, right)



    # Visit a parse tree produced by ISSLParser#id.
    def visitId(self, ctx:ISSLParser.IdContext):
        return IDNode(ctx.qualified_id().getText())


    # Visit a parse tree produced by ISSLParser#int.
    def visitInt(self, ctx:ISSLParser.IntContext):
        return ValueNode(ctx.INT().getText())


    # Visit a parse tree produced by ISSLParser#EqNeq.
    def visitEqNeq(self, ctx:ISSLParser.EqNeqContext):
        left = self.visit(ctx.left)
        right = self.visit(ctx.right)
        op = (Operators.EQ
                if ctx.op.type == ISSLParser.OP_EQ
                else Operators.NEQ)  
 
        return InfixExprNode(op, left, right)


    # Visit a parse tree produced by ISSLParser#qualified_id.
    def visitQualified_id(self, ctx:ISSLParser.Qualified_idContext):
        return IDNode(ctx.getText())


    # Visit a parse tree produced by ISSLParser#datatype.
    def visitDatatype(self, ctx:ISSLParser.DatatypeContext):
        type = ctx.r_type().getText()
        array_specifier = None
        if len(ctx.array_specifier()) > 0:
            array_specifier = [self.visit(a) for a in ctx.array_specifier()]

        return DataTypeNode(type, array_specifier)


    # Visit a parse tree produced by ISSLParser#r_type.
    def visitR_type(self, ctx:ISSLParser.R_typeContext):
        return DataTypeNode(ctx.getText(),None)


    # Visit a parse tree produced by ISSLParser#array_specifier.
    def visitArray_specifier(self, ctx:ISSLParser.Array_specifierContext):
        size = "0"
        if ctx.INT is not None:
            size = ctx.INT().getText()
        return int(size, base=0)
