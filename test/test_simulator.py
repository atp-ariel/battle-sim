from src.core.simulator.sides import Side
from src.core.simulator.simulator import Simulator
from src.core.maps.genetic import GAT_Generator
from src.core.maps.heightmap import HeightMap
from src.core.bs_objects import LandUnit
from src.core.maps.maps import LandMap
from random import randint as r
from numpy import array
import pytest
from collections import namedtuple

skip_if = namedtuple("SkipIf", "condition reason")
SKIP_BIGGER = skip_if(True, "large case delay")


@pytest.mark.skipif(SKIP_BIGGER.condition, reason=SKIP_BIGGER.reason)
def test_simulator():

    # Build map
    sea = 0.45
    n = 50
    maps = GAT_Generator(.95, (n, n), sea_level=sea)()
    maps = LandMap(n, n, maps, sea, [])

    # Side configuration
    s1 = Side(1, [])
    s2 = Side(2, [])


    # Units creation
    for i in range(10):
        s1.add_unit(LandUnit(i+1,r(1,10),r(1,10),r(1,10),r(1,10),r(1,10),r(1,10),r(1,1),r(1,2),1,r(1,10),0,True,True))
        s1.units[-1].put_in_cell(maps, 0, i)

    for i in range(10):
        s2.add_unit(LandUnit(i+10+1,r(1,10),r(1,10),r(1,10),r(1,10),r(1,10),r(1,10),r(1,1),r(1,2),1,r(1,10),0,True,True))
        s2.units[-1].put_in_cell(maps, n-1, i)


    S = Simulator(maps, [s1, s2], 10)

    S.simulator_by_turns()

def test_small_simulator():
    n = 4
    sea = 0.45

    maps = HeightMap.build_from_map(array([
        [.43, .458, .489, .53],
        [.47, .49, .54, .58],
        [.495, .51, .581, .62],
        [.49, .55, .61, .67]
    ]))

    maps = LandMap(n, n, maps, sea, [])

    maps.sides.append(Side(1, []))
    maps.sides.append(Side(2, []))

    s1: Side = maps.sides[0]
    s2: Side = maps.sides[1]

    # Side 1

    s1.units.append(LandUnit(1, 10, 9, 10, 9, 9, 1, 2, 1, 5, 6, 0, True, True))
    s1.units[-1].put_in_cell(maps, 0,1)
    s1.units.append(LandUnit(2, 6, 5, 7, 9, 3, 1, 1, 1, 2, 10, 0, True, True ))
    s1.units[-1].put_in_cell(maps, 0, 2)

    # Side 2
    s2.units.append(LandUnit(3, 2, 3,  10, 3, 5, 1, 1,1, 1, 5, 0, True, True))
    s2.units[-1].put_in_cell(maps, 2, 3)
    s2.units.append(LandUnit(4, 7, 8,  8, 4, 6, 1, 2, 1, 10, 4, 0, True, True))
    s2.units[-1].put_in_cell(maps, 3, 3)

    S = Simulator(maps, [s1, s2], 10)

    S.simulator_by_turns()