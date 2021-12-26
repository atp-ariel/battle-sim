from src.core.utils import Simulator, Side
from src.core.genetic import GAT_Generator
from src.core.bs_objects import BSLandUnit
from src.core.maps import LandMap
from random import randint as r

def test_simulator():

    # Build map
    sea = 0.45
    n = 50
    maps = GAT_Generator(.2, (n, n), sea_level=sea)()
    maps.get_img().show()
    maps = LandMap(n, n, maps, sea, [])

    # Side configuration
    s1 = Side(1, "s1")
    s2 = Side(2, "s2")


    # Units creation
    for i in range(10):
        s1.add_unit(BSLandUnit(i + 1, 10, r(1, 10), s1, r(1, 10), r(1, 10),
                            r(1, 3), r(3, 8), r(1, 8), r(1, 9), r(1, 10), r(5, 10), r(1, 10), r(1,10)))


    for i in range(10):
                            r(1, 3), r(3, 8), r(1, 8), r(1, 9), r(1, 10), r(5, 10), r(1, 10), r(1,10)))

    S = Simulator(maps, maps, [s1, s2], 10)

    S.simulator_by_turns()