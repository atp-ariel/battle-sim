from .core.maps.heightmap import HeightMap
from numpy import array
from .core.maps.maps import LandMap
from .core.simulator.sides import Side
from .core.simulator.simulator import Simulator
from .core.bs_objects import BSLandUnit

n = 4
sea = 0.45

maps = HeightMap.build_from_map(array([
    [.43, .458, .489, .53],
    [.47, .49, .54, .58],
    [.495, .51, .581, .62],
    [.49, .55, .61, .67]
]))
maps.get_img().show()

maps = LandMap(n, n, maps, sea, [])

maps.sides.append(Side(1, "s1"))
maps.sides.append(Side(2, "s2"))

s1: Side = maps.sides[0]
s2: Side = maps.sides[1]

# Side 1

s1.units.append(BSLandUnit(1, 10, 9, s1, 10, 9, 9, 1, 2, 1, 5, 6, 0, True, True))
s1.units[-1].put_in_cell(maps, 0,1)
s1.units.append(BSLandUnit(2, 6, 5, s1, 7, 9, 3, 1, 1, 1, 2, 10, 0, True, True ))
s1.units[-1].put_in_cell(maps, 0, 2)

# Side 2
s2.units.append(BSLandUnit(3, 2, 3, s2, 10, 3, 5, 1, 1,1, 1, 5, 0, True, True))
s2.units[-1].put_in_cell(maps, 2, 3)
s2.units.append(BSLandUnit(4, 7, 8, s2, 8, 4, 6, 1, 2, 1, 10, 4, 0, True, True))
s2.units[-1].put_in_cell(maps, 3, 3)

S = Simulator(maps, maps, [s1, s2], 10)

S.simulator_by_turns()