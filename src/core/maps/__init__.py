from .genetic import *
from .heightmap import *
from .maps import *

def build_random_map(percentage: float, rows: int, cols: int) -> LandMap:
    generator = GAT_Generator(percentage, (rows, cols))
    hm = generator()

    passable = hm.__map__ * 10

    return LandMap(rows, cols, passable, hm, 0.45)
