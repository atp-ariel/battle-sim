from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List


@dataclass
class Node(ABC):
    pass


@dataclass
class Statement(Node):
    pass


@dataclass
class Expression(Node):
    pass


@dataclass
class FuncDef(Statement):
    name: str
    return_type: str
    arg_names: List[str]
    arg_types: List[str]
    body: List[Statement]
    context: Context
    my_context: Context


@dataclass
class AttrDef(Node):
    name: str
    type: str
    init: Expression
    context: Context


@dataclass
class ClassDef(Node):
    name: str
    parent: str
    arg_names: List[str]
    arg_types: List[str]
    attributes: List[AttrDef]
    methods: List[FuncDef]
    context: Context
    my_context: Context


@dataclass
class BsFile(Node):
    classes: List[ClassDef]
    statements: List[Statement]


@dataclass
class If(Statement):
    condition: Expression
    body: List[Statement]


@dataclass
class Branch(Statement):
    ifs: List[If]
    else_body: List[Statement]


@dataclass
class WhileDef(Statement):
    condition: Expression
    body: List[Statement]


@dataclass
class Decl(Statement):
    type: str
    name: str
    expression: Expression
    context: Context


@dataclass
class Assign(Statement):
    name: str
    expression: Expression
    context: Context


@dataclass
class Return(Statement):
    expression: Expression


@dataclass
class Break(Statement):
    pass


@dataclass
class Continue(Statement):
    pass

# endregion

# region BinaryExpressions


@dataclass
class BinaryExpression(Expression):
    op: str
    left: Expression
    right: Expression


@dataclass
class AritmeticBinaryExpression(BinaryExpression):
    pass


@dataclass
class TernaryExpression(Expression):
    left: Expression
    condition: Expression
    right: Expression

# endregion

# region AtomicExpressions
@dataclass
class Inversion(Expression):
    expression: Expression


@dataclass
class Primary(Expression):
    expression: Expression
    name: str
    args: List[Expression]


@dataclass
class Variable(Expression):
    name: str
    context: Context


@dataclass
class Number(Expression):
    value: str


@dataclass
class Bool(Expression):
    value: str


@dataclass
class MyNone(Expression):
    pass

@dataclass
class MyList(Expression):
    inner_list: List[Expression]

# endregion


@dataclass
class ReturnType:
    type: str


@dataclass
class Type:
    type: str


@dataclass
class Params:
    type: str
    name: str
    params: 'Params'


@dataclass
class Statements:
    statement: Statement
    statements: 'Statements'


@dataclass
class ElseDef:
    body: List[Statement]


@dataclass
class ElifDef:
    expression: Expression
    body: List[Statement]
    elif_def: 'ElifDef'
    else_def: ElseDef


@dataclass
class Expressions:
    expression: Expression
    expressions: 'Expressions'


@dataclass
class Functions:
    function: FuncDef
    functions: 'Functions'


@dataclass
class Attributes:
    attr_def: AttrDef
    attributes: 'Attributes'


@dataclass
class Constructor:
    arg_names: List[str]
    arg_types: List[str]
    attributes: List[AttrDef]


@dataclass
class Classes:
    class_def: ClassDef
    classes: 'Classes'
