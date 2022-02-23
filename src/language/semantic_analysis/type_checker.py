from numpy import isin
from .context import *
from typing import List
from ...utils.visitor import *
from ..parser.ast import *


class Type_Checker:
    def __init__(self, context):
        self.context = context
        self.bool_ops = set(["eq","neq","lte","lt","gte","gt"])
        self.return_type = ""
        self.no_return_type=True

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
            
        if not node.context.check_type(node.type,node.computed_type) and node.computed_type != "None":
            raise Exception(f"The type of the variable {node.name} is different from the defined type. Expected {node.type}, Recived {node.computed_type}")
        
    @visitor(FuncDef)
    def visit(self, node: FuncDef):
        self.return_type=node.return_type
        for i in node.body:
            self.visit(i)
            
        if node.return_type == "void" and not self.no_return_type:
            raise Exception(f"There is a return for the void function {node.name} ")
            
        elif node.return_type != "void" and self.no_return_type:
            raise Exception(f"There is not returning any value for the function {node.name} ")
      
        self.return_type = ""
        self.no_return_type=True
        
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
        if isinstance(node.expression.computed_type, list):
            node.expression.computed_type=node.expression.computed_type[1]
        if (not node.context.check_var(node.name)) and (node.context.check_type(node.type,node.expression.computed_type) or node.expression.computed_type=="None"):
            node.context.define_var(node.name,node.type)
            node.computed_type = None

        else:
            if node.context.check_var(node.name):
                raise Exception(f"Var {node.name} is already defined")
                
            raise Exception(f"Type mismatch for for the declaration of the variable {node.name}")
            node.computed_type = None

    @visitor(Assign)
    def visit(self, node: Assign):
        self.visit(node.expression)
        if node.context.check_var_type(node.name, node.expression.computed_type) or node.expression.computed_type=="None":
            node.computed_type = None

        else:
            raise Exception(f"the expected type for the variable {node.name} is not the one received ")
            node.computed_type = None

    @visitor(Return)
    def visit(self, node: Return):
        node.computed_type = "Null"
        if not node.expression is None :
            self.visit(node.expression)

            node.computed_type = node.expression.computed_type
            
        if not node.context.is_in_func_context():
            raise Exception(f"Return expression most be in a function")
        
        if isinstance(node.computed_type,list):
            node.computed_type=node.computed_type[1]
                
        self.no_return_type=False
            
        if node.computed_type=="Null":
            self.no_return_type=True
            return
                
        if not node.context.check_type(self.return_type,node.computed_type) and (node.computed_type == "None" and (self.return_type=="number" or self.return_type=="bool")):
            raise Exception("The return type does not match with the one specified")

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

        if node.left.computed_type != node.right.computed_type and node.right.computed_type != "None":
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
            node.right.computed_type=node.right.computed_type[1]
            
        if node.left.computed_type != node.right.computed_type and node.right.computed_type != "None":
                raise Exception("Type mismatch for aritmetic expression")

        else:
            if node.left.computed_type == "number" or (node.right.computed_type== "None" and (node.op=="eq" or node.op=="neq")):
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
            node.right.computed_type=node.right.computed_type [1]
            
            
        if isinstance(node.condition.computed_type, list):
            node.condition.computed_type=node.condition.computed_type[1]
            

        if node.right.computed_type == node.left.computed_type:
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
        expr_type=node.expression.computed_type
        expr_name=node.expression.name
        if node.name is None:
            if isinstance(node.expression.computed_type,list):
                expr_type=expr_type[1]
                    
                if node.expression.computed_type[0]== 'function':
                    args = [0]*len(node.args)

                    for i in range(len(node.args)):
                        self.visit(node.args[i])
                        args[i] = node.args[i].computed_type
                        if isinstance(args[i],list):
                            args[i]=args[i][1]
                
                    if node.context.check_func_args(expr_name,args):
                        node.computed_type=node.context.get_return_type(expr_name)
                        
                    elif isinstance(node.expression, Primary):
                        _type=node.expression.expression.computed_type
                        
                        if isinstance(_type, list):
                            _type=_type[1]
                          
                        _type=node.context.get_type_object(_type)
                        
                        if _type.context.check_func_args(expr_name,args):
                            node.computed_type=_type.context.get_return_type(expr_name)
                        
                        else:
                            raise Exception(f"Function {expr_name} is not a function for the type {_type.name} ")
                        
                    else:
                        raise Exception(f"Some types are incorrect for function {expr_name}")

             
        else:
            _type = node.expression.computed_type
            
            if isinstance(_type, list):
                _type=_type[1]
                
            t_object=node.context.get_type_object(_type)
                
            if t_object.is_attribute(node.name):
                node.computed_type = t_object.context.get_type(node.name)
                
            elif isinstance(node.expression, Primary):
                _type=node.expression.expression.computed_type
                        
                if isinstance(_type, list):
                    _type=_type[0]
                          
                _type=node.context.get_type_object(_type)
                if _type.is_attribute(expr_name):
                    node.computed_type=_type.context.get_type(expr_name)
                        
                else:
                    raise Exception(f"Variable {expr_name} is not a variable for the type {temp[0]} ")
                        
                
            else:
                raise Exception(f"Attribute {node.name} is not defined for type {_type} ")
                       
    @visitor(Variable)
    def visit(self, node: Variable):
        
        if node.context.check_var(node.name):
            node.computed_type = node.context.get_type(node.name)
            return

        elif self.context.check_var(node.name):
            node.computed_type = self.context.get_type(node.name)
            return
        
        raise Exception(f"Name {node.name} is not defined")

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
            