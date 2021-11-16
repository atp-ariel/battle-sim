from math import prod
from typing import List, Tuple
from heightmap import HeightMap
from numpy import  sum, array, vectorize, zeros, linspace, meshgrid
from random import sample, randint
import noise

class GAT_Generator:
    @property
    def poblation(self) -> List:
        return self.__poblation__

    def __init__(self, percentage: float, shape: Tuple[int, int], sea_level=0.5, poblation_size=10, iter=100, merge_weight=0.95, tol=0.03):
        self.percentage = percentage

        self.__shape__ = shape
        self.__poblation_size__ = poblation_size
        self.__iter = iter

        self.__poblation__ = []
        self.__fitness__ = []
        self.__merge__ = merge_weight
        self.__sea__ = sea_level

        self.__tol__ = tol

    def __call__(self, verbose=False) -> HeightMap:
        self._generate_poblation()
        self._calculate_fitness()

        self.__poblation__ = array(sorted(self.__poblation__, key=self.fit_func, reverse=True))
        self.__fitness__ = array(sorted(self.__fitness__, reverse=True))
        
        i = 0
        while i < self.__iter:
            if self.__fitness__[0] > self.percentage - self.__tol__ and self.__fitness__[0] < self.percentage + self.__tol__:
                break

            new_poblation = []

            # generate new poblation
            for k in range(self.__poblation_size__):
                # Select
                parents = self._selection()
                # Merge
                child = self._merge(parents)
                # Mutate
                child = self._mutate(child)

                # add to new poblation 
                new_poblation.append(child)

            # convert new poblation to numpy array
            new_poblation = sorted(new_poblation, key=self.fit_func, reverse=True)
            self.__poblation__ = array(new_poblation) 
            self._calculate_fitness()
            self.__fitness__ = array(sorted(self.__fitness__, reverse=True))
            
            i += 1
        if verbose:
            print(f"GAT Generator:\nfitness:\t{self.__fitness__[0]}\niter:\t{i}")
        return self.__poblation__[0]
            
    def fit_func(self, heightmap: HeightMap):
        count = sum(sum(heightmap.__map__ > self.__sea__))
        per = count / prod(self.__shape__)
        return per if per < self.percentage else 0

    def __generate_member(self) -> HeightMap:
        world = zeros(self.__shape__)

        x_idx = linspace(0, 1, self.__shape__[0])
        y_idx = linspace(0, 1, self.__shape__[1])
        world_x, world_y = meshgrid(x_idx, y_idx)

        world = vectorize(noise.pnoise2)(world_x/.5,
                                world_y/.5,
                                octaves=6,
                                # accidentalidad
                                persistence=.1,
                                lacunarity=2.,
                                repeatx=1024,
                                repeaty=1024,
                                base=randint(0, 1024))
        world = HeightMap.build_from_map(world)
        world.normalize()
        #world.get_img().show()
        return world

    def _generate_poblation(self):
        for i in range(self.__poblation_size__):
            self.__poblation__.append(self.__generate_member())
        self.__poblation__ = array(self.__poblation__)

    def _calculate_fitness(self):
        fitness = []
        for item in self.poblation:
            fitness.append(self.fit_func(item))
        self.__fitness__ = array(fitness)
    
    def _selection(self) -> Tuple[HeightMap, HeightMap]:
        # Seleccion competitiva
        # index = sample(range(0, self.__poblation_size__), 4)
        # tournment = self.poblation[index]
        # fitness = self.__fitness__[index]

        # grp1 = sorted(tournment[:2], key=self.fit_func, reverse=True)
        # grp2 = sorted(tournment[2:], key=self.fit_func, reverse=True)

        # final = sorted([grp1[0], grp2[0]], key=self.fit_func, reverse=True)
        # return tuple(final)

        return self.poblation[0:2]

    def _merge(self, heightmaps: Tuple[HeightMap, HeightMap]) -> HeightMap:
        # Suma ponderada
        h0, h1 = heightmaps
        h0 *= self.__merge__
        h1 *= 1-self.__merge__
        return (h0 + h1).normalize()
    
    def _mutate(self, h: HeightMap) -> HeightMap:
        tmp = HeightMap.build_from_map(h.__map__)
        tmp *= -1.5
        return (h + tmp).normalize()

a = GAT_Generator(.9, (300, 300), sea_level=0.45, poblation_size=7, iter=100)
world = a(True)
world.get_img().show()
