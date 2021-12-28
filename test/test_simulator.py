from src.core.utils import Simulator, Side
from src.core.genetic import GAT_Generator
from src.core.bs_objects import BSLandUnit
from src.core.maps import LandMap
from random import randint as r

def test_simulator():

    # Build map
    sea = 0.45
    n = 50
    maps = GAT_Generator(.9, (n, n), sea_level=sea)()
    maps.get_img().show()
    maps = LandMap(n, n, maps, sea, [])

    # Side configuration
    s1 = Side(1, "s1")
    s2 = Side(2, "s2")


    # Units creation
    for i in range(10):
        s1.add_unit(BSLandUnit(i+1,r(1,10),r(1,10),s1,r(1,10),r(1,10),r(1,10),r(1,10),r(1,1),r(1,2),1,r(1,10),0,True,True))
        s1.units[-1].put_in_cell(maps, 0, i)

    for i in range(10):
        s2.add_unit(BSLandUnit(i+10+1,r(1,10),r(1,10),s1,r(1,10),r(1,10),r(1,10),r(1,10),r(1,1),r(1,2),1,r(1,10),0,True,True))
        s2.units[-1].put_in_cell(maps, n-1, i)


    S = Simulator(maps, maps, [s1, s2], 10)

    S.simulator_by_turns()