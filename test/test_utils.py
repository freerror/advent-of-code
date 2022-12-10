import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
from utils import Vec


def test_init():
    """Test the __init__() method"""
    v1 = Vec(1, 2)
    assert v1.x == 1
    assert v1.y == 2


def test_coord():
    """Test the coord property"""
    v1 = Vec(1, 2)
    assert v1.coord == (1, 2)

    v2 = Vec(3, 3)
    assert v2.coord == (3, 3)


def test_move():
    """Test the move method"""
    v1 = Vec(1, 2)
    v1.move("u", 3)
    assert v1.coord == (1, 5)
    v1.move("r", 3)
    assert v1.coord == (4, 5)
    v1.move("d", 3)
    assert v1.coord == (4, 2)
    v1.move("l", 3)
    assert v1.coord == (1, 2)


def test_converge():
    """Test the converge() method"""
    v1 = Vec(0, 0)
    v2 = Vec(3, 3)
    v1.converge(v2, 2)
    assert v1.x == 2
    assert v1.y == 2

    v1 = Vec(1, 2)
    v2 = Vec(3, 3)
    v1.converge(v2, 1)
    assert v1.x == 2
    assert v1.y == 3

    v1 = Vec(1, 2)
    v2 = Vec(3, 3)
    v1.converge(v2, 0)
    assert v1.x == 1
    assert v1.y == 2

    v1 = Vec(1, 2)
    v2 = Vec(3, 3)
    v1.converge(v2, None)
    assert v1.x == 3
    assert v1.y == 3


def test_copy():
    """Test the copy() method"""
    v1 = Vec(1, 2)
    v2 = Vec(3, 3)
    v1.copy(v2)
    assert v1.x == 3
    assert v1.y == 3


def test_add():
    """Test the __add__() method"""
    v1 = Vec(1, 2)
    v2 = Vec(3, 3)
    v1 += v2
    assert v1.x == 4
    assert v1.y == 5


def test_sub():
    """Test the __sub__() method"""
    v1 = Vec(1, 2)
    v2 = Vec(3, 3)
    v1 -= v2
    assert v1.x == -2
    assert v1.y == -1
