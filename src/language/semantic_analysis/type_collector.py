from .context import  *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *


class Type_Collector:
    def __init__(self, context):
        self.context = context

    @visitor(BsFile)
    def visit(self, node: BsFile):

        for classDef in node.classes:
            self.visit(classDef)  # revisar esto

    @visitor(ClassDef)
    def visit(self, node: ClassDef):
        self.context.create_type(node.name)
        