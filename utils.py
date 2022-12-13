"""Useful utils for solving puzzles or parsing input"""

from dataclasses import dataclass
from itertools import combinations
from typing import Optional


letters_to_numbers = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
    "i": 8,
    "j": 9,
    "k": 10,
    "l": 11,
    "m": 12,
    "n": 13,
    "o": 14,
    "p": 15,
    "q": 16,
    "r": 17,
    "s": 18,
    "t": 19,
    "u": 20,
    "v": 21,
    "w": 22,
    "x": 23,
    "y": 24,
    "z": 25,
}


def try_int(string):
    try:
        return int(string)
    except:
        return string


def lrg(start: int, arr: list):
    """returns a range based on the length of a list in one step, with a
    starting index
    """
    return range(start, len(arr))


@dataclass
class Vec:
    """Represents a thing with x and y coords"""

    x: int
    y: int

    @property
    def coord(self):
        """Return tuple coord"""
        return (self.x, self.y)

    def converge(self, other: "Vec", max_amount: Optional[int] = None):
        """Move toward up to the max amount"""
        if max_amount is None:
            self.copy(other)
            return
        x_dist = other.x - self.x
        y_dist = other.y - self.y
        self.x += min(max(x_dist, -max_amount), max_amount)
        self.y += min(max(y_dist, -max_amount), max_amount)

    def copy(self, other: "Vec"):
        """Copy the x and y coords from another Vec object"""
        self.x = other.x
        self.y = other.y

    def move(self, direction: str, amount: int):
        """Move the Vec object by the given amount"""
        if direction == "u":
            self.y += amount
        elif direction == "r":
            self.x += amount
        elif direction == "d":
            self.y -= amount
        elif direction == "l":
            self.x -= amount

    def __add__(self, other: "Vec"):
        self.x += other.x
        self.y += other.y

    def __sub__(self, other: "Vec"):
        self.x -= other.x
        self.y -= other.y

    def __mul__(self, other: "Vec"):
        self.x *= other.x
        self.y *= other.y

    def __repr__(self):
        return f"Vec({self.x}, {self.y})"


def search_grid(grid, target):
    """searches a grid or matrix of values for a particular
    target value
    """
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == target:
                return (i, j)
    return None


def find_substrings(string):
    """Takes a string and returns a list of all the possible
    substrings of the string, along with their starting and ending positions in
    the original string
    """
    substrings = []
    for i in range(len(string)):
        for j in range(i + 1, len(string) + 1):
            substrings.append((string[i:j], i, j))
    return substrings


def find_combinations(numbers):
    """takes a list of numbers and returns a list of all the possible
    combinations of the numbers, along with the sum of each combination
    """
    combinations_ = []
    for i in range(1, len(numbers) + 1):
        for combination in combinations(numbers, i):
            combinations_.append((combination, sum(combination)))
    return combinations_


def find_words_by_length(words, length):
    """takes a list of words and a target word length, and returns a list of
    all the words in the input list that are of the target length
    """
    return [word for word in words if len(word) == length]
