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

class BusNode():
    def __init__(self, name, channels):
        self.name = name
        self.channels = channels

class ChannelNode():
    def __init__(self, type, id):
        self.type = type
        self.id = id


class ClockNode():
    def __init__(self, stages):
        self.stages = stages


class StageNode():
    def __init__(self, id, vars, stats):
        self.id = id
        self.vars = vars
        self.stats = stats

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
    def __init__(self, id, expr):
        self.id = id
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

class InitializerListNode():
    def __init__(self, exprs):
        self.exprs = exprs

class TypeNode():
    def __init__(self, type):
        self.type = type

class DataTypeNode():
    def __init__(self, type, dims):
        self.type = type
        self.dims = dims

    def numDimentions(self):
        return len(self.dims)


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
        print(results)
        exit(0)
        # for i in range(ctx.getChildCount()):
        #     childResult = ctx.getChild(i).accept(self)
        #     results.append(childResult)

        buses = [b for b in results if isinstance(b, BusNode)]
        clock = [c for c in results if isinstance(c, ClockNode)]
        stages = [s for s in results if isinstance(s, StageNode)]
    
        return SpecificationNode(buses, clock, stages) 



    # Visit a parse tree produced by ISSLParser#specs.
    def visitSpecs(self, ctx:ISSLParser.SpecsContext):
        return self.visit(ctx.getChild(0))


    # Visit a parse tree produced by ISSLParser#bus_specification.
    def visitBus_specification(self, ctx:ISSLParser.Bus_specificationContext):
        channels = [self.visit(c) for c in (ctx.channel_specification())]
        return BusNode(ctx.ID().getText(), channels )


    # Visit a parse tree produced by ISSLParser#channel_specification.
    def visitChannel_specification(self, ctx:ISSLParser.Channel_specificationContext):
        type = self.visit(ctx.r_type())
        return ChannelNode(type, ctx.ID().getText())


    # Visit a parse tree produced by ISSLParser#clock_specification.
    def visitClock_specification(self, ctx:ISSLParser.Clock_specificationContext):
        return ClockNode([self.visit(i) for i in ctx.clock_stage()])

    # Visit a parse tree produced by ISSLParser#clock_stage.
    def visitClock_stage(self, ctx:ISSLParser.Clock_stageContext):
        return ctx.ID().getText()


    # Visit a parse tree produced by ISSLParser#stage_specification.
    def visitStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
        id = ctx.ID().getText()

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
        stats = self.visitChildren(ctx)
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
        id = IDNode(ctx.qualified_id().getText())
        return AssignNode(id, expr)


    # Visit a parse tree produced by ISSLParser#varDecl.
    def visitVarDecl(self, ctx:ISSLParser.VarDeclContext):
        datatype = self.visit(ctx.datatype())
        id = IDNode(ctx.ID().getText())
        expr = ValueNode(0)
        if ctx.expr is not None:
            expr = self.visit(ctx.expr()) 

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
        type = self.visit(ctx.r_type())
        array_specifier = None
        if ctx.array_specifier is not None:
            array_specifier = [self.visit(a) for a in ctx.array_specifier()]

        return DataTypeNode(type, array_specifier)


    # Visit a parse tree produced by ISSLParser#r_type.
    def visitR_type(self, ctx:ISSLParser.R_typeContext):
        return TypeNode(ctx.getText())


    # Visit a parse tree produced by ISSLParser#array_specifier.
    def visitArray_specifier(self, ctx:ISSLParser.Array_specifierContext):
        return int(ctx.INT().getText(), base=0)



