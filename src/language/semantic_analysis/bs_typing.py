
"""
1-Recolectar los tipos del AST en diccionario
2-Recolectar Métodos de tipos
3-Verificar la semántica
"""


class battle_sim_typing:
    def __init__(self, program, collector, builder, checker, context):
        self.program=program
        self.collector=collector
        self.builder=builder
        self.checker=checker
        self.context=context

    def __call__(self):
        self.context.create_type("number")
        self.context.create_type("bool")
        self.context.create_type("List")
        self.collecting()
        self.building()
        self.checking()

    def collecting(self):
        self.collector.visit(self.program)

    def building(self):
        self.builder.visit(self.program)

    def checking(self):
        self.checker.visit(self.program)

