from random import randint as r
from .core.maps.heightmap import HeightMap
from numpy import array
from .core.maps.maps import LandMap
from .core.simulator.sides import Side
from .core.simulator.simulator import Simulator
from .core.bs_objects import LandUnit, StaticObject
from .core.maps.genetic import GAT_Generator

class Spartano(LandUnit):
    def __init__(self, id: int):
        LandUnit.__init__(self, id, life_points=10, defense=8, attack=9, moral=r(1, 10), ofensive=7, min_range=1, max_range=6, radio=1, vision=7, intelligence=r(1,10), recharge_turns=0, solidarity=True, movil=True )

class Marine(LandUnit):
    def __init__(self, id: int):
        LandUnit.__init__(self, id, life_points=10, defense=7, attack=10, moral=10, ofensive=7, min_range=1, max_range=6, radio=2, vision=7, intelligence=r(1,10), recharge_turns=0, solidarity=True, movil=True )

class Tree(StaticObject):
    def __init__(self, id):
        StaticObject.__init__(self, id, 10, 1)

n = 8
sea = 0.45

# maps = HeightMap.build_from_map(array([
#     [.43, .458, .489, .53],
#     [.47, .49, .54, .58],
#     [.495, .51, .581, .62],
#     [.49, .55, .61, .67]
# ]))

# maps = HeightMap.build_from_map(array([
#     [.458, .458, .458, .458,.458, .458, .458, .458],
#     [.458, .458, .458, .458,.458, .458, .458, .458],
#     [.458, .458, .458, .458,.458, .458, .458, .458],
#     [.458, .458, .458, .458,.458, .458, .458, .458],
#     [.458, .458, .458, .458,.458, .458, .458, .458],
#     [.458, .458, .458, .458,.458, .458, .458, .458],
#     [.458, .458, .458, .458,.458, .458, .458, .458],
#     [.458, .458, .458, .458,.458, .458, .458, .458]
# ]))

maps = GAT_Generator(0.65, (8, 8))()

passable = maps.__map__ * 10

maps = LandMap(n, n, passable, maps, sea)

s1: Side = Side(1, [])

# Side 1
s1.add_unit(Spartano(1))
s1.units[-1].put_in_cell(maps, 0,0)
s1.add_unit(Spartano(2))
s1.units[-1].put_in_cell(maps, 0, 2)
s1.add_unit(Spartano(3))
s1.units[-1].put_in_cell(maps, 0,3)

# Side 2
m1 = Marine(4)
m2 = Marine(5)

m1.put_in_cell(maps, 7, 3)
m2.put_in_cell(maps, 7, 4)

s2: Side = Side(2, [m1, m2])

Tree(6).put_in_cell(maps, 1, 0)
Tree(7).put_in_cell(maps, 1, 1)
Tree(8).put_in_cell(maps, 0, 1)

S = Simulator(maps, [s1, s2], 20, 1)

S.simulating_k_turns()

result = [
    ["Bando", "Bajas amigas", "Bajas enemigas"],
    [s1.name, s1.no_own_units_defeated, s1.no_enemy_units_defeated ],
    [s2.name, s2.no_own_units_defeated, s2.no_enemy_units_defeated ]
]

print(result[0])
print(result[1])
print(result[2])
