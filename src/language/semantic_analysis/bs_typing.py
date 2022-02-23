
"""
1-Recolectar los tipos del AST en diccionario
2-Recolectar Métodos de tipos
3-Verificar la semántica
"""


class battle_sim_typing:
    def __init__(self, program, collector, builder, definer,checker, context):
        self.program=program
        self.collector=collector
        self.builder=builder
        self.definer=definer
        self.checker=checker
        self.context=context

    def __call__(self):
        self.context.create_type("Type",acces=False)
        self.context.create_type("number",acces=False)
        self.context.create_type("bool",acces=False)
        
        t=self.context.create_type("List",acces=False)[1]
        t.define_func("append", "void", ["x"], ["Type"])
        t.define_func("remove", "void", ["x"], ["Type"])
        
        self.context.create_type("LandMap",args=["no_rows", "no_columns", "passable_map", "height_map", "sea_height"],type_args=["number","number","List","List","number"])
        
        t=self.context.create_type("BSObject",args=["id","life_points","defense"],type_args=["number","number","number"],acces=False)[1]
        
        t.define_var("id", "number")
        t.define_var("life_points", "number")
        t.define_var("defense","number")
        t.define_func("take_damage","void",["damage"],["number"])
        t.define_func("put_in_cell", "void", ["map","row","col"], ["LandMap","number","number"])        
    
        t=self.context.create_type("Cell", args=["passable","row" , "column", "height"],type_args=["number","number","number","number"],acces=False)[1]
        t.define_var("row","number")
        t.define_var("col", "number")
        t.define_var("passable", "number")
        t.define_var("height", "number")
        
        self.context.create_type("StaticObject", args=["id","life_points","defense"], type_args=["number","number","number"],parent="BSObject",acces=False)
        
        t=self.context.create_type("BSUnit",args=["id","life_points","defense","attack","moral","ofensive","min_range","max_range","radio","vision","intelligence","recharge_turns","solidarity","movil"],type_args=["number","number","number","number","number","number","number","number","number","number","number","number","bool","bool"], parent="BSObject",acces=False)[1]
        
        t.define_var("attack","number")
        t.define_var("moral", "number")
        t.define_var("ofensive", "number")
        t.define_var("min_range", "number")
        t.define_var("max_range", "number")
        t.define_var("radio", "number")
        t.define_var("vision", "number")
        t.define_var("intelligence", "number")
        t.define_var("recharge_turns", "number")
        t.define_var("recharging_turns", "number")
        t.define_var("solidarity","bool")
        t.define_var("movil", "bool")       
        
        t.define_func("calculate_distance","number",["cell1","cell2"],["Cell","Cell"])
        t.define_func("nearby_friend","bool",["cell"],["Cell"])
        t.define_func("enemy_in_range","List",["cell"],["Cell"])
        t.define_func("in_range_of_enemy","number",["cell"],["Cell"])
        t.define_func("move_cost_calculate","number",["cell"],["Cell"])
        t.define_func("enemy_cost_calculate","number",["enemy"],["BSUnit"])
        t.define_func("friend_in_danger","bool",["cell"],["Cell"])
        t.define_func("enemy_to_attack","BSUnit",[],[])
        t.define_func("take_damage","void",["damage"],["number"])
        t.define_func("attack_enemy","void",["enemy"],["BSUnit"])
        t.define_func("move_to_cell","void",["cell"],["Cell"])
        t.define_func("turn","void",[],[])

        self.context.create_type("LandUnit", args=["id","life_points","defense","attack","moral","ofensive","min_range","max_range","radio","vision","intelligence","recharge_turns","solidarity","movil"],type_args=["number","number","number","number","number","number","number","number","number","number","number","number","bool","bool"],parent="BSUnit",acces=False)[1]
        
        self.context.create_type("NavalUnit", args=["id","life_points","defense","attack","moral","ofensive","min_range","max_range","radio","vision","intelligence","recharge_turns","solidarity","movil"],type_args=["number","number","number","number","number","number","number","number","number","number","number","number","bool","bool"], parent="BSUnit", acces=False)[1]
        
        t=self.context.create_type("Side", ["id", "units"], ["number", "List"])[1]

        t.define_var("id", "number")
        t.define_var("units", "List")
        t.define_var("no_own_units_defeated", "number")
        t.define_var("no_enemy_units_defeated", "number")
        t.define_func("add_unit", "void", ["unit"], ["BSUnit"])
        t.define_func("remove_unit", "void", ["unit"], ["BSUnit"])

        
        t=self.context.create_type("Simulator",["map","Sides","turns", "interval"],["LandMap","List","number","number"])[1]
        t.define_func("start", "void", [], [])
        
        self.context.define_func("build_random_map", "LandMap", ["percent","rows","cols"], ["number","number","number"])
        
        self.collecting()
        self.building()
        self.define_context()
        self.checking()

    def collecting(self):
      self.collector.visit(self.program)
        

    def building(self):
        self.builder.visit(self.program)
      
    def define_context(self):
        self.definer.visit(self.program)
    
    def checking(self):
        self.checker.visit(self.program)

