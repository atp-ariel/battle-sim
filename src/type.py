import visitor

"""
1-Recolectar los tipos del AST en diccionario
2-Recolectar Métodos de tipos
3-Verificar la semántica
"""
class battle_sim_typing:
    def __init__(self,program,collector,builder,checker,context):
        self.program=program
        self.collector=collector
        self.builder=builder
        self.checker=checker
        self.context=context

    def collecting(self):
        self.collector.visit(self.program)

    def building(self):
        self.builder.visit(self.program)

    def checking(self):
        self.checker.visit(self.program)

