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
        node.my_context=self.context.create_type(node.name,parent=node.parent)[1]
        node.context=self.current_context

        


        
    