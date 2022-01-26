from abc import ABC,abstractmethod
from dataclasses import dataclass
from typing import  List
import enum

@dataclass
class Node(ABC):
    @abstractmethod
    def validate(self, context: Context) -> bool:
        pass

class BsFile(Node):
    staments: List[Stament]
    
    def validate(self, context: Context) -> bool:
        for st in self.statements:
            if not st.validate(context):
                return False
        return True

class Stament(Node):
    pass

class Expression(Node):
    pass

#region Staments    
class FuncDef(Stament):
    name: str
    args : List[str]
    body : List[Stament]
    
    def validate(self, context: Context) -> bool:
        inner_context = context.create_child_context()
        
        for arg in self.args:
            inner_context.define_var(arg)
        
        for st in body:
            if not st.validate(inner_context):
                return False    
        
        return context.define_fun(self.name, self.args)

class If(Stament):
    condition : Expression
    body : List[Stament]
    
    def validate(self, context: Context) -> bool:
        inner_context = context.create_child_context()
        
        if not self.condition.validate(context):
            return False
        
        for st in self.body:
            if not st.validate(inner_context):
                return False
        
        return True      

class Branch(Stament):
    ifs : List[If]
    else_body : List[Stament]
    
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
    body: List[Stament]

class ClassDef(Node):
    name: str
    attributes: List[AttrDef]
    methods: List[MethodDef]

class WhileDef(Stament):
    condition : Expression
    body : List[Stament]
    
    def validate(self, context) -> bool:
        if not self.condition.validate(context):
            return False
        
        inner_context = context.create_child_context()
        
        for st in self.body:
            if st.validate(inner_context):
                return False
            
        return True
        
    
class Assign(Stament):
    name: str
    expression: Expression
    
    def validate(self, context: Context) -> bool:
        if not self.expression.validate(context):
            return False
        if not context.define_var(self.name):
            return False
        return True
    
class Return(Stament):
    expression : Expression
    
    def validate(self, context : Context) -> bool:
        return expression.validate(context)
        
class Break(Stament):
    def validate(self, context: Context) -> bool:
        return True

class Continue(Stament):
    def validate(self, context: Context) -> bool:
        return True

#endregion

#region BinaryExpressions
class Operator(enum.Enum):
    Add: enum.auto()
    Sub: enum.auto()
    Mult: enum.auto()
    Div: enum.auto()
    Mod: enum.auto()
    And: enum.auto()
    Or: enum.auto()
    Eq: enum.auto()
    Neq: enum.auto()
    Gte: enum.auto()
    Lte: enum.auto()
    Gt: enum.auto()
    Lt: enum.auto()


class BinaryExpression(Expression):
    op: Operator
    left : Expression
    right : Expression
    
    def validate(self, context: Context) -> bool:
        return self.left.validate(context) and self.right.validate(context)

#endregion

#region AtomicExpressions
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

#endregion