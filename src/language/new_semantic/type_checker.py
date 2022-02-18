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
        
        node.computed_type=node.init.computed_type
        if isinstance(node.computed_type,list):
            node.computed_type=node.computed_type[1]
            
        if node.type != node.computed_type and node.computed_type != "None":
            raise Exception(f"The type of the variable {node.name} is different from the defined type. Expected {node.type}, Recived {node.computed_type}")

        node.context.assign_var(node.name,node.type,node.init)
        
    @visitor(FuncDef)
    def visit(self, node: FuncDef):
        returns_types = set()
        for i in node.body:
            self.visit(i)
            if isinstance(i, Return):
                if isinstance(i.computed_type,list):
                    i.computed_type=i.computed_type[1]
                returns_types.add(i.computed_type)
                
        if len(returns_types) == 1:
            node.computed_type = list(returns_types)[0]
            
            if node.return_type == "void" and node.computed_type != "None":
                raise Exception(f"There is a return for the void function {node.name} ")
            
            if node.return_type!=node.computed_type:
                raise Exception("The return type is not the one specified for the function {node.name}")

            
        elif len(returns_types) == 0:
            if node.return_type != "void":
                raise Exception(f"There is not returning any value for the function {node.name} ")

        else:
            raise Exception(f"More than one return type for the function {node.name} ")
        
    @visitor(If)
    def visit(self, node: If):
        self.visit(node.condition)
        
        if isinstance(node.condition.computed_type, list):
            node.condition.computed_type=node.condition.computed_type[1]
        
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
        
        if isinstance(node.condition.computed_type, list):
            node.condition.computed_type=node.condition.computed_type[1]
            
        if node.condition.computed_type != "bool":
            raise Exception("Condition in while statements must be a bool")
            
        for i in node.body:
            self.visit(i)

        node.computed_type = None

    @visitor(Decl)
    def visit(self, node: Decl):
        self.visit(node.expression)
        #print(node.expression.computed_type) 
        if (not node.context.check_var(node.name)) and (node.expression.computed_type == node.type or node.expression.computed_type=="None"):
            node.context.define_var(node.name,node.type,node.expression)
            node.computed_type = None

        else:
            if node.context.check_var(node.name):
                raise Exception(f"Var {node.name} is already defined")
                
            #print(f"decl {node.name}")
            raise Exception(f"Type mismatch for for the declaration of the variable {node.name}")
            node.computed_type = None

    @visitor(Assign)
    def visit(self, node: Assign):
        self.visit(node.expression)
        if node.context.check_var_type(node.name, node.expression.computed_type) or node.expression.computed_type=="None":
            self.node.context.assign_var(node.name,node.expression.computed_type,node.expression)
            node.computed_type = None

        else:
            #print(f"assign {node.name}")
            raise Exception(f"the expected type for the variable {node.name} is not the one received ")
            node.computed_type = None

    @visitor(Return)
    def visit(self, node: Return):
        node.computed_type = "None"
        if not node.expression is None :
            self.visit(node.expression)

            node.computed_type = node.expression.computed_type
            
        if not node.context.is_in_func_context():
            raise Exception(f"Return expression most be in a function")

    @visitor(Break)
    def visit(self, node: Break):
        node.computed_type = None
        
        if not node.context.is_in_while_context():
            raise Exception(f"Break expression most be in a loop")

    @visitor(Continue)
    def visit(self, node: Continue):
        node.computed_type = None
        
        if not node.context.is_in_while_context():
            raise Exception(f"Continue expression most be in a loop")

    @visitor(BinaryExpression)
    def visit(self, node: BinaryExpression):
        # Ver AritmeticBinaryExpression
        self.visit(node.left)
        self.visit(node.right)

        if isinstance(node.left.computed_type,list):
            node.left.computed_type=node.left.computed_type [1]
            
        if isinstance(node.right.computed_type,list):
            node.right.computed_type=node.left.computed_type [1]

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

        if isinstance(node.left.computed_type,list):
            node.left.computed_type=node.left.computed_type[1]
            
        if isinstance(node.right.computed_type,list):
            node.right.computed_type=node.left.computed_type[1]
            
        if node.left.computed_type != node.right.computed_type:
                #print(f"aritmetic {node.left} {node.right}")
                print(f"{node.left}: {node.left.computed_type}")
                raise Exception("Type mismatch for aritmetic expression")

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
        
        if isinstance(node.left.computed_type,list):
            node.left.computed_type=node.left.computed_type [1]
            
        if isinstance(node.right.computed_type,list):
            node.right.computed_type=node.left.computed_type [1]
            
            
        if isinstance(node.condition.computed_type, list):
            node.condition.computed_type=node.condition.computed_type[1]
            

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
            
        if isinstance(node.expression.computed_type, list):
            node.condition.computed_type=node.condition.computed_type[1]
            
        if node.expression.computed_type == "bool":
            node.computed_type = "bool"

    @visitor(Primary)
    def visit(self, node: Primary):
        self.visit(node.expression)
        
        #Revisar self.func()
        if none.name is None:
            
            expr_type=node.expression.computed_type
            expr_name=node.expression.name
            
            if isinstance(node.expression.computed_type,list):
                expr_type=expr_type[1]
                
            if isinstance(node.expression.computed_type, list) and node.expression.computed_type[0]== 'function':
                args = [0]*len(node.args)

                for i in range(len(node.args)):
                    self.visit(node.args[i])
                    args[i] = node.args[i].computed_type
                    if isinstance(args[i],list):
                        args[i]=args[i][1]
                        
                if node.context.check_func_args(expr_name,args):
                    node.computed_type=node.context.get_return_type(name)
                    
                elif isinstance(node.expression, Primary):
                    _type=node.expression.expression.computed_type
                    
                    if isinstance(_type, list):
                        _type=_type[0]
                        
                    temp=[_type]
                    for i in args:
                        temp.append(i)
                            
                    _type=node.context.get_type_object(_type)
                    if _type.check_method(expr_name,temp):
                        node.computed_type=_type.context.get_return_type(expr_name)
                    
                    else:
                        raise Exception(f"Function {expr_name} is not a function for the type {temp[0]} ")
                else:
                    raise Exception(f"Some types are incorrect for function {name}")

             
        else:
            print(f"{node.expression} {node.expression.computed_type}")
            _type = node.expression.computed_type
            
            if isinstance(_type, list):
                _type=_type[1]
                
            if node.context.get_type_object(_type).is_attribute(node.name):
                node.computed_type = node.context.get_type(node.name)
                
            else:
                raise Exception(f"Attribute {node.name} is not defined for type {_type} ")
                       
    @visitor(Variable)
    def visit(self, node: Variable):
        #print(f"name {node.name}")
        #print(f"context {node.context.name}")
        #print(self.context._var_context.keys())
        
        if node.context.check_var(node.name):
            node.computed_type = node.context.get_type(node.name)
            return

        else: 
            if node.ctor_context.check_var(node.name):
                node.computed_type = node.ctor_context.get_type(node.name)
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
        node.computed_type = "None"

    @visitor(MyList)
    def visit(self, node: MyList):
        node.computed_type = "List"
        
    @visitor(PExpression)
    def visit(self,node:PExpression):
        if not node.expression is None:
            self.visit(node.expression)
            node.computed_type=node.expression.computed_type
            