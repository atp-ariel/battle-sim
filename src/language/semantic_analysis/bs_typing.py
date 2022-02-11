
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
        self.context.create_type("MyNone")

        self.context.create_type("List")
        t = self.context.get_type_object("List")
        t.define_method("append", "MyNone", ["x"], ["Type"])
        t.define_method("remove", "MyNone", ["x"], ["Type"])
        
        self.context.create_func("super", "BSObject", [],[])

        self.context.create_type("BSObject")
        self.context.create_type("BSUnit", parent="BSObject")

        self.context.create_type("StaticObject", parent="BSObject")
        t = self.context.get_type_object("StaticObject")
        t.define_method("put_in_cell", "MyNone", ["self", "arg1","arg2","arg3"], ["StaticObject","LandMap","number","number"])

        self.context.create_type("LandUnit", parent="BSUnit")
        self.context.get_type_object("LandUnit").define_method("put_in_cell", "MyNone", ["self", "arg1","arg2","arg3"], ["LandUnit","LandMap","number","number"])
        
        self.context.create_type("NavalUnit", parent="BSUnit")
        self.context.get_type_object("NavalUnit").define_method("put_in_cell", "MyNone", ["self", "arg1","arg2","arg3"], ["NavalUnit", "LandMap","number","number"])
        
        self.context.create_type("LandMap")
        
        self.context.create_type("Side")

        t = self.context.get_type_object("Side", ["id", "units"], ["number", "List"])
        t.define_attribute("id", "number")
        t.define_attribute("units", "List")
        t.define_attribute("no_own_units_defeated", "number")
        t.define_attribute("no_enemy_units_defeated", "number")
        t.define__method("add_unit", "MyNone", ["self", "unit"], ["Side", "BSUnit"])
        t.define__method("remove_unit", "MyNone", ["self", "unit"], ["Side", "BSUnit"])

        
        self.context.create_type("Simulator",["map","Sides","arg1", "arg2"],["LandMap","List","number","number"])
        self.context.get_type_object("Simulator").define_method("start", "MyNone", [], [])
        
        self.context.define_func("build_random_map", "LandMap", ["map","arg2","arg3"], ["LandMap","number","number"])
        
        
        self.collecting()
        self.building()
        self.checking()

    def collecting(self):
      self.collector.visit(self.program)
        

    def building(self):
        self.builder.visit(self.program)

    def checking(self):
        self.checker.visit(self.program)

