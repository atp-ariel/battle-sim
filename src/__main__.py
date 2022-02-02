from .core.maps.heightmap import HeightMap
from numpy import array
from .core.maps.maps import LandMap
from .core.simulator.sides import Side
from .core.simulator.simulator import Simulator
from .core.bs_objects import LandUnit


n = 8
sea = 0.45

# maps = HeightMap.build_from_map(array([
#     [.43, .458, .489, .53],
#     [.47, .49, .54, .58],
#     [.495, .51, .581, .62],
#     [.49, .55, .61, .67]
# ]))
maps = HeightMap.build_from_map(array([
    [.458, .458, .458, .458,.458, .458, .458, .458],
    [.458, .458, .458, .458,.458, .458, .458, .458],
    [.458, .458, .458, .458,.458, .458, .458, .458],
    [.458, .458, .458, .458,.458, .458, .458, .458],
    [.458, .458, .458, .458,.458, .458, .458, .458],
    [.458, .458, .458, .458,.458, .458, .458, .458],
    [.458, .458, .458, .458,.458, .458, .458, .458],
    [.458, .458, .458, .458,.458, .458, .458, .458]
]))
maps = LandMap(n, n, maps, sea, [])

maps.sides.append(Side(1, []))
maps.sides.append(Side(2, []))

s1: Side = maps.sides[0]
s2: Side = maps.sides[1]

# Side 1

s1.add_unit(LandUnit(1, life_points=10, defense=9, attack=6, moral=9, ofensive=9, min_range=1, max_range=2, radio=1, vision=5, intelligence=6, recharge_turns=0, solidarity=True, movil=True))
s1.units[-1].put_in_cell(maps, 0,1)
s1.add_unit(LandUnit(2, life_points=10, defense=9, attack=2, moral=7, ofensive=8, min_range=1, max_range=2, radio=2, vision=5, intelligence=6, recharge_turns=0, solidarity=True, movil=True))
s1.units[-1].put_in_cell(maps, 0, 2)

# Side 2
s2.add_unit(LandUnit(3, life_points=10, defense=9, attack=4, moral=7, ofensive=8, min_range=1, max_range=2, radio=1, vision=5, intelligence=6, recharge_turns=0, solidarity=True, movil=True))
s2.units[-1].put_in_cell(maps, 1, 1)
s2.add_unit(LandUnit(4, life_points=10, defense=9, attack=1, moral=7, ofensive=8, min_range=1, max_range=2, radio=1, vision=5, intelligence=6, recharge_turns=0, solidarity=True, movil=True))
s2.units[-1].put_in_cell(maps, 7, 7)

S = Simulator(maps, [s1, s2], 20)

S.simulator_by_turns()