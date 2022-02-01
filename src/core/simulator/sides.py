class Side:
    @property
    def no_units(self) -> int:
        return len(self.units)

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.units = []
        self.no_own_units_defeated = 0
        self.no_enemy_units_defeated = 0

    def add_unit(self, unit):
        unit.side = self
        self.units.append(unit)

    def remove_unit(self, unit):
        unit.side = None
        self.units.remove(unit)

    def get_units(self):
        return self.units

    def __iter__(self):
        for unit in self.units:
            yield unit

    def __eq__(self, o):
        if isinstance(o, Side):
            return self.id==o.id
        return False