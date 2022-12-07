import os
from pathlib import Path
import sys
import requests


def get_file_contents(filepath: str | Path):
    """Open the file, read the contents to a string and return"""
    file = Path(filepath)
    with open(file) as f:
        return f.read()


def make_file(filepath: str | Path, content: str):
    """Write file with contents"""
    with open(filepath, "w") as f:
        f.write(content)


# CONSTANTS
YEAR_FILE = Path("year")
if not YEAR_FILE.exists():
    print("Enter year: ", end="")
    YEAR = int(input())
    make_file(YEAR_FILE, str(YEAR))
else:
    YEAR = int(get_file_contents(YEAR_FILE))
SESSION_FILE = Path("session")
if not SESSION_FILE.exists():
    print("Enter session cookie: ", end="")
    SESSION = input()
    make_file(SESSION_FILE, SESSION)
else:
    SESSION = get_file_contents(SESSION_FILE)


def download_input(day: int, year: int):
    """Download input from AOC website"""
    res = requests.get(
        f"https://adventofcode.com/{year}/day/{day}/input",
        cookies={"session": SESSION},
    )
    if not res.ok:
        if res.status_code == 404:
            raise FileNotFoundError(res.text)
        raise RuntimeError(
            f"Request failed: {res.status_code}, content: {res.content}"
        )
    return res.text[:-1]


def get_input(day: int, year: int = YEAR):
    """Get input from file or download from AOC website.
    Returns file contents as a string
    """
    dest = Path.joinpath(Path(sys.argv[0]).parent, "input")
    file = Path(dest)
    if not file.exists():
        payload = download_input(day, year)
        with open(file, "w", newline="\n") as f:
            f.write(payload)
    return get_file_contents(file)


def main():
    """Create all the individual day folders with a template"""
    day = 1
    with open("template") as f:
        template = f.read()
    while day <= 27:
        day_dir = Path(f"day {day}")
        if day_dir.exists():
            continue
        os.mkdir(day_dir)
        with open(day_dir) as f:
            f.write(template.replace("DAY", str(day)))


if __name__ == "__main__":
    main()
