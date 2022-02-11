from ...utils.visitor import *
from ..parser.ast import *
from io import StringIO


class CodeGenerate:
    def __init__(self):
        self.file = StringIO(str())
        self.count_tabs = 0

        self.translation = {
            "eq": "==",
            "neq": "!=",
            "lte": "<=",
            "lt": "<",
            "gte": ">=",
            "gt": ">",
            "^": "**"
        }

    def write(self, string: str):
        tab_string = ''.join('\t' for i in range(self.count_tabs))
        self.file.write(tab_string + string)

    @visitor(BsFile)
    def visit(self, node: BsFile):
        self.write("from .core import *\n\n")

        for class_def in node.classes:
            self.visit(class_def)

        for statement in node.statements:
            if isinstance(statement, Expression):
                self.write(self.visit(statement) + "\n")
            else:
                self.visit(statement)

        return self.file.getvalue()

    @visitor(ClassDef)
    def visit(self, node: ClassDef):

        self.write(f'class {node.name}({node.parent}):\n')

        args = ', '.join(arg.name for arg in node.attributes)

        self.count_tabs += 1

        self.write(f'def __init__(self, {args}):\n')

        self.count_tabs += 1

        self.write(f'self.id=id\n')
        self.write(f'self.life_points = 5\n')
        self.write(f'self.defense = 3\n')
        self.write(f'self.map = None\n')
        self.write(f'self.cell : Cell = None\n')

        if node.parent == 'LandUnit' or node.parent == 'NavalUnit':

            self.write(f'self.side = None\n')
            self.write(f'self.moral = 5\n')
            self.write(f'self.attack = 6\n')
            self.write(f'self.solidarity = True\n')
            self.write(f'self.ofensive = 2\n')
            self.write(f'self.min_range = 1\n')
            self.write(f'self.max_range = 3\n')
            self.write(f'self.radio = 1\n')
            self.write(f'self.vision = 6\n')
            self.write(f'self.intelligence = 8\n')
            self.write(f'self.recharge_turns = 0\n')
            self.write(f'self.turns_recharging = 0\n')
            self.write(f'self.movil = True\n')
            self.write(f'self.intelligence = 8\n')
            self.write(f'self.no_defeated_units = 0\n')
            self.write(f'self.visited_cells = set()\n')

        for at in node.attributes:
            self.write(f'self.{at.name} = {self.visit(at.init)}\n')

        self.count_tabs -= 1

        for f in node.methods:
            self.visit(f)

        self.count_tabs -= 1

    @visitor(FuncDef)
    def visit(self, node: FuncDef):

        args = ', '.join(name for name in node.arg_names)
        self.write(f'def {node.name}({args}):\n')

        self.count_tabs += 1
        for statement in node.body:
            if isinstance(statement, Expression):
                self.write(self.visit(statement) + "\n")
            else:
                self.visit(statement)
        self.count_tabs -= 1

    @visitor(Branch)
    def visit(self, node: Branch):

        initial = node.ifs[0]

        self.write(f'if {self.visit(initial.condition)}:\n')

        self.count_tabs += 1

        for statement in initial.body:
            if isinstance(statement, Expression):
                self.write(self.visit(statement) + "\n")
            else:
                self.visit(statement)

        self.count_tabs -= 1

        total = len(node.ifs)

        if total > 1:
            for i in range(1, total):
                self.visit(node.ifs[i])

        if node.else_body is not None:
            self.write("else:\n")
            self.count_tabs += 1
            for statement in node.else_body:
                if isinstance(statement, Expression):
                    self.write(self.visit(statement) + "\n")
                else:
                    self.visit(statement)

            self.count_tabs -= 1

    @visitor(If)
    def visit(self, node: If):

        self.write(f'elif {self.visit(node.condition)}:\n')

        self.count_tabs += 1

        for statement in node.body:
            if isinstance(statement, Expression):
                self.write(self.visit(statement) + "\n")
            else:
                self.visit(statement)
        self.count_tabs -= 1

    @visitor(WhileDef)
    def visit(self, node: WhileDef):

        self.write(f'while {self.visit(node.condition)}:\n')

        self.count_tabs += 1

        for statement in node.body:
            if isinstance(statement, Expression):
                self.write(self.visit(statement) + "\n")
            else:
                self.visit(statement)
        self.count_tabs -= 1

    @visitor(Decl)
    def visit(self, node: Decl):
        self.write(f'{node.name} = {self.visit(node.expression)}\n')

    @visitor(Assign)
    def visit(self, node: Assign):
        self.write(f'{node.name} = {self.visit(node.expression)}\n')

    @visitor(Return)
    def visit(self, node: Return):
        if node.expression is None:
            self.write('return\n')
        else:
            self.write(f'return {self.visit(node.expression)}\n')

    @visitor(Continue)
    def visit(self, node: Continue):
        self.write('continue\n')

    @visitor(Break)
    def visit(self, node: Break):
        self.write('break\n')

    @visitor(BinaryExpression)
    def visit(self, node: BinaryExpression):

        left = self.visit(node.left)
        right = self.visit(node.right)

        return f'{left} {node.op} {right}'

    @visitor(AritmeticBinaryExpression)
    def visit(self, node: BinaryExpression):

        left = self.visit(node.left)
        right = self.visit(node.right)

        return f'{left} {node.op if not node.op in self.translation else self.translation[node.op]} {right}'

    @visitor(TernaryExpression)
    def visit(self, node: TernaryExpression):

        left = self.visit(node.left)
        condition = self.visit(node.condition)
        right = self.visit(node.right)

        return f'{left} if {condition} else {right}'

    @visitor(Primary)
    def visit(self, node: Primary):

        exp = self.visit(node.expression)
        if node.args is None:
            return f'{exp}.{node.name}'
        else:
            args = ', '.join(self.visit(e) for e in node.args)

            return f'{exp}({args})'

    @visitor(Variable)
    def visit(self, node: Variable):
        return node.name

    @visitor(Number)
    def visit(self, node: Number):
        return node.value

    @visitor(Bool)
    def visit(self, node: Bool):
        return node.value

    @visitor(MyNone)
    def visit(self, node: MyNone):
        return 'None'

    @visitor(MyList)
    def visit(self, node: MyList):
        args = ', '.join(self.visit(e) for e in node.inner_list)
        return f'[{args}]'