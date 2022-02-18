
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
        #self.definer=definer

    def __call__(self):
        self.context.create_type("Type",acces=False)
        self.context.create_type("number",acces=False)
        self.context.create_type("bool",acces=False)
        #self.context.create_type("None",acces=False)
        self.context.create_type("LandMap",args=["no_rows", "no_columns", "passable_map", "height_map", "sea_height"],type_args=["number","number","List","List","number"])

        self.context.create_type("List",acces=False)
        t = self.context.get_type_object("List")
        t.define_method("append", "void", ["x"], ["Type"])
        t.define_method("remove", "void", ["x"], ["Type"])
        
        t=self.context.create_type("BSObject",args=["id","life_points","defense"],type_args=["number","number","number"],acces=False)[1]
        self.context.define_func("super", "BSObject", [],[])
        t.define_func("take_damage","void",["self","damage"],["BSObject","number"])

        
        t=self.context.create_type("Cell", args=["passable","row" , "column", "height"],type_args=["number","number","number","number"],acces=False)
        
        t=self.context.create_type("BSUnit",args=["id","life_points","defense","attack","moral","ofensive","min_range","max_range","radio","vision","intelligence","recharge_turns","solidarity","movil"],type_args=["number","number","number","number","number","number","number","number","number","number","number","number","bool","bool"], parent="BSObject",acces=False)[1]
        t.define_func("calculate_distance","number",["self","cell1","cell2"],["BSUnit","Cell","Cell"])
        t.define_func("nearby_friend","bool",["self","cell"],["BSUnit","Cell"])
        t.define_func("enemy_in_range","List",["self","cell"],["BSUnit","Cell"])
        t.define_func("in_range_of_enemy","number",["self","cell"],["BSUnit","Cell"])
        t.define_func("move_cost_calculate","number",["self","cell"],["BSUnit","Cell"])
        t.define_func("enemy_cost_calculate","number",["self","enemy"],["BSUnit","BSUnit"])
        t.define_func("friend_in_danger","bool",["self","cell"],["BSUnit","Cell"])
        t.define_func("enemy_to_attack","BSUnit",["self"],["BSUnit"])
        t.define_func("take_damage","void",["self","damage"],["BSUnit","Number"])
        t.define_function("attack_enemy","void",["self","enemy"],["BSUnit","BSUnit"])
        t.define_function("move_to_cell","void",["self","cell"],["BSUnit","Cell"])


        self.context.create_type("StaticObject", args=["id","life_points","defense"], type_args=["number","number","number"],parent="BSObject",acces=False)
        t = self.context.get_type_object("StaticObject")
        t.define_method("put_in_cell", "void", ["self", "arg1","arg2","arg3"], ["StaticObject","LandMap","number","number"])

        t=self.context.create_type("LandUnit", args=["id","life_points","defense","attack","moral","ofensive","min_range","max_range","radio","vision","intelligence","recharge_turns","solidarity","movil"],type_args=["number","number","number","number","number","number","number","number","number","number","number","number","bool","bool"],parent="BSUnit",acces=False)[1]
        self.context.get_type_object("LandUnit").define_method("put_in_cell", "void", ["self", "arg1","arg2","arg3"], ["LandUnit","LandMap","number","number"])
        t.define_func("calculate_distance","number",["self","cell1","cell2"],["LandUnit","Cell","Cell"])
        t.define_func("nearby_friend","bool",["self","cell"],["LandUnit","Cell"])
        t.define_func("enemy_in_range","List",["self","cell"],["LandUnit","Cell"])
        t.define_func("in_range_of_enemy","number",["self","cell"],["LandUnit","Cell"])
        t.define_func("move_cost_calculate","number",["self","cell"],["LandUnit","Cell"])
        t.define_func("enemy_cost_calculate","number",["self","enemy"],["LandUnit","LandUnit"])
        t.define_func("friend_in_danger","bool",["self","cell"],["LandUnit","Cell"])
        t.define_func("enemy_to_attack","LandUnit",["self"],["LandUnit"])
        t.define_func("take_damage","void",["self","damage"],["LandUnit","Number"])
        t.define_function("attack_enemy","void",["self","enemy"],["LandUnit","LandUnit"])
        t.define_function("move_to_cell","void",["self","cell"],["LandUnit","Cell"])
        t.define_function("turn","void",["self"],["LandUnit"])
        
        t=self.context.create_type("NavalUnit", args=["id","life_points","defense","attack","moral","ofensive","min_range","max_range","radio","vision","intelligence","recharge_turns","solidarity","movil"],type_args=["number","number","number","number","number","number","number","number","number","number","number","number","bool","bool"], parent="BSUnit", acces=False)[1]
        self.context.get_type_object("NavalUnit").define_method("put_in_cell", "void", ["self", "arg1","arg2","arg3"], ["NavalUnit", "LandMap","number","number"])
        t.define_func("calculate_distance","number",["self","cell1","cell2"],["NavalUnit","Cell","Cell"])
        t.define_func("nearby_friend","bool",["self","cell"],["NavalUnit","Cell"])
        t.define_func("enemy_in_range","List",["self","cell"],["NavalUnit","Cell"])
        t.define_func("in_range_of_enemy","number",["self","cell"],["NavalUnit","Cell"])
        t.define_func("move_cost_calculate","number",["self","cell"],["NavalUnit","Cell"])
        t.define_func("enemy_cost_calculate","number",["self","enemy"],["NavalUnit","NavalUnit"])
        t.define_func("friend_in_danger","bool",["self","cell"],["NavalUnit","Cell"])
        t.define_func("enemy_to_attack","NavalUnit",["self"],["NavalUnit"])
        t.define_func("take_damage","void",["self","damage"],["NavalUnit","Number"])
        t.define_function("attack_enemy","void",["self","enemy"],["NavalUnit","NavalUnit"])
        t.define_function("move_to_cell","void",["self","cell"],["NavalUnit","Cell"])
        t.define_function("turn","void",["self"],["NavalUnit"])
        
        self.context.create_type("Side", ["id", "units"], ["number", "List"])

        t = self.context.get_type_object("Side")
        t.define_attribute("id", "number")
        t.define_attribute("units", "List")
        t.define_attribute("no_own_units_defeated", "number")
        t.define_attribute("no_enemy_units_defeated", "number")
        t.define_method("add_unit", "void", ["self", "unit"], ["Side", "BSUnit"])
        t.define_method("remove_unit", "void", ["self", "unit"], ["Side", "BSUnit"])

        
        t=self.context.create_type("Simulator",["map","Sides","arg1", "arg2"],["LandMap","List","number","number"])[1]
        self.context.get_type_object("Simulator").define_method("start", "void", [], [])
        
        self.context.define_func("build_random_map", "LandMap", ["arg1","arg2","arg3"], ["number","number","number"])
        
        self.collecting()
        self.building()
        #self.define_context()
        self.checking()

    def collecting(self):
      self.collector.visit(self.program)
        

    def building(self):
        self.builder.visit(self.program)
     
    """   
    def define_context(self):
        self.definer.visit(self.program)
    """
    
    def checking(self):
        self.checker.visit(self.program)

