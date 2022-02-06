from .context import  *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *
import logging

class Type_Checker:
    def __init__(self, context):
        self.context = context

    @visitor(BsFile)
    def visit(self, node: BsFile):
        for c in node.classes:
            self.visit(c)
        
        for s in node.statements:
            self.visit(s)

    @visitor(ClassDef)
    def visit(self,node:ClassDef):
        for a in node.attributes:
            self.visit(a)

        for m in node.methods:
            self.visit(m)


        node.computed_type="Class"

    @visitor(AttrDef)
    def visit(self,node:AttrDef):
        self.visit(node.init)
        node.computed_type=node.init.computed_type

    @visitor(FuncDef)
    def visit(self,node:FuncDef):
        for i in node.body:
            self.visit(i)

        node.computed_type=node.return_type

        

    @visitor(If)
    def visit(self,node:If):
        self.visit(node.condition)

        for i in node.body:
            self.visit(i)

        node.computed_type=None

    @visitor(Branch)
    def visit(self,node:Branch):
        for i in node.ifs:
            self.visit(i)

        for e in node.else_body:
            self.visit(e)
        
        node.computed_type=None


    @visitor(WhileDef)
    def visit(self,node:WhileDef):
        self.visit(node.condition)

        for i in node.body:
            self.visit(i)

        node.computed_type=None
        

    @visitor(Decl)
    def visit(self,node:Decl):
        self.visit(node.expression)
        if self.context.check_var_type(node.name,node.type) and node.expression.computed_type == node.type:
            node.computed_type=None

        else:
            logging.error("Type mismatch...")
            node.computed_type = None
            
    @visitor(Assign)
    def visit(self,node:Assign):
        self.visit(node.expression)
        if self.context.check_var_type(node.name,node.expression.computed_type):
            node.computed_type=None

        else:
            logging.error("Type mismatch...")
            node.computed_type = None

    @visitor(Return)
    def visit(self,node:Return):
        self.visit(node.expression)

        node.computed_type=None

    @visitor(Break)
    def visit(self,node:Break):
        node.computed_type=None

    @visitor(Continue)
    def visit(self,node:Continue):
        node.computed_type=None

    @visitor(BinaryExpression)
    def visit(self, node: BinaryExpression):
        # Ver AritmeticBinaryExpression
        self.visit(node.left)
        self.visit(node.right)

        node.computed_type = node.left.computed_type
        node.computed_type = node.right.computed_type

        if node.left.computed_type != node.right.computed_type:
            logging.error("Type mismatch...")
            node.computed_type = None

        else:
            node.computed_type = node.left.computed_type

    @visitor(AritmeticBinaryExpression)
    def visit(self, node: AritmeticBinaryExpression):
        self.visit(node.left)
        self.visit(node.right)

        if node.left.computed_type != node.right.computed_type:
            if node.left.computed_type == "Var":
                node.computed_type = node.left.computed_type
                var = self.var.pop()
                self.context.define_var(var, node.computed_type)

            else:
                logging.error("Type mismatch...")
                node.computed_type = None

        if node.left.computed_type == node.right.computed_type:
            if node.left.computed_type == "Number":
                node.computed_type = node.left.computed_type

    @visitor(TernaryExpression)
    def visit(self, node: TernaryExpression):
        self.visit(node.condition)
        self.visit(node.right)
        self.visit(node.left)

        if node.right.computed_type == node.left.computed_type:
            logging.error("Type mismatch...")
            node.computed_type = None

        else:
            logging.error("Type mismatch...")
            node.computed_type = None

    @visitor(Inversion)
    def visit(self, node: Inversion):
        self.visit(node.expression)
        if node.expression.computed_type == "Bool":
            node.computed_type = "Bool"

    @visitor(Primary)
    def visit(self, node: Primary):
        self.visit(node.expression)

        if node.args is None:
            _type = self.context.get_type_object(node.expression.computed_type)

            if _type.is_method:
                node.computed_type = _type.get_method(node.name)[0]

            elif _type.is_attribute:
                node.computed_type = _type.get_attribute(node.name)[0]

        else:
            if node.expression.computed_type == "function":
                args = [0]*len(node.args)

                for i in range(len(node.args)):
                    self.visit(node.args[i])
                    args[i] = node.args[i].computed_type

                name = node.expression.name
                if self.context.check_func_args(name, args):
                    self.context.get_return_type(name)

    @visitor(Variable)
    def visit(self, node: Variable):
        if self.context.var_is_definied(node.name):
            node.computed_type = self.context.get_type(node.name)

        else:
            for t in context._type_context:
                attr=context.get_type_object(t).attributes
                for a in attr:
                    if node.name==a:
                        node.computed_type = t.get_type(a)

            logging.error(f"name {node.name} is not defined")
            
    @visitor(Number)
    def visit(self, node: Number):
        node.computed_type = "Number"

    @visitor(Bool)
    def visit(self, node: Bool):
        node.computed_type = "Bool"

    @visitor(MyNone)
    def visit(self, node: MyNone):
        node.computed_type = "MyNone"

    @visitor(MyList)
    def visit(self, node: MyList):
        node.computed_type = "MyList"
