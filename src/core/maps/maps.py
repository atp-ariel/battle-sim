from abc import ABC, abstractclassmethod
from typing import List

class Cell:

    def __init__(self, passable : float, type : str, row : int, column: int, height: float):
        self.passable = passable
        self.type = type
        self.row = row
        self.col = column
        self.height = height
        self.bs_object = None
        
    def __hash__(self):
        return hash(f'{self.row} {self.col}')
    
    def __eq__(self, o):
        if isinstance(o, Cell):
            return self.row == o.row and self.col == o.col
        return False

    def __str__(self):
        return f"({self.row}, {self.col})"
    
    def __repr__(self) -> str:
        return self.__str__()

class Map(ABC):

    @abstractclassmethod
    def __init__(self, no_rows : int, no_columns:int):
        self.no_rows = no_rows
        self.no_columns = no_columns
        self.matrix = None

    def __getitem__(self, i):
        return self.matrix[i]


class LandMap(Map):

    def __init__(self, no_rows, no_columns, passable_map, height_map, sea_height):
        Map.__init__(no_rows, no_columns)
        self.matrix = [[Cell(passable_map[i][j], "earth" if height_map[i][j] > sea_height else "water",
                             i, j, height_map[i][j]) for j in range(no_columns)] for i in range(no_rows)]
