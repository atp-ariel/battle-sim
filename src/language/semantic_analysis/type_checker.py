from .context import  *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *


class Type_Checker:
    def __init__(self, context):
        self.context = context
        self.var = []

    @visitor(BsFile)
    def visit(self, node: BsFile, logger):
        for c in node.classes:
            self.visit(c, logger)
        
        for s in node.statements:
            self.visit(s, logger)

    @visitor(BinaryExpression)
    def visit(self, node: BinaryExpression, logger):
        # Ver AritmeticBinaryExpression
        self.visit(node.left, logger)
        self.visit(node.right, logger)

        node.computed_type = node.left.computed_type
        node.computed_type = node.right.computed_type

        if node.left.computed_type != node.right.computed_type:
            if node.left.computed_type == "Var":
                node.computed_type = node.left.computed_type
                var = self.var.pop()
                self.context.define_var(var, node.computed_type)

            else:
                logger.error("Type mismatch...")
                node.computed_type = None

        else:
            node.computed_type = node.left.computed_type

    @visitor(AritmeticBinaryExpression)
    def visit(self, node: AritmeticBinaryExpression, logger):
        self.visit(node.left, logger)
        self.visit(node.right, logger)

        if node.left.computed_type != node.right.computed_type:
            if node.left.computed_type == "Var":
                node.computed_type = node.left.computed_type
                var = self.var.pop()
                self.context.define_var(var, node.computed_type)

            else:
                logger.error("Type mismatch...")
                node.computed_type = None

        if node.left.computed_type == node.right.computed_type:
            if node.left.computed_type == "Number":
                node.computed_type = node.left.computed_type

    @visitor(TernaryExpression)
    def visit(self, node: TernaryExpression, logger):
        self.visit(node.condition)
        self.visit(node.right)
        self.visit(node.left)

        if node.right.computed_type == node.left.computed_type:
            logger.error("Type mismatch...")
            node.computed_type = None

        else:
            logger.error("Type mismatch...")
            node.computed_type = None

    @visitor(Inversion)
    def visit(self, node: Inversion, logger):
        self.visit(node.expression, logger)
        if node.expression.computed_type == "Bool":
            node.computed_type = "Bool"

    @visitor(Primary)
    def visit(self, node: Primary, logger):
        self.visit(node.expression, logger)

        if node.args is None:
            _type = self.context.get_type_object(node.expression.computed_type)

            if _type.is_method:
                node.computed_type = _type.get_method(node.name)[0]

            elif _type.is_attribute:
                node.computed_type = _type.get_attribute(node.name)[0]

        else:
            if node.expression.computed_type == "Var":
                args = [0]*len(node.args)

                for i in range(len(node.args)):
                    self.visit(node.args[i], logger)
                    args[i] = node.args[i].computed_type

                name = node.expression.name
                if self.context.check_func_args(name, args):
                    self.context.get_return_type(name)

    @visitor(Variable)
    def visit(self, node: Variable, logger):
        # No me queda claro si ya está definida o no
        if self.context.var_is_definied(node.name):
            node.computed_type = self.context.get_type(node.name)

        else:
            self.var.append(node.name)
            node.computed_type = "Var"
        pass

    @visitor(Number)
    def visit(self, node: Number, logger):
        node.computed_type = "Number"

    @visitor(Bool)
    def visit(self, node: Bool, logger):
        node.computed_type = "Bool"

    @visitor(MyNone)
    def visit(self, node: MyNone, logger):
        node.computed_type = "MyNone"

    @visitor(MyList)
    def visit(self, node: MyList, logger):
        node.computed_type = "MyList"
