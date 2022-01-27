from abc import ABC,abstractmethod
from dataclasses import dataclass
from typing import  List
import enum

class Context:
    pass

@dataclass
class Node(ABC):
    @abstractmethod
    def validate(self, context: Context) -> bool:
        pass
    
class Statement(Node):
    pass

class Expression(Node):
    pass

class BsFile(Node):
    staments: List[Statement]
    
    def validate(self, context: Context) -> bool:
        for st in self.statements:
            if not st.validate(context):
                return False
        return True

#region Statements    
class FuncDef(Statement):
    name: str
    return_type: str
    arg_names: List[str]
    arg_types: List[str]
    body : List[Statement]
    
    def validate(self, context: Context) -> bool:
        inner_context = context.create_child_context()
        
        for arg in self.args:
            inner_context.define_var(arg)
        
        for st in body:
            if not st.validate(inner_context):
                return False    
        
        return context.define_fun(self.name, self.args)

class If(Statement):
    condition : Expression
    body : List[Statement]
    
    def validate(self, context: Context) -> bool:
        inner_context = context.create_child_context()
        
        if not self.condition.validate(context):
            return False
        
        for st in self.body:
            if not st.validate(inner_context):
                return False
        
        return True      

class Branch(Statement):
    ifs : List[If]
    else_body : List[Statement]
    
    def validate(self, context)->bool:
        
        for i in self.ifs:
            if not i.validate(context):
                return False
        
        inner_context = context.create_child_context()    
        for st in self.else_body:
            if not st.validate(inner_context):
                return False
            
        return True
    
class AttrDef(Node):
    name: str
    type: str
    init: Expression

class MethodDef(Node):
    name: str
    return_type: str
    arg_names: List[str]
    arg_types: List[str]
    body: List[Statement]

class ClassDef(Node):
    name: str
    attributes: List[AttrDef]
    methods: List[MethodDef]

class WhileDef(Statement):
    condition : Expression
    body : List[Statement]
    
    def validate(self, context) -> bool:
        if not self.condition.validate(context):
            return False
        
        inner_context = context.create_child_context()
        
        for st in self.body:
            if st.validate(inner_context):
                return False
            
        return True
        
    
class Assign(Statement):
    type : str
    name: str
    expression: Expression
    
    def validate(self, context: Context) -> bool:
        if not self.expression.validate(context):
            return False
        if not context.define_var(self.name):
            return False
        return True
    
class Return(Statement):
    expression : Expression
    
    def validate(self, context : Context) -> bool:
        return expression.validate(context)
        
class Break(Statement):
    def validate(self, context: Context) -> bool:
        return True

class Continue(Statement):
    def validate(self, context: Context) -> bool:
        return True

#endregion

#region BinaryExpressions

class BinaryExpression(Expression):
    op: str
    left : Expression
    right : Expression
    
    def validate(self, context: Context) -> bool:
        return self.left.validate(context) and self.right.validate(context)
    
class AritmeticBinaryExpression(BinaryExpression):
    pass
        
    
class TernaryExpression(Expression):
    left : Expression
    condition : Expression
    right : Expression
    
    def validate(self, context:Context)->bool:
        return self.condition.validate(context) and self.left.validate(context) and self.right.validate(context)

#endregion

#region AtomicExpressions
class Inversion(Expression):
    expression : Expression


class FuncCall(Expression):
    name : str
    args: List[Expression]
    
    def validate(self, context: Context) -> bool:
        for expr in self.args:
            if not expr.validate(context):
                return False

        return context.check_fun(self.name, len(self.args))
    
class Variable(Expression):
    name : str
    
    def validate(self, context: Context) -> bool:
        return context.check_var(self.name)
        
class Number(Expression):
    value: str

    def validate(self, context: Context) -> bool:
        return True
    
class Bool(Expression):
    value: str

    def validate(self, context: Context) -> bool:
        return True
    
class MyList(Expression):
    inner_list : List[Expression]

#endregion

@dataclass
class ReturnType:
    type : str
    
@dataclass
class Type:
    type : str

@dataclass    
class Params:
    type : str
    name : str
    params : Params

@dataclass    
class Block:
    statements: List[Statement]

@dataclass    
class Statements:
    statement : Statement
    statements : Staments 

@dataclass
class ElseDef:
    body : List[Statement]

@dataclass    
class ElifDef:
    expression : Expression
    body : Block
    elif_def : ElifDef
    else_def : ElseDef

@dataclass    
class Expressions:
    expression : expression
    expressions : Expressions 

@dataclass    
class ComparePar:
    op : str
    expression : Expression

@dataclass    
class Primary:
    primary : Primary
    extra : object