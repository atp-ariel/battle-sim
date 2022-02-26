from .context import  *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *


class Type_Builder:

    def __init__(self, context) -> None:
        self.context = context
        self.current_type : Type

    @visitor(BsFile)
    def visit(self, node: BsFile):
        for classDef in node.classes:
            self.visit(classDef)
            
    @visitor(ClassDef)
    def visit(self, node: ClassDef):
        
        self.current_type=self.context.get_type_object(node.name)
        
        for attrDef in node.attributes:
            self.visit(attrDef)
            
        for methodDef in node.methods:
            self.visit(methodDef)
            
    @visitor(AttrDef)
    def visit(self, node: AttrDef):
        node.context=self.current_type.context
        self.current_type.define_attribute(node.name, node.type)

    @visitor(FuncDef)
    def visit(self, node: FuncDef):
        node.context=self.current_type.context
        node.my_context=self.current_type.define_method(node.name, node.return_type, node.arg_names, node.arg_types)
        node.my_context.define_var("self",self.current_type.name)
        node.my_context.define_func("super",self.current_type.parent.name,[],[])

            