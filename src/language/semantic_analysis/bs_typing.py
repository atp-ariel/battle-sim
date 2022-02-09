
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
        self.context.create_type("LandUnit")
        self.context.create_type("LandMap")
        self.context.create_type("Side")
        self.context.create_type("MyNone")
        self.context.create_type("Simulator",["map","Sides","arg1", "arg2"],["LandMap","List","number","number"])
        self.context.define_func("build_random_map", "LandMap", ["map","arg2","arg3"], ["LandMap","number","number"])
        self.context.get_type_object("LandUnit").define_method("put_in_cell", "MyNone", ["arg1","arg2","arg3"], ["number","number","number"])
        self.context.get_type_object("Simulator").define_method("start", "MyNone", [], [])
        
        self.collecting()
        self.building()
        self.checking()

    def collecting(self):
      self.collector.visit(self.program)
        

    def building(self):
        self.builder.visit(self.program)

    def checking(self):
        self.checker.visit(self.program)

