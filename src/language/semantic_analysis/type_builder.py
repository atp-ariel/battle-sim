from .context import  *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *


class Type_Builder:

    def __init__(self, context) -> None:
        self.context = context
        self.current_context=context

    @visitor(BsFile)
    def visit(self, node: BsFile):
        self.current_context=self.context
        for classDef in node.classes:
            self.visit(classDef)


    @visitor(ClassDef)
    def visit(self, node: ClassDef):
        self.current_type = self.context.get_type_object(node.name)
        node.context=self.current_context
        for attrDef in node.attributes:
            self.current_context=node.my_context
            self.visit(attrDef)

        for methodDef in node.methods:
            self.current_context=node.my_context
            self.visit(methodDef)

    @visitor(AttrDef)
    def visit(self, node: AttrDef):
        node.context=self.current_context
        self.current_type.define_attribute(node.name, node.type)

    @visitor(FuncDef)
    def visit(self, node: FuncDef):
        node.context=self.current_context
        node.my_context=self.current_type.define_method(node.name, node.return_type, node.arg_names, node.arg_types)
        self.current_context=node.my_context
