import pytest
from src.core.maps.heightmap import HeightMap
from src.core.maps.genetic import GAT_Generator
from numpy import array

LIST_1 = array([[0.3, 0.4, 0.32], [0.9, 0.75, 0.01], [0.875, 0.2, 0.3]])


def test_fit_function():
    h = HeightMap.build_from_map(LIST_1)
    g = GAT_Generator(0.8, (3, 3), sea_level=0.45)

    fit = g.fit_func(h)

    assert fit == 3 / 9


def test_generator_big_percentage():
    tol = 0.03
    g = GAT_Generator(0.95, (10, 10), tol=tol)

    map = g()

    fit = g.fit_func(map)

    assert fit >= 0.95 - tol and fit <= 0.95 + tol

def test_generator_small_percentage():
    tol = 0.03
    per = 0.05
    g = GAT_Generator(0.05, (10, 10), tol=tol)

    map = g()

    fit = g.fit_func(map)

    assert fit >= per - tol and fit <= per + tol
