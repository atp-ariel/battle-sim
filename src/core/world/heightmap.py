from typing import List, Optional, Tuple, Union
from numpy import zeros, array, amin, amax, floor, uint8
from PIL import Image

class HeightMap:
    @classmethod
    def build_from_map(cls, map):
        new = HeightMap(map.shape)
        for i in range(new.shape[0]):
            for j in range(new.shape[1]):
                new[i][j] = map[i][j]
        return new
    
    @property
    def shape(self) -> Tuple[int, int]:
        return self.__map__.shape

    @property
    def min(self) -> float:
        return amin(self.__map__)
    
    @property
    def max(self) -> float:
        return amax(self.__map__)

    def __init__(self, shape: Tuple[int, int]):
        self.__map__ = zeros(shape)
    
    def __getitem__(self, index) -> List:
        return self.__map__[index]

    def __add__(self, other):
        new = self.__map__ + other.__map__
        return HeightMap.build_from_map(new)

    def __iadd__(self, other: float):
        self.__map__ += other
        return self

    def __isub__(self, other: float):
        self.__map__ -= other
        return self

    def __imul__(self, other: float):
        self.__map__ *= other
        return self

    def normalize(self):
        min = self.min
        max = self.max

        for i in range(len(self.__map__)):
            for j in range(len(self.__map__[i])):
                self.__map__[i][j] = (self.__map__[i][j] - min)/(max - min)
        return self

    def get_img(self):
        img = floor(self.__map__ * 255) # <- Normalize world first
        img = img.astype(uint8)
        return Image.fromarray(img, mode='L')