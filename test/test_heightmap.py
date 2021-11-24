import pytest
from numpy import array
from src.core.heightmap import HeightMap


LIST_1 = array([[0.1, 1, 3], [3, 2, 10], [3, 2, 1]])


def test_create_from_map():
    a = HeightMap.build_from_map(LIST_1)

    assert (LIST_1 == a.__map__).all()


def test_index_heightmap():
    a = HeightMap.build_from_map(LIST_1)

    assert LIST_1[1, 1] == a.__map__[1, 1]


def test_add_height_map():
    a = HeightMap.build_from_map(LIST_1)
    b = HeightMap.build_from_map(LIST_1)

    c = a + b

    assert (2 * LIST_1 == c.__map__).all()


def test_add_float():
    a = HeightMap.build_from_map(LIST_1)

    a += 2.3

    assert (2.3 + LIST_1 == a.__map__).all()


def test_mul_float():
    a = HeightMap.build_from_map(LIST_1)

    a *= 2.3

    assert (LIST_1 * 2.3 == a.__map__).all()


def test_normalize():
    a = HeightMap.build_from_map(LIST_1)

    a.normalize()

    assert (a.__map__ <= 1).all() and (a.__map__ >= 0).all()


def test_create():
    a = HeightMap((100, 100))

    assert (a.__map__ == 0).all() and a.shape == (100, 100)


@pytest.mark.xfail(raises=Exception)
def test_add():
    a = HeightMap.build_from_map(LIST_1)
    b = HeightMap((4, 4))

    c = a + b
