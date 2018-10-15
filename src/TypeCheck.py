from antlr4 import *

from antlr_python.ISSLParser import ISSLParser
from antlr_python.ISSLListener import ISSLListener

class TypeCheck(ISSLListener):
    def __init__(self, parser:ISSLParser):
        self.parser = parser

    