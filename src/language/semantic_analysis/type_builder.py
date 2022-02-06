from .context import  *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *


class Type_Builder:

    def __init__(self, context) -> None:
        self.context = context

    @visitor(BsFile)
    def visit(self, node: BsFile):
        for classDef in node.classes:
            self.visit(classDef)

    @visitor(ClassDef)
    def visit(self, node: ClassDef):
        self.current_type = self.context.get_type_object(node.name)
        for attrDef in node.attributes:
            self.visit(attrDef)

        for methodDef in node.methods:
            self.visit(methodDef)

    @visitor(AttrDef)
    def visit(self, node: AttrDef):
        attr_type = self.context.create_type(node.type)
        self.current_type.define_attribute(node.name, attr_type)

    @visitor(FuncDef)
    def visit(self, node: FuncDef):
        return_type = self.context.create_type(node.return_type)
        arg_types = [self.context.create_type(t) for t in node.arg_types]
        self.current_type.define_method(
            node.name, return_type, node.arg_names, arg_types)
