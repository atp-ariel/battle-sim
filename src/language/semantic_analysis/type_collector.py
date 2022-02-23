from .context import  *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *


class Type_Collector:
    def __init__(self, context):
        self.context = context
        self.current_context=context

    @visitor(BsFile)
    def visit(self, node: BsFile):

        for classDef in node.classes:
            self.visit(classDef)  # revisar esto

    @visitor(ClassDef)
    def visit(self, node: ClassDef):
        if node.parent=="LandUnit" or node.parent=="NavalUnit" or node.parent=="StaticObject":
            cont=self.context.create_type(node.name,node.arg_names,node.arg_types,node.parent)
            node.my_context=cont[1]
            node.context=self.current_context
            node.constructor_context=cont[2]
                
        else:
            raise Exception(f"Parent is not valid for class {node.name}")

        


        
    