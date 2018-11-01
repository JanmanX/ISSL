from antlr4 import *

import collections
from antlr_python.ISSLParser import ISSLParser
from antlr_python.ISSLListener import ISSLListener
from antlr_python.ISSLVisitor import ISSLVisitor
from AST import *

from pprint import pprint

def verifyAST(ast : SpecificationNode):
    if not isinstance(ast, SpecificationNode):
        raise TypeError("VerifyAST can only be called with the tree root (SpecificationNode)")
    return checkSymbolRefs(ast)


### Symbol Reference check
def checkSymbolRefs(ast: SpecificationNode):
    errors = []

    # Check clock
    errors += checkClockRefs(ast)

    # Check every stage
    errors += checkStageRefs(ast)

    return errors

def checkClockRefs(ast: SpecificationNode):
    errors = []
    for idNode in ast.clock.stages:
        if ast.getStage(idNode.id) is None:
            errors.append("[MINOR]: Stage <{0}> is not defined!".format(
                idNode.id))

    return errors


def checkStageRefs(ast: SpecificationNode):
    # Mark Bus Drivers, collect errors
    busDriverErrors = ASTMarkBuses(ast).markBusDrivers()

    # Check Refs
    refErrors = ASTCheckRefs(ast).checkRefs()

    # Merge errors and return
    return busDriverErrors + refErrors


# Checks that references exist
class ASTCheckRefs(ASTVisitor):
    def __init__(self, ast : SpecificationNode):
        self.ast = ast

    def checkRefs(self):
        self.errors = []

        # scopes is used as a stack-based symbol table of scopes
        self.scopes = []

        self.visit(self.ast)
        return self.errors

    # visit only IDs in stages, so just visit stages..
    def visitSpecificationNode(self, node : StageNode):
        for s in node.stages:
            self.visit(s)  


    def visitStageNode(self, node : StageNode):
        self.scopes.append(node.vars)

        # Visit only statements
        for stat in node.stats:
            self.visit(stat)

        self.scopes.pop()


    def visitBlockNode(self, node : BlockNode):
        self.scopes.append(node.vars)
        super(ASTCheckRefs, self).visitBlockNode(node)
        self.scopes.pop()


    def visitIDNode(self, node : IDNode):
        # check if bus or var
        if '.' in node.id:  # bus
            busName = node.id.split('.')[0]
            channelName = node.id.split('.')[1]
            bus = self.ast.getBus(busName)

            if bus is None:
                self.errors.append("[CRITICAL]: Bus <{0}> does not exist!".format(
                    busName))
                return 
            
            channel = bus.getChannel(channelName)
            if channel is None:
                self.errors.append("[CRITICAL]: Channel <{0}> in Bus <{1}> does not exist!".format(
                    channelName,
                    busName))
                return

        else:   # var
            # In case of array indexing, remove the brackets
            varName = node.id.split('[', 1)[0]

            # Search through the stack top down (reversed)
            for scope in reversed(self.scopes):
                # Search for variable, return if found
                for var in scope:
                    if var.idNode.id == varName:
                        return

            # var not found, add error
            self.errors.append("[CRITICAL]: Variable <{0}> does not exist!"
                            .format(varName))


class ASTMarkBuses(ASTVisitor):
    def __init__(self, ast):
        if not isinstance(ast, SpecificationNode):
            raise Exception("ASTMarkBuses must be called with a SpecificationNode!")
        self.ast = ast
        self.errors = []

    def markBusDrivers(self):
        super(ASTMarkBuses, self).visit(self.ast)
        return self.errors

    def visitStageNode(self, node : StageNode):
        self.currentStageName = node.idNode.id
        super(ASTMarkBuses, self).visitStageNode(node)
        self.currentStageName = ""
        

    def visitAssignNode(self, node : AssignNode):
        # Check if assign to bus
        if '.' in node.idNode.id:
            busName = node.idNode.id.split('.')[0] # get "bus" part of ID
            bus = self.ast.getBus(busName)

            if bus is None:
                # bus not found. This is handled in the RefPhase, so dont generate
                # another error, just exit.
                return 
            if bus.driver is not None and bus.driver != self.currentStageName:
                self.errors.append("[CRITICAL]: Bus <{0}> has multiple drivers: <{1}>, <{2}>)".format(
                    busName, bus.driver, self.currentStageName))
                return

            # Set driver 
            bus.driver = self.currentStageName 


# class Bus():
#     def __init__(self, name, channels, reads, exposed=False):
#         self.name = name
#         self.channels = channels
#         self.reads = reads
#         self.exposed = exposed
#     def __repr__(self):
#         return ("Bus(name:{0},Channels:{1})"
#                 .format(self.name, self.channels))
# 
# class Channel():
#     def __init__(self, name, _type, driver):
#         self.name = name
#         self.type = _type
#         self.driver = driver
# 
#     def __repr__(self):
#         return "Channel(name:{0}, type:{1}, driver:{2})".format(
#                 self.name, self.type, self.driver)
# 
# 
# class Stage():
#     def __init__(self, name, vars, reads):
#         self.name = name
#         self.vars = vars
#         self.reads = reads # keeps track of which busses are being read
# 
#     def __repr__(self):
#         return "Stage(name:{0}, vars: {1})".format(self.name, self.vars)
# 
# class Var():
#     def __init__(self, name, _type, initValue="0"):
#         self.name = name
#         self.type = _type
#         self.initValue = initValue
#     def __repr__(self):
#         return "Var(name:{0}, type: {1})".format(self.name, self.type)
# 
# 
# 
# class DefPhase(ISSLListener):
#     # Enter a parse tree produced by ISSLParser#specification.
#     def enterSpecification(self, ctx:ISSLParser.SpecificationContext):
#         self.symbolTable = []
# 
#     # Enter a parse tree produced by ISSLParser#bus_specification.
#     def enterBus_specification(self, ctx:ISSLParser.Bus_specificationContext):
#         name = ctx.ID().getText()
#         exposed = True if ctx.modifier is not None else False
# 
#         # Check if Bus name already exists
#         if any(isinstance(b, Bus) and b.name == name for b in self.symbolTable):
#             print("Bus: \"{0}\" already defined!".format(name))
#             return
# 
#         self.currentBus = Bus(name,[],[], exposed)
# 
#     # Exit a parse tree produced by ISSLParser#bus_specification.
#     def exitBus_specification(self, ctx:ISSLParser.Bus_specificationContext):
#         self.symbolTable.append(self.currentBus)
#         self.currentBus = None
# 
#     # Enter a parse tree produced by ISSLParser#channel_specification.
#     def enterChannel_specification(self, ctx:ISSLParser.Channel_specificationContext):
#         name = ctx.ID().getText()
#         r_type = ctx.r_type().getText()
# 
#         # Check if channel name already exists in the current bus
#         if any(c.name == name for c in self.currentBus.channels):
#             print("Channel: \"{0}\" already defined in bus!".format(name))
#             return
# 
#         self.currentBus.channels.append(Channel(name, r_type, None))
# 
#     # Enter a parse tree produced by ISSLParser#stage_specification.
#     def enterStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
#         name = ctx.ID().getText()
# 
#         # Check if Stage name already exists
#         if any(isinstance(s, Stage) and s.name == name for s in self.symbolTable):
#             print("Stage: \"{0}\" already defined!".format(name))
#             return
# 
#         self.currentStage = Stage(name,[],[])
# 
#     # Exit a parse tree produced by ISSLParser#stage_specification.
#     def exitStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
#         self.symbolTable.append(self.currentStage)
#         self.currentStage = None
# 
#     # Enter a parse tree produced by ISSLParser#varDecl.
#     def enterVarDecl(self, ctx:ISSLParser.VarDeclContext):
#         name = ctx.ID().getText()
#         r_type = ctx.r_type().getText()
# 
#         # Check if variable name already in use
#         if any(v.name == name for v in self.currentStage.vars):
#             print("Variable: \"{0}\" already defined in stage!".format(name))
#             return
# 
#         self.currentStage.vars.append(Var(name, r_type))
# 
# 
# class RefPhase(ISSLListener):
#     def __init__(self, symbolTable):
#         self.symbolTable = symbolTable
# 
#     # Enter a parse tree produced by ISSLParser#clock_stage.
#     def enterClock_stage(self, ctx:ISSLParser.Clock_stageContext):
#         name = ctx.ID().getText()
# 
#         # Check if ClockStage exists
#         if not any(isinstance(s, Stage) and s.name == name for s in self.symbolTable):
#             print("Stage: \"{0}\" is not defined!".format(name))
#             return
#         pass
# 
#     # Enter a parse tree produced by ISSLParser#stage_specification.
#     def enterStage_specification(self, ctx:ISSLParser.Stage_specificationContext):
#         name = ctx.ID().getText()
#         self.currentStage = ([s for s in self.symbolTable 
#                             if isinstance(s, Stage) and s.name == name]
#                             [0])
# 
#     # Enter a parse tree produced by ISSLParser#assign.
#     def enterAssign(self, ctx:ISSLParser.AssignContext):
#         qualified_id = ctx.qualified_id().getText()
# 
#         # If write to bus
#         if '.' in qualified_id:
#             bus_name = qualified_id.split('.')[0]
#             channel_name = qualified_id.split('.')[1]
#             bus = getBusFromSymbolTable(bus_name, self.symbolTable)
#             if bus is None:
#                 print("Bus: {0} does not exist!".format(bus_name))
#                 return
# 
#             channel = getChannelFromBus(channel_name, bus)
#             if channel is None:
#                 print("Channel: {0} does not exist in Bus: {1}!"
#                         .format(channel_name,bus_name))
# 
#             # Check for driver already set 
#             if channel.driver is not None and channel.driver != self.currentStage.name:
#                 print("Channel: {0}.{1} already has a driver: {2}"
#                     .format(bus_name, channel_name, channel.driver))
#                 return
# 
#             # Set driver
#             channel.driver = self.currentStage.name
# 
#         else: # if write to local variable
# 
#             # Remove array indexing, if any
#             qualified_id = qualified_id.split('[')[0]
# 
#             if not qualified_id in self.currentStage.vars:
#                 print("Var: {0} not in scope of {1}!".format(
#                     qualified_id,
#                     self.currentStage.name))
#                 return
# 
#     # Enter a parse tree produced by ISSLParser#id.
#     def enterId(self, ctx:ISSLParser.IdContext):
#         qualified_id = ctx.qualified_id().getText()
# 
#         # If this is a read from a bus, add it to the "reads" in the stage
#         if('.' in qualified_id):
#             bus = qualified_id.split('.')[0]
#             self.currentStage.reads.append(bus)
# 
# 
#     # Enter a parse tree produced by ISSLParser#r_type.
#     def enterR_type(self, ctx:ISSLParser.R_typeContext):
#         # TODO: Check size
#         pass
# 
# # Macros
# def getBusFromSymbolTable(name, symtab):
#     return next((b for b in symtab if isinstance(b,Bus) and b.name == name), None)
# 
# def getChannelFromBus(name, bus: Bus):
#     return next((c for c in bus.channels if c.name == name), None)
# 
# def getStageFromSymbolTable(name, symtab):
#     return next((s for s in symtab if isinstance(s,Stage) and s.name == name), None)


