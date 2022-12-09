"""Useful utils for solving puzzles or parsing input"""

from dataclasses import dataclass


def try_int(string):
    try:
        return int(string)
    except:
        return string


def lrg(start: int, arr: list):
    return range(start, len(arr))


@dataclass
class Vec:
    x: int
    y: int
