from abc import ABC, abstractmethod
from ..maps import *


class BSObject(ABC):

    @abstractmethod
    def __init__(self, id: int, life_points: int, defense: int):
        self.id = id
        self.life_points = life_points
        self.defense = defense
        self.map = None
        self.cell : Cell = None

    # poner en celda el objeto
    def put_in_cell(self, map: Map, type: str, row: int, col: int):
        if map[row][col].type != type:
            self.life_points=0
        else:
            if map[row][col].bs_object != None:
                raise Exception("Busy cell")
            map[row][col].bs_object = self
            self.map = map
            self.cell = map[row][col]

    # tomar danio
    def take_damage(self, damage: float):
        self.life_points -= damage / self.defense
        if self.life_points <= 0:
            self.life_points = 0
            self.cell.bs_object = None


class StaticObject(BSObject):

    def __init__(self, id: int, life_points: float, defense: float):
        BSObject.__init__(self,id, life_points, defense)

    def put_in_cell(self, map: Map, row: int, col: int):
        BSObject.put_in_cell(self, map, "earth", row, col)