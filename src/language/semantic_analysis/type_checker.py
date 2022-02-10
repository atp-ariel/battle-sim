from numpy import isin
from .context import *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *


class Type_Checker:
    def __init__(self, context):
        self.context = context
        self.bool_ops = set(["eq","neq","lte","lt","gte","gt"])

    @visitor(BsFile)
    def visit(self, node: BsFile):
        for c in node.classes:
            self.visit(c)

        for s in node.statements:
            self.visit(s)

    @visitor(ClassDef)
    def visit(self, node: ClassDef):

        for a in node.attributes:
            a._class=node.context.get_type_object(node.name)
            self.visit(a)

        for m in node.methods:
            self.visit(m)

        node.computed_type = "Class"

    @visitor(AttrDef)
    def visit(self, node: AttrDef): 
        self.visit(node.init)
        
        node.computed_type = node.init.computed_type
        if isinstance(node.computed_type,list):
            node.computed_type=node.computed_type[1]
            
        if node.type != node.computed_type:
            raise Exception(f"The type of the variable {node.name} is different from the defined type. Expected {node.type}, Recived {node.computed_type}")

        node._class.define_attribute(node.name,node.computed_type,node.init)
        
    @visitor(FuncDef)
    def visit(self, node: FuncDef):
        if not node.context.check_func(node.name):
            if node.arg_types[0]==node.context.name:
                node.context.define_func(node.name,node.return_type,node.arg_names[1:],node.arg_types[1:])
            
            else:
                node.context.define_func(node.name,node.return_type,node.arg_names,node.arg_types)
                

        
        returns_types = set()
        for i in node.body:
            self.visit(i)
            if isinstance(i, Return):
                returns_types.add(i.computed_type)
                
        if len(returns_types) == 1:
            node.computed_type = list(returns_types)[0]

        else:
            raise Exception("More than one return type in the function")

        if node.return_type!=node.computed_type:
            #print(f"func {node.name}")
            raise Exception("The return type is not the one specified for the function {node.name}")

    @visitor(If)
    def visit(self, node: If):
        self.visit(node.condition)
        
        if node.condition.computed_type != "bool":
            raise Exception("Condition in if statements must be a bool")

        for i in node.body:
            self.visit(i)

        node.computed_type = None

    @visitor(Branch)
    def visit(self, node: Branch):
        for i in node.ifs:
            self.visit(i)

        if not node.else_body is None:
            for e in node.else_body:
                self.visit(e)

        node.computed_type = None

    @visitor(WhileDef)
    def visit(self, node: WhileDef):
        self.visit(node.condition)
        if node.condition.computed_type != "bool":
            raise Exception("Condition in while statements must be a bool")
            
        for i in node.body:
            self.visit(i)

        node.computed_type = None

    @visitor(Decl)
    def visit(self, node: Decl):
        self.visit(node.expression)
        #print(node.expression.computed_type) 
        if (not (node.context.check_var(node.name)) or node.context.check_var_type(node.name,node.type)) and node.expression.computed_type == node.type:
            node.context.define_var(node.name,node.type,node.expression)
            node.computed_type = None

        else:
            #print(f"decl {node.name}")
            raise Exception(f"Type mismatch for for the declaration of the variable {node.name}")
            node.computed_type = None

    @visitor(Assign)
    def visit(self, node: Assign):
        self.visit(node.expression)
        if node.context.check_var_type(node.name, node.expression.computed_type):
            self.node.context.define_var(node.name,node.type,node.expression)
            node.computed_type = None

        else:
            #print(f"assign {node.name}")
            raise Exception("Type mismatch...")
            node.computed_type = None

    @visitor(Return)
    def visit(self, node: Return):
        self.visit(node.expression)

        node.computed_type = node.expression.computed_type

    @visitor(Break)
    def visit(self, node: Break):
        node.computed_type = None

    @visitor(Continue)
    def visit(self, node: Continue):
        node.computed_type = None

    @visitor(BinaryExpression)
    def visit(self, node: BinaryExpression):
        # Ver AritmeticBinaryExpression
        self.visit(node.left)
        self.visit(node.right)

        node.computed_type = node.left.computed_type
        node.computed_type = node.right.computed_type

        if node.left.computed_type != node.right.computed_type:
            #print(f"bin {node.left} {node.right}")
            raise Exception("Type mismatch binary expression")
            node.computed_type = None

        else:
            node.computed_type = node.left.computed_type

    @visitor(AritmeticBinaryExpression)
    def visit(self, node: AritmeticBinaryExpression):
        self.visit(node.left)
        self.visit(node.right)

        if node.left.computed_type != node.right.computed_type:
                #print(f"aritmetic {node.left} {node.right}")
                raise Exception("Type mismatch for aritmetic expression")
                node.computed_type = None

        else:
            if node.left.computed_type == "number":
                node.computed_type = node.left.computed_type
                
                if node.op in self.bool_ops:
                    node.computed_type="bool"
                
            else:
                raise Exception("Invalid operation")
                
    @visitor(TernaryExpression)
    def visit(self, node: TernaryExpression):
        self.visit(node.condition)
        self.visit(node.right)
        self.visit(node.left)

        if node.right.computed_type == node.left.computed_type:
            #print("Ternary")
            if node.condition.computed_type=="bool":
                node.computed_type = None
                
            else:
                raise Exception("Condition most be a bool")
                
                

        else:
            raise Exception("Type mismatch for Ternary expression")
            node.computed_type = None

    @visitor(Inversion)
    def visit(self, node: Inversion):
        self.visit(node.expression)
        if node.expression.computed_type == "bool":
            node.computed_type = "bool"

    @visitor(Primary)
    def visit(self, node: Primary):
        self.visit(node.expression)
        
        if node.args is None:
            #print(f"Type {node.expression.computed_type}")
            _type = node.context.get_type_object(node.expression.computed_type)

            if _type.is_method(node.name):
                node.computed_type = _type.get_method(node.name)[0]

           
            elif _type.is_attribute(node.name):
                node.computed_type = _type.get_attribute(node.name)[0]
                
            elif isinstance(node.expression.computed_type, list) and node.expression.computed_type[0]== 'var':
                #print(f"node {node.name}: {node.expression.computed_type}")
                #print(f"{node.expression.computed_type[1]} {node.expression.computed_type[1] in node.context.children}")
                
                    
                if (((node.expression.computed_type[1] in node.context.children) and (node.context.children[node.expression.computed_type[1]].check_var(node.name)))or ((node.context.is_context_father(node.expression.computed_type[1])) and (node.context.get_context_father(node.expression.computed_type[1]).check_var(node.name)))):
                    if node.expression.computed_type[1] in node.context.children:
                        exp_type=node.context.children[node.expression.computed_type[1]].get_type(node.name)
                    
                    else:
                        exp_type=node.context.get_context_father(node.expression.computed_type[1]).get_type(node.name)
                        
                    if exp_type[0]=='var':
                        node.computed_type=exp_type[1]
                        
                    else:
                        node.computed_type=node.context.children[node.expression.computed_type[1]].get_return_type(node.name)
                        
                else:
                    raise Exception(f"Name {node.name} is not defined")
                    
            else:
                    raise Exception(f"Name {node.name} is not a var")       

        else:
            if isinstance(node.expression.computed_type, list) and node.expression.computed_type[0]== 'function':
                args = [0]*len(node.args)

                for i in range(len(node.args)):
                    self.visit(node.args[i])
                    args[i] = node.args[i].computed_type
                    if isinstance(args[i],list):
                        args[i]=args[i][1]

                name = node.expression.name
                if node.context.check_func_args(name,args):
                    node.computed_type=node.context.get_return_type(name)
                
                else:
                    raise Exception(f"Some types are incorrect for function {name}")
                    
                
            elif (((node.expression.computed_type[1] in node.context.children) and (node.context.children[node.expression.computed_type[1]].check_var(node.name)))or ((node.context.is_context_father(node.expression.computed_type[1])) and (node.context.get_context_father(node.expression.computed_type[1]).check_var(node.name)))):
                if node.expression.computed_type[1] in node.context.children:
                    exp_type=node.context.children[node.expression.computed_type[1]].get_type(node.name)
                    
                else:
                    exp_type=node.context.get_context_father(node.expression.computed_type[1]).get_type(node.name)
                        
                if exp_type[0]=="var":
                    node.computed_type=exp_type[1]
                        
                else:
                    node.computed_type=node.context.children[node.expression.computed_type[1]].get_return_type(node.name)
                    
            else:
                raise Exception(f"Name {node.name} is not a var")
                
    @visitor(Variable)
    def visit(self, node: Variable):
        #print(f"name {node.name}")
        #print(f"context {node.context.name}")
        #print(self.context._var_context.keys())
        
        if node.context.check_var(node.name):
            node.computed_type = node.context.get_type(node.name)

        else: 
            for c in node.context.children:
                if node.context.children[c].check_var(node.name):
                    node.computed_type=node.context.get_type(node.name)
                    return

            raise Exception(f"name {node.name} is not defined")

    @visitor(Number)
    def visit(self, node: Number):
        node.computed_type = "number"

    @visitor(Bool)
    def visit(self, node: Bool):
        node.computed_type = "bool"

    @visitor(MyNone)
    def visit(self, node: MyNone):
        node.computed_type = "MyNone"

    @visitor(MyList)
    def visit(self, node: MyList):
        node.computed_type = "List"
