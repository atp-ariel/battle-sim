from .context import  *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *


class Type_Builder:

    def __init__(self, context) -> None:
        self.context = context
        self.current_context=self.context

    @visitor(BsFile)
    def visit(self, node: BsFile):
        for classDef in node.classes:
            self.visit(classDef)
            self.current_context=self.context
            
        for statement in node.statements:
            if isinstance(statement, FuncDef):
                self.visit(statement)
                
            self.current_context=self.context
            
    @visitor(ClassDef)
    def visit(self, node: ClassDef):
        for attrDef in node.attributes:
            self.current_context=node.my_context
            self.visit(attrDef)
            self.current_context=self.context
            
        for methodDef in node.methods:
            self.current_context=node.my_context
            self.visit(methodDef)
            self.current_context=self.context
            
    @visitor(AttrDef)
    def visit(self, node: AttrDef):
        node.context=self.current_context
        node.context.define_var(node.name, node.type)

    @visitor(FuncDef)
    def visit(self, node: FuncDef):
        node.context=self.current_context
        node.my_context=node.context.define_func(node.name, node.return_type, node.arg_names, node.arg_types)

            